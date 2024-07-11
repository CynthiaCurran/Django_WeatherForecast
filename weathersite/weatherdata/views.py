from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import pgeocode #used for converting zip codes to coordinates we need to grab weather data
import requests
from datetime import datetime

# Create your views here.


def index(request):
    return render(request, 'weatherdata/index.html')

def weather_query(request):

    zip_code = ''

    if request.method == 'POST':
        zip_code = request.POST.get('zip_code')


    if(len(str(zip_code)) != 5 or zip_code == ''):
        return render(request, 'weatherdata/weather_query_error.html')
    
    nomi = pgeocode.Nominatim('us')
    zip_info = nomi.query_postal_code(zip_code)
    latitude = zip_info.latitude
    longitude = zip_info.longitude

    #url for grabbing weather data for the coordinates
    url = 'https://api.weather.gov/points/{},{}'.format(latitude, longitude)

    req = requests.get(url)
    req_json = req.json()

    forecast_url = req_json['properties']['forecastHourly']

    req = requests.get(forecast_url)
    req_json = req.json()

    #grab the next 12 hours of data
    raw_data = req_json['properties']['periods'][:11]
    parsed_data = []

    for i in raw_data:
        entry = {}

        #formatting for time period 
        startTime = int(i['startTime'][11:13])
        amOrPm = ''
        if startTime > 11:
            amOrPm = 'PM'
        else:
            amOrPm = 'AM'
        if startTime > 12:
            startTime -= 12
        if startTime == 0:
            startTime = 12

        entry['startTime'] = "{} {}".format(startTime, amOrPm)

        entry['temperature'] = i['temperature']
        entry['rainChance'] = i['probabilityOfPrecipitation']['value']
        entry['wind'] = i['windSpeed']
        entry['description'] = i['shortForecast']

        parsed_data.append(entry)


    context = {
        "data": parsed_data,
    }

    return render(request, 'weatherdata/weather_query.html', context)