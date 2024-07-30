from django.db.models import query
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .serializers import ActivityPhotoSerializer, ActivitySerializer, ClimbSerializer, MunroSerializer, ProfilePhotoSerializer, WeatherSerializer
from .models import Activity, ActivityPhoto, Climb, Munro, ProfilePhoto, Weather
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from rest_framework import status
from accounts import models, serializers
from .S3 import create_presigned_post, create_presigned_url, getMultiplePresignedUrls

# Create your views here.

class WeatherView(viewsets.ModelViewSet):
    serializer_class = WeatherSerializer
    queryset = Weather.objects.all()

    @action(detail=False, methods=['GET'], url_path='goodWeather/(?P<date>[^/.]+)')
    def goodWeather(self, request, date):
        queryset = Weather.objects.all()
        goodWeatherMunros = queryset.filter(description='overcast clouds', date=date)
        serializer = WeatherSerializer(goodWeatherMunros, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='(?P<hillId>[^/.]+)')
    def byHillId(self, request, hillId):
        queryset = Weather.objects.all()
        hillWeather = queryset.filter(hillId=hillId)
        serializer = WeatherSerializer(hillWeather, many=True)
        return Response(serializer.data)

class MunroView(viewsets.ModelViewSet):
    serializer_class = MunroSerializer
    queryset = Munro.objects.all()

    @action(detail=False, methods=['GET'], url_path='(?P<day>[^/.]+)/(?P<hillId>[^/.]+)')
    def getMunroById(self, request, hillId):
        queryset = Munro.objects.all()
        hillWeather = queryset.filter(hillId=hillId)
        serializer = Munro(hillWeather, many=True)
        return Response(serializer.data)

class ClimbView(viewsets.ModelViewSet):
    serializer_class = ClimbSerializer
    queryset = Climb.objects.all()

    @action(detail=False, methods=['GET'])
    def getAllClimbs(self, request):
        queryset = Climb.objects.all()
        serializer = ClimbSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def addClimb(self, request):
        serializer = ClimbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='(?P<userId>[^/.]+)')
    def getClimbsByUserId(self, request, userId):
        queryset = Climb.objects.all().filter(userId=userId)
        serializer = ClimbSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['DELETE'], url_path ='delete/(?P<climb_id>[^/.]+)')
    def deleteClimb(self, request, climb_id):
        instance = Climb.objects.get(id=climb_id)
        if instance:
            instance.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='(?P<userId>[^/.]+)/(?P<hillId>[^/.]+)')
    def getClimbsByHillAndUser(self, request, userId, hillId):
        queryset = Climb.objects.all().filter(userId=userId, hillId=hillId)
        serializer = ClimbSerializer(queryset, many=True)
        return Response(serializer.data)

class ActivityView(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()

    @action(detail=False, methods=['GET'])
    def getAllActivities(self, request):
        queryset = Activity.objects.all()
        serializer = ActivitySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def addActivity(self, request):
        serializer = ActivitySerializer(data=request.data)
        #climbSerializer = MunroSerializer(data=request.data.munros, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='user/(?P<userId>[^/.]+)/recent/(?P<no_climbs>[^/.]+)')
    def getRecentActivitiesByUserId(self, request, userId, no_climbs):
        queryset = Activity.objects.all().filter(userId=userId).order_by('-dateAdded')[0: int(no_climbs)]       
        response = []
        for activity in queryset:
            serailizedActivity = ActivitySerializer(activity)
            user = serializers.UserNameSerializer(activity.userId)
            munros = MunroSerializer(activity.munros, many=True)
            photos = ActivityPhoto.objects.all().filter(activityId=activity.id)
            urls = getMultiplePresignedUrls(photos)
            response.append({"activity": serailizedActivity.data, "user": user.data, "munros": munros.data, "urls": urls})
        return Response(response)

    @action(detail=False, methods=['GET'], url_path='page/(?P<id>[^/.]+)')
    def getActivityById(self, request, id):
        activity = Activity.objects.all().filter(id=id).first()
        serailizedActivity = ActivitySerializer(activity)
        user = serializers.UserNameSerializer(activity.userId)
        munros = MunroSerializer(activity.munros, many=True)
        photos = ActivityPhoto.objects.all().filter(activityId=activity.id)
        urls = getMultiplePresignedUrls(photos)
        
        response = {"activity": serailizedActivity.data, "user": user.data, "munros": munros.data, "urls": urls}

        return Response(response)

    @action(detail=False, methods=['GET'], url_path='recent/(?P<page>[^/.]+)')
    def getRecentActivities(self, request, page):
        activities = Activity.objects.all().order_by('-dateAdded')[(int(page) * 10): ((int(page) + 1) * 10)]
        response = []
        for activity in activities:
            serailizedActivity = ActivitySerializer(activity)
            user = serializers.UserNameSerializer(activity.userId)
            munros = MunroSerializer(activity.munros, many=True)
            photos = ActivityPhoto.objects.all().filter(activityId=activity.id)
            urls = getMultiplePresignedUrls(photos)
            response.append({"activity": serailizedActivity.data, "user": user.data, "munros": munros.data, "urls": urls})

        return Response({"page": int(page), "data": response})

class MunroImageView(viewsets.ModelViewSet):
    
    @action(detail=False, methods=['GET'], url_path='munro/image')
    def getMunroImagePresignedURL(self, request):
        url = create_presigned_url('munroapp-s3-bucket', 'ben-nevis.webp')
        return Response({'url': url})

    @action(detail=False, methods=['POST'], url_path='post/image')
    def postImagePresignedURL(self, request):
        key = request.key
        url = create_presigned_post('munroapp-s3-bucket', key)
        return Response ({'url': url})
        
        
class ProfilePhotoView(viewsets.ModelViewSet):
    serializer_class = ProfilePhotoSerializer
    queryset = ProfilePhoto.objects.all()

    @action(detail=False, methods=['GET'], url_path='(?P<userId>[^/.]+)')
    def getProfilePhotoPresignedURL(self, request, userId):
        profilephoto = ProfilePhoto.objects.filter(userId=userId).order_by('-date_added').first()
        key = profilephoto.photo.file.obj.key
        print(key)
        url = create_presigned_url('munroapp-s3-bucket', key)
        return Response({'url': url})

class ActivityPhotoView(viewsets.ModelViewSet):
    serializer_class = ActivityPhotoSerializer
    queryset = ActivityPhoto.objects.all()
