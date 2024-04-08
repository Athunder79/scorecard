from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.models import Clubs

User = get_user_model()

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=False, blank=False)
    address = models.CharField(max_length=255)
    rating = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ['latitude', 'longitude'] 

    def __str__(self):
        return self.name

class Round(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    round_date = models.DateField(auto_now_add=True)
    round_completed = models.BooleanField(default=False)


    def __str__(self):
        return str(self.round_date)

class Hole(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole_num = models.IntegerField(null=False, blank=False)
    hole_par = models.IntegerField(null=False, blank=False)
    hole_distance = models.IntegerField(null=True, blank=True)

    # check if the hole_num is unique for the round if not raise an error
    def save(self, *args, **kwargs):
        if not self.pk:
            if Hole.objects.filter(round=self.round, hole_num=self.hole_num).exists():
                raise ValueError('This hole number already exists for this round. Please continue or finsh the hole')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.course} - Hole {self.hole_num}'

class Shot(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)
    hole_num = models.IntegerField(null=True, blank=True)
    hole_par = models.IntegerField(null=True, blank=True)
    shot_num_per_hole = models.IntegerField(null=True, blank=True, default=1)  
    latitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=7 , blank=True, null=False)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=True)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=7, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shot_distance = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('scorecard-create')
    
    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def ShotNumber(self):
        if self.shot_num_per_hole:
            return 1
        # incresase the shot number by 1
        self.shot_num_per_hole = F('shot_num_per_hole') + 1

