import requests
from bs4 import BeautifulSoup
from .weather import WEATHER_URLS
from munroapp import models

def getWeatherData(munro_index):
    munro = models.Munro.objects.get(pk=munro_index)
    print(munro.weather)
    if munro.weather != '':
        base_url = 'https://www.mountain-forecast.com/peaks/' + munro.weather
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find('table', {"class":"forecast-table__table"})
        dates = table.find('tr', {"data-row":"days"}).find_all('td')
        colspans = [int(date['colspan']) for date in dates]
        out1 = [date.find('div', {"class":"forecast-table-days__content"}) for date in dates]
        out2 = [out.find_all('div') for out in out1]
        out3 = [{"day": out[0].text.strip(), "date": out[1].text} for out in out2]
        finalDates = []
        for i in range(len(out3)):
            for j in range(colspans[i]):
                finalDates.append(out3[i])

        times = table.find('tr', {"data-row": "time"}).find_all('span')
        times2 = [time.text.strip() for time in times]

        summaries = table.find('tr', {"data-row": "phrases"}).find_all('td')
        summaries2 = [summary.text.strip() for summary in summaries]

        max1 = table.find('tr', {"data-row": "temperature-max"}).find_all('td')
        max2 = [max.text.strip() for max in max1]

        min1 = table.find('tr', {"data-row": "temperature-min"}).find_all('td')
        min2 = [min.text.strip() for min in min1]

        feels1 = table.find('tr', {"data-row": "temperature-chill"}).find_all('td')
        feels2 = [feels.text.strip() for feels in feels1]

        for i in range(len(finalDates)):
            weatherObject = models.Weather()
            weatherObject.hillId = munro_index
            weatherObject.hillname = WEATHER_URLS[munro_index]['hillname']
            weatherObject.date = finalDates[i]['day'] + ' ' + finalDates[i]['date']
            weatherObject.time = times2[i]
            weatherObject.weather = summaries2[i]
            weatherObject.maxTemp = max2[i]
            weatherObject.minTemp = min2[i]
            weatherObject.feelsLike = feels2[i]
            weatherObject.save()

        return 'done'
    else:
        return 'none'

def run() :
    weatherData = models.Weather.objects.all()
    weatherData.delete()
    for i in range(len(WEATHER_URLS)):
        getWeatherData(i)

# when App is deployed, run this script and update weather in the database (Heroku/Django scheduler?)