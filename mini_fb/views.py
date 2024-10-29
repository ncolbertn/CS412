from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
import random
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import * 
from .forms import *
from typing import Any


class ShowAllProfileView(ListView):
    '''the view to show all Profiles'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileView(DetailView):
    '''Display one Profile selected by PK'''
    model = Profile # the model to display
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        print(f'CreateStatusView.form_valid(): form={form.cleaned_data}')
        print(f'CreateStatusView.form_valid(): self.kwargs={self.kwargs}')
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        print(files)
        for file in files:
            image = StatusMessageImage()
            image.image_file = file
            print("img file: ", file)
            image.status_message = sm
            print("status msg: ", sm)
            image.save()
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs={'pk':profile.pk})
    
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_messages"

    def get_success_url(self) -> str:
        profile = self.object.profile

        return reverse('profile', kwargs={'pk':profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    context_object_name = "status_messages"

    def get_success_url(self) -> str:
        profile = self.object.profile


class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile1pk = kwargs.get('pk')
        otherpk = kwargs.get('other_pk')
        profile = get_object_or_404(Profile, id=profile1pk)
        other_profile = get_object_or_404(Profile, id=otherpk)
        created = profile.add_friend(other_profile)
        return redirect(reverse('profile', kwargs={'pk': profile1pk}))
    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_onject_name = "profile"


        