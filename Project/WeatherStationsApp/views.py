from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from WeatherStationsApp.models import Station, Station_report, Temperature_report
from django.db import connection, models 
import datetime

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

    return redirect(stationsPage)

def stationsPage(request):
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
    try:
        report = Temperature_report.objects.get(id=id)
    except Temperature_report.DoesNotExist:
        return redirect(stationsPage)
    
    if report is None or report.status == "Deleted":
        return redirect(stationsPage)
    
    stations = list()
    for station_report in Station_report.objects.filter(report_id = id):
        stations.append({'station':station_report.station_id,'temperature':station_report.temperature})
    return render(request,'report_page.html', {'report':report,'stations':stations,'report_date':report.report_date.strftime("%d.%m.%Y")})

def delete_report(request, report_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE reports SET status = 'Deleted' WHERE id = %s", [report_id])
    
    return redirect(stationsPage)