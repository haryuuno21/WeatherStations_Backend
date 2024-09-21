from django.shortcuts import render
from django.http import HttpRequest

stations = list()
station = {'id':0,'photo':'http://localhost:9000/weather-station-images/0.webp','shortName':'ВДНХ','fullName':'Метеостанция ВДНХ',
                                    'adress':'129223, г.Москва, ВДНХ, Проспект Мира, вл.119,стр.423',
                                    'chiefFIO':'Никитина Светлана Александровна','phoneNumber':'8-499-760-36-95','seaLevel':147}
stations.append(station)
station = {'id':1,'photo':'http://localhost:9000/weather-station-images/1.jpg','shortName':'Балчуг','fullName':'Метеостанция Балчуг',
                                    'adress':'115184, г.Москва, Средне-Овчинникосвкий пер., д.1, стр.4',
                                    'chiefFIO':'Ревкова Татьяна Геннадьевна','phoneNumber':'8-495-953-42-89','seaLevel':124}
stations.append(station)
station = {'id':2,'photo':'http://localhost:9000/weather-station-images/2.jpg','shortName':'Тушино','fullName':'Метеостанция Тушино',
                                    'adress':'123481, г.Москва, пос.Новобутаково, д.39, стр.1',
                                    'chiefFIO':'Зинкина Марина Васильевна','phoneNumber':'8-495-571-52-21','seaLevel':167}
stations.append(station)
station = {'id':3,'photo':'http://localhost:9000/weather-station-images/3.jpg','shortName':'Михайловское','fullName':'Метеостанция Михайловское',
                                    'adress':'142020, г.Москва, поселение Вороновское, д.Голохвастово, д.2г',
                                    'chiefFIO':'–','phoneNumber':'8-495-850-60-83','seaLevel':192}
stations.append(station)

reports = list()
reports.append({'id':0, 'stations':[{'station': stations[0],'temperature':'+22'},
                                    {'station': stations[1],'temperature':'+23'}],
                        'report_date':'13.09.2024'})
reports.append({'id':1, 'stations':[{'station': stations[0],'temperature':'+24'},
                                    {'station': stations[2],'temperature':'+25'},
                                    {'station': stations[3],'temperature':'+23'}],
                        'report_date':'21.09.2024'})
currentReport = reports[1]


def mainPage(request : HttpRequest): 
    station_name = request.GET.get("station_name")
    filteredStations = list()
    if(not station_name):
        return render(request, 'main_page.html', {'stations':stations,'filter':"Название станции",'currentReport':currentReport,'count':len(currentReport['stations'])})

    for station in stations:
        if station_name.lower() in station['shortName'].lower():
            filteredStations.append(station)
    
    return render(request, 'main_page.html', {'stations':filteredStations,'filter':station_name,'currentReport':currentReport,'count':len(currentReport['stations'])})
    


def description(request,id):
    return render(request,'description.html',stations[id])


def reportInfo(request,id):
    return render(request,'report_page.html', reports[id])