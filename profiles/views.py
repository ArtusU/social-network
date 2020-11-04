from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from profiles.models import Profile
from .forms import ProfileModelForm

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