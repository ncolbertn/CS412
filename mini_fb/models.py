from django.db import models

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