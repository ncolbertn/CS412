from django.db import models
from django.urls import reverse

class Profile(models.Model):
    ''''''

    # data attributes of a Profile:
    first_name = models.TextField(blank=False)
    surname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    pfp = models.URLField(blank=True)

    def __str__(self):
        ''''''

        return f'{self.first_name} {self.surname}'
    def get_status_message(self):
        message = StatusMessage.objects.filter(profile=self).order_by("timestamp")
        return message
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk':self.pk})
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.message}'
    
    def get_images(self):
        images = StatusMessageImage.objects.filter(status_message=self).order_by("timestamp")
        return images
    
class StatusMessageImage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.image_file}'
    