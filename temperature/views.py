from django.shortcuts import render
from .models import TemperatureReading

def temperature_list(request):
    # Fetch all temperature readings from the database
    readings = TemperatureReading.objects.all().order_by('-timestamp')

    # Pass the readings to the template
    return render(request, 'temperature/temperature_list.html', {'readings': readings})


