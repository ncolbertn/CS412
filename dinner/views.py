from django.views.generic import CreateView, ListView, View
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import *
from .forms import *
import random

class RestaurantCreateView(CreateView):
    model = Restaurant
    fields = ['name', 'distance_from_me', 'cost_range']
    success_url = reverse_lazy('restaurant_list')  # Replace 'restaurant_list' with your desired URL pattern name

    def form_valid(self, form):
        # You can add any additional logic here if needed
        return super().form_valid(form)

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'  # Optional: Specify your template name
    context_object_name = 'restaurants' 

class MainPageView(View):
    def get(self, request):
        form = RestaurantFilterForm()
        return render(request, 'dinner/main_page.html', {'form': form})

    def post(self, request):
        form = RestaurantFilterForm(request.POST)
        if form.is_valid():
            # Start with all restaurants
            queryset = Restaurant.objects.all()

            # Filter by maximum distance if provided
            max_distance = form.cleaned_data.get('max_distance')
            if max_distance is not None:
                queryset = queryset.filter(distance_from_me__lte=max_distance)

            # Filter by cost range if provided
            cost_range = form.cleaned_data.get('cost_range')
            if cost_range:
                queryset = queryset.filter(cost_range=cost_range)

            # Randomly select a restaurant
            restaurant = queryset.order_by('?').first()

            return render(request, 'dinner/random_restaurant.html', {
                'restaurant': restaurant,
                'form': form
            })
        else:
            return render(request, 'dinner/main_page.html', {'form': form})