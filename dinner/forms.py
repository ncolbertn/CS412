# forms.py
from django import forms
from .models import Restaurant

class RestaurantFilterForm(forms.Form):
    max_distance = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False, label='Maximum Distance (minutes)'
    )
    cost_range = forms.ChoiceField(
        choices=[('', 'Any')] + Restaurant.COST_RANGE_CHOICES,
        required=False, label='Cost Range'
    )
