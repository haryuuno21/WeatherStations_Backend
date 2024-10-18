from django.contrib import admin
from API import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('stations/', views.StationsList.as_view(), name='stations-list'),
    path('stations/<int:id>/', views.StationDetail.as_view(), name='staion-detail'),
    path('add-pic/<int:id>/',views.post_pic,name='add-pic'),
    path('stations/<int:id>/add-to-report/',views.add_to_report,name='add-to-report'),
    path('reports/',views.get_reports,name='reports-list'),
    path('reports/<int:id>/',views.ReportDetail.as_view(),name='report-detail'),
    path('reports/<int:id>/form/',views.form_report,name='form-report'),
    path('reports/<int:id>/confirm/',views.confirm_report,name='confirm-report'),
    path('reports/<int:id>/delete/',views.delete_report,name='delete-report'),
    path('stations-reports/<int:report_id>/<int:station_id>/remove_station/',views.remove_from_report,name='remove-station'),
    path('stations-reports/<int:report_id>/<int:station_id>/put_temperature/',views.put_temperature,name='put-temperature'),
    path('registration/',views.registration,name='registration'),
    path('users/<int:id>/',views.put_user,name='put_user'),
    path('authentication/',views.authentication,name='authentication'),
    path('deauthorization/',views.deauthorization,name='deauthorization'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]