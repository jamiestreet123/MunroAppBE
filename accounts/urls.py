from django.urls import path, include
from rest_framework import routers
from .views import FollowersView, UserProfileView

router = routers.DefaultRouter()
router.register(r'follows', FollowersView, 'followers')
router.register(r'user', UserProfileView, 'user')

urlpatterns = [
    path('profiles/', include(router.urls)),
]