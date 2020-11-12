from django.shortcuts import render
from django.views.generic import ListView
from profiles.models import Profile, Relationship
from .forms import ProfileModelForm
from django.contrib.auth.models import User

def home_view(request):
    user = request.user
    hello = 'Hello world'

    context = {
        'user': user,
        'hello' : hello,
    }
    return render(request, 'home.html', context)
    # return HttpResponse('Hello world')


def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm
    }
    
    return render(request, 'profiles/myprofile.html', context)

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)



def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'profiles/to_invite_list.html', context)


class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    #context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        
        rel_receiver = []
        rel_sender = []
        
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        
        for item in rel_s:
            rel_sender.append(item.sender.user)

        context["rel_receiver"] = rel_receiver
        context["rel_seneder"] = rel_sender
        context["is_empty"] = False

        if len(self.get_queryset()) == 0:
            context["is_empty"] = True
        
        return context


