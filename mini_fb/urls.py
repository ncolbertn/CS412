from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.ShowAllProfileView.as_view(), name="show_all_profiles"),
    
]