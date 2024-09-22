from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from WeatherStationsApp.models import Station, Station_report, Temperature_report
from django.db import connection
import datetime

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
#currentReport = reports[1]

def add_station_to_report(request,station_id):
    station = get_object_or_404(Station, id=station_id)
    user = request.user
    try:
        report = Temperature_report.objects.get(status='Draft', creator_id = user)
    except Temperature_report.DoesNotExist:
        report = Temperature_report.objects.create(status='Draft', creator_id = user)

    station_report, created = Station_report.objects.get_or_create(report_id = report, station_id = station)
    if created:
        station_report.save()

    return redirect(mainPage)

def mainPage(request):
    station_name = request.GET.get("station_name")
    user = request.user
    currentReport = Temperature_report.objects.filter(status='Draft', creator_id = user).first()
    stations_count = 0
    if currentReport:
        stations_count = Temperature_report.objects.get_stations_count(currentReport)

    if station_name:
        stations = Station.objects.filter(status = 'A').filter(short_name__icontains = station_name)
        return render(request, 'main_page.html', {'stations':stations,'filter':station_name,'currentReport':currentReport,'count':stations_count})
    
    stations = Station.objects.filter(status = 'A')
    return render(request, 'main_page.html', {'stations':stations,'filter':"Название станции",'currentReport':currentReport,'count':stations_count})



def description(request,id):
    station = get_object_or_404(Station,id = id)
    return render(request,'description.html', {'station':station})


def reportInfo(request,id):
    report = get_object_or_404(Temperature_report,id = id)
    stations = list()
    for station_report in Station_report.objects.filter(report_id = id):
        stations.append({'station':station_report.station_id,'temperature':station_report.temperature})
    return render(request,'report_page.html', {'report':report,'stations':stations,'report_date':report.report_date.strftime("%d.%m.%Y")})

def delete_report(request, report_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE reports SET status = 'Deleted' WHERE id = %s", [report_id])
    
    return redirect(mainPage)