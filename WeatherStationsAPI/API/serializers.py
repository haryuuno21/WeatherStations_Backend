from API.models import *
from rest_framework import serializers

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        exclude = ['description']

class Station_reportSerializer(serializers.ModelSerializer):
    station_id = StationSerializer(read_only = True)
    class Meta:
        model = Station_report
        fields = ['temperature','station_id']

class Temperature_reportSerializer(serializers.ModelSerializer):
    creator_id = serializers.StringRelatedField(read_only=True)
    moderator_id = serializers.StringRelatedField(read_only=True)
    stations = Station_reportSerializer(many=True,read_only = True)
    class Meta:
        model = Temperature_report
        fields = ['status','report_date','creation_date','formation_date','completion_date','creator_id',
                  'moderator_id','average_temperature','stations']

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