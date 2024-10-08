from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from API.serializers import *
from API.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from API.minio import add_pic,del_pic
import datetime

def user():
    try:
        user1 = User.objects.get(id=1)
    except:
        user1 = AuthUser(id=1, first_name="Иван", last_name="Иванов", password=1234, username="user1")
        user1.save()
    return user1

def moderator():
    try:
        moderator = User.objects.get(id=2)
    except:
        moderator = AuthUser(id=2, first_name="Даниил", last_name="Шиленок", password=1234, username="haryuuno")
        moderator.save()
    return moderator

class StationsList(APIView):
    model_class = Station
    serializer_class = StationSerializer

    def get(self, request, format=None):
        station_name = request.GET.get("station_name")
        currentReport = Temperature_report.objects.filter(status='Draft', creator_id = user()).first()
        if(station_name):
            stations = self.model_class.objects.filter(status = 'A').filter(short_name__icontains = station_name)
        else:
            stations = self.model_class.objects.filter(status = 'A')
        serializer = self.serializer_class(stations, many=True)
        if(not currentReport):
            data = {"current_report":None,"stations":serializer.data}
            return Response(data)
        data = {"current_report":currentReport.id,"stations":serializer.data}
        return Response(data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            station = serializer.save()
            pic = request.FILES.get("pic")
            pic_result = add_pic(station, pic)
            if 'error' in pic_result.data:    
                return pic_result
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StationDetail(APIView):
    model_class = Station
    serializer_class = StationSerializer

    def get(self, request, id, format=None):
        station = get_object_or_404(self.model_class, id=id)
        if station.status == 'D':
            return Response(data="station is deleted",status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(station)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        station = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(station, data=request.data, partial=True)
        if 'pic' in serializer.initial_data:
            pic_result = add_pic(station, serializer.initial_data['pic'])
            if 'error' in pic_result.data:
                return pic_result
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        station = get_object_or_404(self.model_class, id=id)
        station.status = "D"
        station.save()
        del_pic(station)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['Get'])
def get_reports(request, format=None):
    filter_status = request.GET.get("status")
    start_date = request.GET.get("start-date")
    end_date = request.GET.get("end-date")
    reports = Temperature_report.objects.exclude(status='Draft').exclude(status="Deleted")
    if(filter_status):
        reports = reports.filter(status = filter_status)
    if(start_date):
        start_date = datetime.datetime.strptime(start_date,"%d.%m.%Y")
        reports = reports.filter(formation_date__gte = start_date)
    if(end_date):
        end_date = datetime.datetime.strptime(end_date,"%d.%m.%Y")
        reports = reports.filter(formation_date__lte = end_date)
    serializer = Temperature_reportsSerializer(reports, many=True)
    return Response(serializer.data)

@api_view(['Get'])
def get_report(request, id, format=None):
    report = get_object_or_404(Temperature_report, id=id)
    if report.status == 'Deleted':
        return Response(data="report is deleted",status=status.HTTP_400_BAD_REQUEST)
    stations_in_report = Station_report.objects.filter(report_id = report)
    report_serializer = Temperature_reportSerializer(report)
    stations_in_report_serializer = Station_reportSerializer(stations_in_report, many = True)
    data = report_serializer.data | {'stations':stations_in_report_serializer.data}
    return Response(data)

@api_view(['Put'])
def put_report_info(request,id,format=None):
    report = get_object_or_404(Temperature_report,id=id)
    if report.status == 'Deleted':
        return Response(data="report is deleted",status=status.HTTP_400_BAD_REQUEST)
    report_date = request.data['report-date']
    report_date = datetime.datetime.strptime(report_date,"%d.%m.%Y")
    report.report_date = report_date
    report.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['Put'])
def form_report(request,id,format=None):
    report = get_object_or_404(Temperature_report,id=id)
    if report.status == 'Deleted':
        return Response(data="report is deleted",status=status.HTTP_400_BAD_REQUEST)
    if report.status != 'Draft':
        return Response(data="report has already been formed",status=status.HTTP_400_BAD_REQUEST)
    report.formation_date = now()
    report.status = "Formed"
    report.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['Put'])
def confirm_report(request,id,format=None):
    report = get_object_or_404(Temperature_report,id=id)
    if report.status == 'Deleted':
        return Response(data="report is deleted",status=status.HTTP_400_BAD_REQUEST)
    if report.status == 'Draft':
        return Response(data="report is in draft",status=status.HTTP_400_BAD_REQUEST)
    if report.status != 'Formed':
        return Response(data="report has already been confirmed/declined",status=status.HTTP_400_BAD_REQUEST)
    confirm = request.data['confirm']
    if confirm == '1':
        report.status = 'Completed'
        report.moderator_id = moderator()
        report.average_temperature = Temperature_report.objects.get_average_temperature(report)
        report.completion_date = now()
        report.save()
        return Response(status=status.HTTP_200_OK)
    if confirm == '0':
        report.status = 'Rejected'
        report.moderator_id = moderator()
        report.completion_date = now()
        report.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])
def delete_report(request,id,format=None):
    report = get_object_or_404(Temperature_report,id=id)
    report.status = 'Deleted'
    report.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Post'])
def post_pic(request, id, format=None):
    station = get_object_or_404(Station,id=id)
    pic = request.FILES.get("pic")
    pic_result = add_pic(station, pic)
    if 'error' in pic_result.data:
        return pic_result

@api_view(['Post'])
def add_to_report(request, id, format=None):
    station = get_object_or_404(Station, id=id)
    if station.status == 'D':
        return Response(data="station is deleted",status=status.HTTP_400_BAD_REQUEST)
    try:
        report = Temperature_report.objects.get(status='Draft', creator_id = user())
    except Temperature_report.DoesNotExist:
        report = Temperature_report.objects.create(status='Draft', creator_id = user())

    station_report, created = Station_report.objects.get_or_create(report_id = report, station_id = station)
    if created:
        station_report.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(data="station already added",status=status.HTTP_400_BAD_REQUEST)