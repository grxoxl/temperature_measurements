from django.urls import path
from . import views

urlpatterns = [
    path('serve-plot/', views.serve_plot, name='serve_plot'), 
    path('get-temperature-data/', views.get_temperature_data, name='get_temperature_data'),
    path('temperature-data/', views.temperature_data, name='temperature_data'),
]
