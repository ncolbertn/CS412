from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User

class Profile(models.Model):
    ''''''
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)


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
    
    def get_friends(self):
        friend_relations = Friend.objects.filter(Q(profile1=self) | Q(profile2=self))
        friend_profiles = []
        for relation in friend_relations:
            if relation.profile1 == self:
                friend_profiles.append(relation.profile2)
            else:
                friend_profiles.append(relation.profile1)

        return friend_profiles
    
    def add_friend(self, other):
        if self == other:
            return False
        elif Friend.objects.filter((Q(profile1=self) & Q(profile2=other)) | (Q(profile1=other) & Q(profile2=self))):
            return False
        else:
            Friend.objects.create(profile1=self, profile2=other)
            return True
        
    def get_friend_suggestions(self):
        friends_profile1_qs = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_profile2_qs = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)

        # Combine friend IDs and add self ID to the exclusion list
        exclude_ids = list(friends_profile1_qs) + list(friends_profile2_qs) + [self.id]

        # Retrieve Profiles that are not friends and are not self
        suggestions = Profile.objects.exclude(id__in=exclude_ids)

        return suggestions
    

    def get_news_feed(self):
        friends = self.get_friends()
        profile_ids = [self.id] + []
        for f in friends:
            profile_ids.append(f.id)
        print(profile_ids)
        news_feed = StatusMessage.objects.filter(profile__in=profile_ids).order_by('-timestamp')
        print(news_feed)
        return news_feed
            


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
    
class Friend(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")

    def __str__(self):
        s = f'{self.profile1} & {self.profile2}'
        return s
    