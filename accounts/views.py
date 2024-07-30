from rest_framework import status
from rest_framework import viewsets
from .models import Followers, UserAccount
from .serializers import FollowerSerializer, UserProfileSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.

class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserAccount.objects.all()

    @action(detail=False, methods=['GET'], url_path='user/(?P<userId>[^/.]+)')
    def getUserById(self, request, userId):
        queryset = UserAccount.objects.get(id=userId)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)


class FollowersView(viewsets.ModelViewSet):
    serializer_class = FollowerSerializer
    queryset = Followers.objects.all()

    @action(detail=False, methods=['GET'], url_path='following/(?P<userId>[^/.]+)')
    def getAllFollowing(self, request, userId):
        queryset = Followers.objects.all().filter(follower=userId)
        serializer = FollowerSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='followers/(?P<userId>[^/.]+)')
    def getAllFollowers(self, request, userId):
        queryset = Followers.objects.all().filter(followee=userId)
        serializer = FollowerSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def addFollow(self, request):
        serializer = FollowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'], url_path ='(?P<follow_id>[^/.]+)')
    def deleteFollow(self, request, follow_id):
        instance = Followers.objects.get(id=follow_id)
        if instance:
            instance.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)