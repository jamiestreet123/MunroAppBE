import requests
from munroapp import models
import json

DIRECTIONS_API_KEY = ''

def getWeatherData(munro_index):
    munro = models.Munro.objects.get(pk=munro_index)
    base_url = 'http://api.openweathermap.org/data/2.5/forecast'
    url = base_url + '?lat=' + str(munro.startPointLatitude) + '&lon=' + str(munro.startPointLongitude) + '&appid=' + DIRECTIONS_API_KEY + '&units=metric'
    r = requests.get(url)
    json_r = json.loads(r.content)
    lst = json_r['list']
    for item in lst:
        weatherObject = models.Weather()
        weatherObject.hillId = munro_index
        weatherObject.maxTemp = item['main']['temp_max']
        weatherObject.minTemp  = item['main']['temp_min']
        weatherObject.feelsLike  = item['main']['feels_like']
        weatherObject.description  = item['weather'][0]['description']
        date_text = item['dt_txt']
        date_split = date_text.split(' ')
        weatherObject.date  = date_split[0]
        weatherObject.time  = date_split[1]
        weatherObject.save()
    
    return 'done'
    

def run() :
    weatherData = models.Weather.objects.all()
    weatherData.delete()
    for i in range(282):
        getWeatherData(i)

# when App is deployed, run this script and update weather in the database (Heroku/Django scheduler?)