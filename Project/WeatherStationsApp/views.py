from django.shortcuts import render
from django.http import HttpResponse
from WeatherStationsApp.models import WeatherStation

stations = list()
station = WeatherStation.create(0,'http://localhost:9000/weather-station-images/0.webp','ВДНХ','Метеостанция ВДНХ',
                                    '129223, г.Москва, ВДНХ, Проспект Мира, вл.119,стр.423',
                                    'Никитина Светлана Александровна','8-499-760-36-95')
stations.append(dict(station.AsDict(),**{'temperature':'+24°'}))
station = WeatherStation.create(1,'http://localhost:9000/weather-station-images/1.jpg','Балчуг','Метеостанция Балчуг',
                                    '115184, г.Москва, Средне-Овчинникосвкий пер., д.1, стр.4',
                                    'Ревкова Татьяна Геннадьевна','8-495-953-42-89')
stations.append(dict(station.AsDict(),**{'temperature':'+25°'}))
station = WeatherStation.create(2,'http://localhost:9000/weather-station-images/2.jpg','Тушино','Метеостанция Тушино',
                                    '123481, г.Москва, пос.Новобутаково, д.39, стр.1',
                                    'Зинкина Марина Васильевна','8-495-571-52-21')
stations.append(dict(station.AsDict(),**{'temperature':'+23°'}))
station = WeatherStation.create(3,'http://localhost:9000/weather-station-images/3.jpg','Михайловское','Метеостанция Михайловское',
                                    '142020, г.Москва, поселение Вороновское, д.Голохвастово, д.2г',
                                    '–','8-495-850-60-83')
stations.append(dict(station.AsDict(),**{'temperature':'+24°'}))

reports = list()
reports.append({'id':0, 'stations':[stations[0],stations[1]]})
reports.append({'id':1, 'stations':[stations[0],stations[2],stations[3]]})
currentReport = reports[1]


def mainPage(request): 
    return render(request, 'main_page.html', {'stations':stations,'currentReport':currentReport,'count':len(currentReport['stations'])})


def description(request,id):
    return render(request,'description.html',stations[id])


def reportInfo(request,id):
    return render(request,'report_page.html', reports[id])


def setFilter(request):
    input_text = request.POST['filter_text'].lower()
    filteredStations = list()
    if(not input_text):
        return mainPage(request)

    for station in stations:
        if station['shortName'].lower().startswith(input_text):
            filteredStations.append(station)

    return render(request,'main_page.html',{'stations':filteredStations,'currentReport':currentReport,'count':len(currentReport['stations'])})