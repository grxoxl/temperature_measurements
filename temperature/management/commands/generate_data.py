import random
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
            for i in range(500):
                temperature = random.uniform(18.0, 30.0)
                timestamp = datetime.utcnow() - timedelta(minutes=i)
                point = Point('temperature') \
                    .tag("location", "home") \
                    .field("value", temperature) \
                    .time(timestamp.isoformat() + 'Z')
                write_api.write(bucket="temperature_data", record=point)
            self.stdout.write(self.style.SUCCESS('Synthetic data generated and stored in InfluxDB'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating data: {e}'))
        finally:
            client.close()
    