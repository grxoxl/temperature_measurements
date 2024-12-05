from django.db import models

# Create your models here.

class TemperatureReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()  # Store temperature in Celsius or Fahrenheit

    def __str__(self):
        return f'{self.timestamp} - {self.temperature}°C'