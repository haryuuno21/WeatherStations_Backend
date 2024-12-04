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
        station = Station.objects.get(id=station_report.station_id.id)
        return station.photo_url
    
    def get_station_id(self, station_report):
        station = Station.objects.get(id=station_report.station_id.id)
        return station.id
    
    def get_short_name(self, station_report):
        station = Station.objects.get(id=station_report.station_id.id)
        return station.short_name
    
    class Meta:
        model = Station_report
        fields = ['temperature','station_id','short_name','photo_url']

class Temperature_reportSerializer(serializers.ModelSerializer):
    creator_id = serializers.StringRelatedField(read_only=True)
    moderator_id = serializers.StringRelatedField(read_only=True)
    report_date = serializers.DateField(format='%d.%m.%Y')
    class Meta:
        model = Temperature_report
        fields = ['status','report_date','creation_date','formation_date','completion_date','creator_id',
                  'moderator_id','average_temperature']

class Temperature_reportsSerializer(serializers.ModelSerializer):
    creator_id = serializers.StringRelatedField(read_only=True)
    moderator_id = serializers.StringRelatedField(read_only=True)
    report_date = serializers.DateField(format='%d.%m.%Y')
    class Meta:
        model = Temperature_report
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password','email']
    
    def create(self, validated_data):
        user = super().create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user
    def update(self,instance,validated_data):
        user = super().update(instance,validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user
    
class GETStationsSerializer(serializers.Serializer):
    current_report = serializers.IntegerField(default = None)
    stations_count = serializers.IntegerField(default = 0)
    stations = StationSerializer(many=True)
    class Meta:
        fields = ['current_report','stations_count',"stations"]

class GETReportInfoSerializer(serializers.Serializer):
    status = serializers.CharField()
    report_date = serializers.DateField(allow_null=True)
    creation_date = serializers.DateTimeField()
    formation_date = serializers.DateTimeField(allow_null=True)
    completion_date = serializers.DateTimeField(allow_null=True)
    creator_id = serializers.IntegerField()
    moderator_id = serializers.IntegerField(allow_null=True)
    average_temperature = serializers.IntegerField(allow_null=True)

    stations = Station_reportSerializer(many=True)

    class Meta:
        fields = [
            'status',
            'report_date',
            'creation_date',
            'formation_date',
            'completion_date',
            'creator_id',
            'moderator_id',
            'average_temperature',
            'stations',
        ]