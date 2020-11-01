from django.urls import path
from .views import my_profile_view

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile-view')
]