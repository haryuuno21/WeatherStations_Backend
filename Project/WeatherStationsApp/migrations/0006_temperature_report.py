# Generated by Django 5.1.1 on 2024-09-21 17:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeatherStationsApp', '0005_alter_station_chief_fio_alter_station_description_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Temperature_report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Deleted', 'Deleted'), ('Formed', 'formed'), ('Completed', 'Completed'), ('Rejected', 'Rejected')], default='Draft', max_length=9)),
                ('report_date', models.DateField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('formation_date', models.DateTimeField(null=True)),
                ('completion_date', models.DateTimeField(null=True)),
                ('creator_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_created', to=settings.AUTH_USER_MODEL)),
                ('moderator_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_moderated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reports',
            },
        ),
    ]