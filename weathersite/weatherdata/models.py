from django.db import models

# Create your models here.

class Forecast(models.Model):
    update_time = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_day_time = models.BooleanField()
    temperatute = models.DecimalField(max_digits=3, decimal_places=0, default=0)    #in fahrenheit
    wind_speed = models.DecimalField(max_digits=3, decimal_places=0, default=0)     #in mph
    wind_direction = models.CharField(max_length=1)                         #N, S, W, E are the returns
    precipitation_perc = models.DecimalField(max_digits=3, decimal_places=0, default=0) #chance of precipitation in percentage
    humidity_perc = models.DecimalField(max_digits=3, decimal_places=0, default=0)  #relative humidity percentage

    short_forecast = models.CharField(max_length=100)   #short description of the weather