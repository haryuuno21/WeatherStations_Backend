from API.models import *
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        exclude = ['description']

class Temperature_reportSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Temperature_report
        fields = '__all__'

class Station_reportSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Station_report
        fields = '__all__'

class User_reportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']