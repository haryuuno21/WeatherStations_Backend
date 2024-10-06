from django.contrib import admin
from API import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('stations/', views.StationsList.as_view(), name='stations-list'),
    path('stations/<int:id>/', views.StationDetail.as_view(), name='staion-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]