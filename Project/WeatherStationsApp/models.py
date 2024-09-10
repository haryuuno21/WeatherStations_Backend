from django.db import models

class WeatherStation(models.Model):
    id = models.IntegerField
    photo = models.CharField(max_length=50)
    shortName = models.CharField(max_length = 20)
    fullName = models.CharField(max_length = 50)
    adress = models.CharField(max_length = 100)
    chiefFIO = models.CharField(max_length = 50)
    phoneNumber = models.CharField(max_length = 20)

    def AsDict(self):
        return {'id':self.id, 'photo':self.photo, 'shortName':self.shortName,
                'fullName':self.fullName,'adress':self.adress,'chiefFIO':self.chiefFIO,
                'phoneNumber':self.phoneNumber}
    
    @classmethod
    def create(cls,id:int, photo:str, shortName:str, fullName:str, adress:str, chiefFIO:str, phoneNumber:str):
        station = cls(id = id, photo = photo, shortName = shortName,
                              fullName = fullName, adress = adress,
                              chiefFIO = chiefFIO, phoneNumber = phoneNumber)
        return station

