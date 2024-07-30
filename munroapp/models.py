from django.db import models
from django.db.models.fields.files import ImageField
from accounts.models import UserAccount
from django.utils import timezone

# Create your models here.

class Weather(models.Model):
    hillId = models.IntegerField()
    hillname = models.CharField(max_length=120)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=50)
    description = models.CharField(max_length=100, default=None)
    maxTemp = models.IntegerField()
    minTemp = models.IntegerField()
    feelsLike = models.IntegerField()

    def _str_(self):
        return self.hillname

class Munro(models.Model):
    hillId = models.IntegerField()
    hillname = models.CharField(max_length=120)
    longitude = models.FloatField()
    latitude = models.FloatField()
    metres = models.FloatField()
    county = models.CharField(max_length=100, default=None, null=True)
    meaning = models.CharField(max_length=250, default=None, null=True)
    startPointLongitude = models.FloatField()
    startPointLatitude = models.FloatField()
    
    def _str_(self):
        return self.hillname

class Climb(models.Model):
    userId = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    hillId = models.ForeignKey(Munro, on_delete=models.CASCADE, null=False)
    dateClimbed = models.DateField(default=None, null=True)

class Activity(models.Model):
    userId = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    munros = models.ManyToManyField(Munro, blank=True)
    title = models.CharField(max_length=120)
    dateAdded = models.DateTimeField(auto_now_add=True)
    dateClimbed = models.DateField()
    tagged_users = models.ManyToManyField(UserAccount, related_name='taggedUserToUser', blank=True)
    description = models.CharField(max_length=2000, null=True, default=None)

class ActivityPhoto(models.Model):
    activityId = models.ForeignKey(Activity, on_delete=models.CASCADE, null=False, default=0)
    photo = models.ImageField(upload_to='activity_photos/')
    date_added = models.DateTimeField(default=timezone.now)

class ProfilePhoto(models.Model):
    userId = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False)
    photo = models.ImageField(upload_to = 'profile_photos/')
    date_added = models.DateTimeField(default=timezone.now)
