from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import random
from django.views.generic import ListView
from .models import * 


class ShowAllProfileView(ListView):
    '''the view to show all Profiles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'
