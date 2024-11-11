from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('restaurants/add/', views.RestaurantCreateView.as_view(), name='restaurant_add'),
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('', views.MainPageView.as_view(), name='main_page')
]