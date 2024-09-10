from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from WeatherStationsApp.models import WeatherStation

stations = list()
for i in range(4):
    station = WeatherStation.create(i,'/static/images/1.png','ВДНХ','Метеостанция ВДНХ',
                                    '129223, г.Москва, ВДНХ, Проспект Мира, вл.119,стр.423',
                                    'Никитина Светлана Александровна','8-499-760-36-95')
    stations.append(dict(station.AsDict(),**{'temperature':'+28°'}))
    
def hello(request): 
    return render(request, 'main_page.html', {'stations':stations})

def description(request,id):
    return render(request,'description.html')

def orderInfo(request):
    return render(request,'order_page.html', { 'data' : {
        'stations': [{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+28°',
                      'id' : 1},{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+26°',
                      'id' : 1}]
    }})