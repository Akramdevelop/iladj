from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctorDashboard/', views.doctorDashboard, name='doctorDashboard'),
    path('assistant/addPatient/', views.assistantIndex, name='assistant'),
    path('switchofdoctors/', views.switchofdoctors, name='switchofdoctors'),
    path('calculation/', views.calculation, name='calculation'),
    path('favoriteMedicine/', views.favoriteMedicine, name='favoriteMedicine'),
    path('sheet/<int:patientcardpk>/',
         views.sheet, name='sheet'),
]
