from django.urls import path
from . import views

urlpatterns = [
    # ... your other URL patterns ...
    path('', views.statistics, name='statistics'),
]