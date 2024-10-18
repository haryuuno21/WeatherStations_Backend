from API.models import *
from rest_framework import serializers

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        exclude = ['description','status']

class Station_reportSerializer(serializers.ModelSerializer):
    station_id = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()
    def get_photo_url(self, station_report):
        station = Station.objects.get(id=1)
        return station.photo_url
    
    def get_station_id(self, station_report):
        station = Station.objects.get(id=1)
        return station.id
    
    def get_short_name(self, station_report):
        station = Station.objects.get(id=1)
        return station.short_name
    
    class Meta:
        model = Station_report
        fields = ['temperature','station_id','short_name','photo_url']

class Temperature_reportSerializer(serializers.ModelSerializer):
    creator_id = serializers.StringRelatedField(read_only=True)
    moderator_id = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Temperature_report
        fields = ['status','report_date','creation_date','formation_date','completion_date','creator_id',
                  'moderator_id','average_temperature']

class Temperature_reportsSerializer(serializers.ModelSerializer):
    creator_id = serializers.StringRelatedField(read_only=True)
    moderator_id = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Temperature_report
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['first_name','last_name','username','email','password']