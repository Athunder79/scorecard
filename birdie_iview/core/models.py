from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.models import Clubs

User = get_user_model()

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255)
    rating = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ['latitude', 'longitude'] 

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and Course.objects.filter(latitude=self.latitude, longitude=self.longitude).exists():
            # If a course with the same latitude and longitude exists, do not save
            print(f"Course with latitude {self.latitude} and longitude {self.longitude} already exists.")
        else:
            super(Course, self).save(*args, **kwargs)


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
    

    # if hole number is not greater than last shot hole number then update shot end latitude and longitude with the current latitude and longitude
    def save(self, *args, **kwargs):
        if not self.pk:
            if Shot.objects.filter(round=self.round, hole=self.hole).exists():
                last_shot = Shot.objects.filter(round=self.round, hole=self.hole).order_by('-shot_num_per_hole').first()
                if self.hole_num <= last_shot.hole_num:
                    last_shot.end_latitude = self.latitude
                    last_shot.end_longitude = self.longitude
                    last_shot.save()
        super().save(*args, **kwargs)

    def ShotNumber(self):
        if self.shot_num_per_hole:
            return 1
        # incresase the shot number by 1
        self.shot_num_per_hole = F('shot_num_per_hole') + 1

