from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=100, blank=True)
    address2 = models.CharField(max_length=100, blank=True) 
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    

    def __str__(self):
        return f'{self.user.username} Profile'

class Clubs(models.Model):
    id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=100, blank=True, null=False)
    club_type = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.club_name