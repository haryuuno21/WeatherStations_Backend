from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
from django.utils.timezone import now


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(("email адрес"), unique=True)
    password = models.CharField(max_length=255, verbose_name="Пароль")    
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

    USERNAME_FIELD = 'username'

    objects = UserManager()

class Station(models.Model):
    STATUS_CHOICES = [
    ("A", "Active"),
    ("D", "Deleted"),
    ]
    short_name = models.CharField(max_length = 50)
    full_name = models.CharField(max_length = 100)
    status = models.CharField(max_length = 1,choices = STATUS_CHOICES, default="A")
    description = models.CharField(max_length = 255, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    address = models.CharField(max_length = 255)
    chief_fio = models.CharField(max_length = 100, null=True)
    phone_number = models.CharField(max_length = 20, null=True)
    sea_level = models.IntegerField(default = 0)

    class Meta:
        db_table = "stations"

class Temperature_report_manager(models.Manager):
    def get_stations_count(self, report):
        return Temperature_report.objects.filter(id = report.id).annotate(count_stations = models.Count("station_report"))[0].count_stations
    def get_average_temperature(self, report):
        return Station_report.objects.filter(report_id = report.id).aggregate(models.Avg("temperature"))['temperature__avg']

class Temperature_report(models.Model):
    STATUS_CHOICES = [
    ("Draft", "Draft"),
    ("Deleted", "Deleted"),
    ("Formed", "formed"),
    ("Completed", "Completed"),
    ("Rejected", "Rejected")
    ]
    status = models.CharField(max_length = 9,choices = STATUS_CHOICES, default="Draft")
    report_date = models.DateField(default=now(),null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    formation_date = models.DateTimeField(null=True)
    completion_date = models.DateTimeField(null=True)
    creator_id = models.ForeignKey(CustomUser,related_name="reports_created",  on_delete=models.SET_DEFAULT, default=0)
    moderator_id = models.ForeignKey(CustomUser, related_name='reports_moderated', on_delete=models.SET_NULL, null=True)
    average_temperature = models.IntegerField(null=True)

    objects = Temperature_report_manager()

    class Meta:
        db_table = "reports"


class Station_report(models.Model):
    station_id = models.ForeignKey(Station, on_delete=models.CASCADE)
    report_id = models.ForeignKey(Temperature_report, on_delete=models.CASCADE)
    temperature = models.IntegerField(default = 0)

    class Meta:
        db_table = "stations_reports"
        constraints = [
            models.UniqueConstraint(fields=['station_id', 'report_id'], name='unique_station_report')
        ]
