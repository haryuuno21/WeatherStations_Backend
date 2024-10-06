from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from API.serializers import *
from API.models import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view

def user():
    try:
        user1 = User.objects.get(id=1)
    except:
        user1 = AuthUser(id=1, first_name="Иван", last_name="Иванов", password=1234, username="user1")
        user1.save()
    return user1

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StationDetail(APIView):
    model_class = Station
    serializer_class = StationSerializer

    def get(self, request, id, format=None):
        station = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(station)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        station = get_object_or_404(self.model_class, id=id)
        serializer = self.serializer_class(station, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        station = get_object_or_404(self.model_class, id=id)
        station.status = "D"
        return Response(status=status.HTTP_204_NO_CONTENT)