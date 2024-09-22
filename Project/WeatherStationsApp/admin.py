from django.contrib import admin
from WeatherStationsApp import models

admin.site.register(models.Station)
admin.site.register(models.Temperature_report)
admin.site.register(models.Station_report)
