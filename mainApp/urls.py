from django.urls import path
from . import views

urlpatterns = [
    path('getCountryRegionMapping', views.getCountryRegionMapping),
    path('getAggregatedCsv', views.getAggregatedCsv),
    path('', views.index, name='index'),

]
