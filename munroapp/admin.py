from django.contrib import admin
from .models import Munro, Weather

class WeatherAdmin(admin.ModelAdmin):
    list_display = ('hillId', 'hillname', 'date', 'time', 'description', 'maxTemp', 'minTemp', 'feelsLike')

class MunroAdmin(admin.ModelAdmin):
    list_display = ('hillId', 'hillname', 'longitude', 'latitude', 'metres', 'county', 'meaning', 'startPointLongitude', 'startPointLatitude')

# Register your models here.

admin.site.register(Weather, WeatherAdmin)
admin.site.register(Munro, MunroAdmin)