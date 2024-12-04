from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from API.serializers import *
from API.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from API.minio import add_pic,del_pic
import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from API.permissions import *
from django.conf import settings
import redis
import uuid

session_storage = redis.Redis(host='localhost', port=6380, db=0)

def getUser(request):
    try:
        ssid = request.COOKIES["session_id"]
        username = session_storage.get(ssid)
        user = CustomUser.objects.get(username = username.decode("utf-8"))
    except:
        return None
    return user

stations_param = openapi.Parameter('station_name', openapi.IN_QUERY, description="Название станции", type=openapi.TYPE_STRING)
stations_response = openapi.Response('GET stations', GETStationsSerializer)

class StationsList(APIView):
    model_class = Station
    serializer_class = StationSerializer
    permission_classes = [IsManagerOrGetOnly]

    @swagger_auto_schema(manual_parameters=[stations_param],responses={200:stations_response})
    def get(self, request, format=None):
        station_name = request.GET.get("station_name")
        user = getUser(request)
        if(user):
            currentReport = Temperature_report.objects.filter(status='Draft', creator_id = user.id).first()
        else:
            currentReport = None
        if(station_name):
            stations = self.model_class.objects.filter(status = 'A').filter(short_name__icontains = station_name)
        else:
            stations = self.model_class.objects.filter(status = 'A')
        serializer = self.serializer_class(stations, many=True)
        if(not currentReport):
            data = {"current_report":None, "stations_count":0, "stations":serializer.data}
            return Response(data)
        data = {"current_report":currentReport.id,"stations_count":Temperature_report.objects.get_stations_count(currentReport),
                "stations":serializer.data}
        return Response(data)
    
    
    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            station = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
station_response = openapi.Response('GET station', StationSerializer)
class StationDetail(APIView):
    model_class = Station
    serializer_class = StationSerializer
    permission_classes = [IsManagerOrGetOnly]

    @swagger_auto_schema(responses={200:station_response,400:'station is deleted'})
    def get(self, request, id, format=None):
        station = get_object_or_404(self.model_class, id=id)
        if station.status == 'D':
            return Response(data="station is deleted",status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(station)
        return Response(serializer.data)
    
    
    @swagger_auto_schema(request_body=serializer_class)
    def put(self, request, id, format=None):
        station = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(station, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(responses={200:'station is deleted'})
    def delete(self, request, id, format=None):
        station = get_object_or_404(self.model_class, id=id)
        station.status = "D"
        station.save()
        del_pic(station)
        return Response('station is deleted', status=status.HTTP_200_OK)
    
schema1 = openapi.Schema(title='report-date',type=openapi.TYPE_STRING,format=openapi.FORMAT_DATE)

class ReportDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(responses={200:GETReportInfoSerializer})
    def get(self, request, id, format=None):
        report = get_object_or_404(Temperature_report, id=id)
        user = getUser(request)
        if report.creator_id != user and not user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if report.status == 'Deleted':
            return Response(data="report is deleted",status=status.HTTP_400_BAD_REQUEST)
        stations_in_report = Station_report.objects.filter(report_id = report)
        report_serializer = Temperature_reportSerializer(report)
        stations_in_report_serializer = Station_reportSerializer(stations_in_report, many = True)
        data = report_serializer.data | {'stations':stations_in_report_serializer.data}
        return Response(data)
    
    @swagger_auto_schema(request_body=schema1,responses={200:"report date changed",400:"report is deleted"})
    def put(self, request, id, format=None):
        report = get_object_or_404(Temperature_report,id=id)
        user = getUser(request)
        if report.creator_id != user and not user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if report.status == 'Deleted':
            return Response(data="report is deleted",status=status.HTTP_400_BAD_REQUEST)
        report_date = request.data['report-date']
        report_date = datetime.datetime.strptime(report_date,"%d.%m.%Y")
        report.report_date = report_date
        report.save()
        return Response(status=status.HTTP_200_OK)

status_param = openapi.Parameter('status', openapi.IN_QUERY, description="Статус отчета", type=openapi.TYPE_STRING)
start_date_param = openapi.Parameter('start-date', openapi.IN_QUERY, description="Фильтр по дате снизу",
                                      type=openapi.TYPE_STRING,format=openapi.FORMAT_DATE)
end_date_param = openapi.Parameter('end-date', openapi.IN_QUERY, description="Фильтр по дате сверху",
                                    type=openapi.TYPE_STRING,format=openapi.FORMAT_DATE)

@swagger_auto_schema(manual_parameters=[status_param,start_date_param,end_date_param],
                     method="Get",responses={200:Temperature_reportsSerializer(many=True)})
@api_view(['Get'])
@permission_classes([IsAuthenticated])
def get_reports(request, format=None):
    filter_status = request.GET.get("status")
    start_date = request.GET.get("start-date")
    end_date = request.GET.get("end-date")
    user = getUser(request)
    if(user.is_staff or user.is_superuser):
        reports = Temperature_report.objects.exclude(status='Draft').exclude(status="Deleted")
    else:
        reports = Temperature_report.objects.exclude(status='Draft').exclude(status="Deleted").filter(creator_id = user)
    if(filter_status):
        reports = reports.filter(status = filter_status.capitalize())
    if(start_date):
        start_date = datetime.datetime.strptime(start_date,"%d.%m.%Y")
        reports = reports.filter(formation_date__gte = start_date)
    if(end_date):
        end_date = datetime.datetime.strptime(end_date,"%d.%m.%Y")
        reports = reports.filter(formation_date__lte = end_date)
    serializer = Temperature_reportsSerializer(reports, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method="Put",responses={200:"report_formed",400:"report is deleted/already formed"})
@api_view(['Put'])
@permission_classes([IsAuthenticated])
def form_report(request,id,format=None):
    report = get_object_or_404(Temperature_report,id=id)
    user = getUser(request)
    if report.creator_id != user and not user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if report.status == 'Deleted':
        return Response(data="report is deleted",status=status.HTTP_400_BAD_REQUEST)
    if report.status != 'Draft':
        return Response(data="report has already been formed",status=status.HTTP_400_BAD_REQUEST)
    report.formation_date = now()
    report.status = "Formed"
    report.save()
    return Response("report formed",status=status.HTTP_200_OK)

confirm_schema = openapi.Schema(title="confirm",type=openapi.TYPE_INTEGER,enum=[0,1],description="Флаг подтверждения отчета")

@swagger_auto_schema(request_body=confirm_schema, method="Put",responses={200:'report confirmed',400:'something wrong with the report'})
@api_view(['Put'])
@permission_classes([IsManager])
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
        report.moderator_id = request.user.id
        report.average_temperature = Temperature_report.objects.get_average_temperature(report)
        report.completion_date = now()
        report.save()
        return Response(status=status.HTTP_200_OK)
    if confirm == '0':
        report.status = 'Rejected'
        report.moderator_id = request.user.id
        report.completion_date = now()
        report.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['Delete'])
@permission_classes([IsAuthenticated])
def delete_report(request,id,format=None):
    report = get_object_or_404(Temperature_report,id=id)
    user = getUser(request)
    if report.creator_id != user and not user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if report.status == 'Completed' or report.status == 'Rejected':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    report.status = 'Deleted'
    report.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

pic_param = openapi.Parameter('pic', openapi.IN_QUERY, description="picture", type=openapi.TYPE_FILE,required=True)

@swagger_auto_schema(manual_parameters=[pic_param],method='Post',responses={200:'photo added'})
@api_view(['Post'])
@permission_classes([IsManager])
def post_pic(request, id, format=None):
    station = get_object_or_404(Station,id=id)
    pic = request.FILES.get("pic")
    pic_result = add_pic(station, pic)
    if 'error' in pic_result.data:
        return pic_result
    return Response(status=status.HTTP_200_OK)

@swagger_auto_schema(method='Post',responses={201:'station added to report',400:'station already added or deleted'})
@api_view(['Post'])
@permission_classes([IsAuthenticated])
def add_to_report(request, id, format=None):
    station = get_object_or_404(Station, id=id)
    user = getUser(request)
    if station.status == 'D':
        return Response(data="station is deleted",status=status.HTTP_400_BAD_REQUEST)
    try:
        report = Temperature_report.objects.get(status='Draft', creator_id = user)
    except Temperature_report.DoesNotExist:
        report = Temperature_report.objects.create(status='Draft', creator_id = user)

    station_report, created = Station_report.objects.get_or_create(report_id = report, station_id = station)
    if created:
        station_report.save()
        return Response(data={"currentReport":report.pk},status=status.HTTP_201_CREATED)
    return Response(data="station already added",status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method="Delete",responses={204:"station removed from report",400:"report is not in draft"})
@api_view(['Delete'])
@permission_classes([IsAuthenticated])
def remove_from_report(request, report_id, station_id, format=None):
    report = get_object_or_404(Temperature_report, id=report_id)
    if report.status != 'Draft':
        return Response(data="report is not in draft",status=status.HTTP_400_BAD_REQUEST)
    station = get_object_or_404(Station, id = station_id)
    Station_report.objects.filter(report_id = report, station_id = station).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


temperature_schema = openapi.Schema(title="temperature",type=openapi.TYPE_INTEGER,description="Новая температура")
@swagger_auto_schema(method="Put",request_body=temperature_schema,responses={200:"temperature added",400:"report is not in draft"})
@api_view(['Put'])
@permission_classes([IsAuthenticated])
def put_temperature(request, report_id, station_id, format=None):
    report = get_object_or_404(Temperature_report, id=report_id)
    if report.status != 'Draft':
        return Response(data="report is not in draft",status=status.HTTP_400_BAD_REQUEST)
    station = get_object_or_404(Station, id = station_id)
    station_report = get_object_or_404(Station_report, station_id = station, report_id = report)
    station_report.temperature = request.data['temperature']
    station_report.save()
    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=UserSerializer)
@csrf_exempt
@api_view(['Post'])
@permission_classes([AllowAny])
def registration(request, format=None):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='put',request_body=UserSerializer)
@api_view(['Put'])
@permission_classes([IsAuthenticated])
def put_user(request, format=None):
    user = getUser(request)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


auth_schema = openapi.Schema("session_id",type=openapi.TYPE_STRING,format=openapi.FORMAT_UUID)
auth_response = openapi.Response("session cookie",auth_schema)


@swagger_auto_schema(request_body=UserSerializer,method="Post",responses={200:auth_response,400:"authentification failed"})
@api_view(['Post'])
@permission_classes([AllowAny])
def authentication(request, format=None):
    username = request.data.get('username')
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        random_key = uuid.uuid4()
        session_storage.set(str(random_key), username)
        response = Response(data={"userName":username,"userGroup":"watcher"},status=status.HTTP_200_OK)
        response.set_cookie("session_id", random_key)
        return response
    else:
        return Response("authentication failed",status=status.HTTP_400_BAD_REQUEST)

@api_view(['Post'])
@permission_classes([IsAuthenticated])
def deauthorization(request,format=None):
    ssid = request.COOKIES["session_id"]
    session_storage.delete(ssid)
    response = Response({'status': 'Success'})
    response.delete_cookie("session_id")
    return response