from django.urls import path
from . import views

urlpatterns = [
    path('', views.temperature_list, name='temperature_list'),
]
