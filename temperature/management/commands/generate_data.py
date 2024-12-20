import numpy as np
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point
from django.core.management.base import BaseCommand
from influxdb_client.client.write_api import SYNCHRONOUS
from django.conf import settings

class Command(BaseCommand):
    help = 'Generates synthetic temperature and pressure data'
    url = settings.INFLUXDB["url"]
    token = settings.INFLUXDB["token"]
    org = settings.INFLUXDB["org"]


    def handle(self, *args, **kwargs):
        try:
            self.stdout.write(self.style.NOTICE('Generating synthetic temperature data...'))
            client = InfluxDBClient(
                url=self.url,
                token=self.token,
                org= self.org
            )
            write_api = client.write_api(write_options=SYNCHRONOUS)
            
            for i in range(100):
                temperature = np.random.normal(21, 0.5)
   
                timestamp = datetime.utcnow() - timedelta(minutes=i)
                point = Point('temperature') \
                    .tag("location", "home") \
                    .field("value", temperature) \
                    .time(timestamp.isoformat() + 'Z')
                write_api.write(bucket="temperature_data", record=point)
            
            self.stdout.write(self.style.NOTICE('Generating synthetic pressure data...'))
            
            for i in range(100):
                pressure = np.random.normal(150, 0.5)
   
                timestamp = datetime.utcnow() - timedelta(minutes=i)
                point = Point('pressure') \
                    .tag("location", "home") \
                    .field("value", pressure) \
                    .time(timestamp.isoformat() + 'Z')
                write_api.write(bucket="pressure_data", record=point)
                
            self.stdout.write(self.style.SUCCESS('Synthetic data generated and stored in InfluxDB'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating data: {e}'))
        finally:
            client.close()
    