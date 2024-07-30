from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from munroapp import views

router = routers.DefaultRouter()
router.register(r'weather', views.WeatherView, 'weather')
router.register(r'munros', views.MunroView, 'munro')
router.register(r'climbs', views.ClimbView, 'climb')
router.register(r'activities', views.ActivityView, 'activity')
router.register(r'images', views.MunroImageView, 'images')
router.register(r'profilephoto', views.ProfilePhotoView, 'profilephoto')
router.register(r'activityphoto', views.ActivityPhotoView, 'activityphoto')

urlpatterns = [
    path('api/', include(router.urls)),
]