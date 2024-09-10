from django.db import models

class WeatherStation(models.Model):
    id = models.BigIntegerField
    photo = models.URLField
    shortName = models.CharField(max_length = 20)
    fullName = models.CharField(max_length = 50)
    adress = models.CharField(max_length = 100)
    chiefFIO = models.CharField(max_length = 50)
    phoneNumber = models.CharField(max_length = 20)