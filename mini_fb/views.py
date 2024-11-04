from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
import random
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import * 
from .forms import *
from typing import Any
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin 


class ShowAllProfileView(ListView):
    '''the view to show all Profiles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileView(DetailView):
    '''Display one Profile selected by PK'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' in kwargs:
            context['user_form'] = kwargs['user_form']
        else:
            context['user_form'] = UserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None  
        form = self.get_form()
        user_form = UserCreationForm(request.POST)

        if form.is_valid() and user_form.is_valid():
            return self.form_valid(form, user_form)
        else:
            return self.form_invalid(form, user_form)

    def form_valid(self, form, user_form):
        user = user_form.save()
        form.instance.user = user
        self.object = form.save()
        username = user_form.cleaned_data.get('username')
        raw_password = user_form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, user_form):
        return self.render_to_response(
            self.get_context_data(form=form, user_form=user_form)
        )

    def get_success_url(self):
        return reverse('show_all_profiles')
    


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Http404("No Profile found for the current user.")
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Http404("No Profile found for the current user.")
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            image = StatusMessageImage()
            image.image_file = file
            image.status_message = sm
            image.save()
        return redirect(reverse('profile', kwargs={'pk':profile.pk}))
    
    def get_success_url(self) -> str:
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs={'pk':profile.pk})
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self, queryset=None):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Http404("No Profile found for the current user.")
        return profile


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_messages"

    def get_success_url(self) -> str:
        profile = self.object.profile

        return reverse('profile', kwargs={'pk':profile.pk})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    context_object_name = "status_messages"

    def get_success_url(self) -> str:
        profile = self.object.profile


class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Http404("No Profile found for the current user.")
        otherpk = kwargs.get('other_pk')
        other_profile = get_object_or_404(Profile, id=otherpk)
        created = profile.add_friend(other_profile)
        return redirect(reverse('profile' , kwargs={'pk':profile.pk}))
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Http404("No Profile found for the current user.")
        return profile

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_onject_name = "profile"

    def get_object(self, queryset=None):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Http404("No Profile found for the current user.")
        return profile


        