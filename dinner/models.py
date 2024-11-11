from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    distance_from_me = models.DecimalField(max_digits=5, decimal_places=2, help_text="Distance in minutes")
    
    COST_RANGE_CHOICES = [
        ('$', 'Budget'),
        ('$$', 'Moderate'),
        ('$$$', 'Expensive'),
    ]
    cost_range = models.CharField(max_length=3, choices=COST_RANGE_CHOICES)

    def __str__(self):
        return self.name
