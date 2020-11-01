from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from profiles.models import Profile

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

    context = {
        'profile': profile
    }
    
    return render(request, 'profiles/myprofile.html', context)