import numpy as np
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point
from django.core.management.base import BaseCommand
from influxdb_client.client.write_api import SYNCHRONOUS
from django.conf import settings

class Command(BaseCommand):
    help = 'Generates synthetic temperature data'
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
            delete_api = client.delete_api()
            for i in range(100):
                temperature = np.random.normal(21, 0.5)
   
                timestamp = datetime.utcnow() - timedelta(minutes=i)
                point = Point('temperature') \
                    .tag("location", "home") \
                    .field("value", temperature) \
                    .time(timestamp.isoformat() + 'Z')
                write_api.write(bucket="temperature_data", record=point)
            start_time = "1970-01-01T00:00:00Z"  # Start of time
            end_time = (datetime.utcnow() - timedelta(hours=24)).isoformat() + 'Z'
            delete_api.delete(
                start=start_time,
                stop=end_time,
                bucket="temperature_data",
                org=self.org,
                predicate='_measurement="temperature"'
            )
            self.stdout.write(self.style.SUCCESS('Synthetic data generated and stored in InfluxDB'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating data: {e}'))
        finally:
            client.close()
    