from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("munroapp.urls")),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("", include("accounts.urls")),
]