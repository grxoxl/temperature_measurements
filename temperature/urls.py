from django.urls import path
from . import views

urlpatterns = [
    path('get-temperature-data/', views.get_temperature_data, name='get_temperature_data'),
    path('temperature-data/', views.temperature_data, name='temperature_data'),
]
