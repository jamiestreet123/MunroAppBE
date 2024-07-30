from rest_framework import serializers
from .models import ActivityPhoto, Climb, Munro, ProfilePhoto, Weather, Activity
from accounts.serializers import UserCreateSerializer
from accounts.models import UserAccount

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('hillId', 'date', 'time', 'description', 'maxTemp', 'minTemp', 'feelsLike')

class MunroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Munro
        fields = ('hillId', 'hillname', 'longitude', 'latitude', 'metres', 'county', 'meaning', 'startPointLongitude', 'startPointLatitude')

class ClimbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climb
        fields = ('id', 'userId', 'hillId', 'dateClimbed')

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'userId', 'title', 'munros', 'dateAdded', 'dateClimbed', 'tagged_users', 'description')

    def create(self, activity_data):
        munros = activity_data.pop('munros')
        taggedUsers = activity_data.pop('tagged_users')
        activity = Activity.objects.create(**activity_data)
        for i in range(len(munros)):
            activity.munros.add(munros[i])
            climb = Climb(userId = activity_data['userId'], hillId = munros[i], dateClimbed = activity_data['dateClimbed'])
            climb.save()
        for i in range(len(taggedUsers)):
            activity.tagged_users.add(taggedUsers[i])
        return activity

class ActivityPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityPhoto
        fields = ('activityId', 'photo')

class ProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoto
        fields = ('userId', 'photo')