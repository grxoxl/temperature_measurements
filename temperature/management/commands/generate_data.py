import random
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point
from django.core.management.base import BaseCommand
from influxdb_client.client.write_api import SYNCHRONOUS

class Command(BaseCommand):
    help = 'Generates synthetic temperature data'
    url = 'http://localhost:8086'
    token = 'eysyl_gzK_cXoZXY0VAyEK3OSHai7B4wtCOD6xrRsrEdIjn5eSrR7QwLb5MDXw94vJcX88XCyxV2A5p9JMpu0w=='
    org = 'GGWP'

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
                temperature = random.gauss(24, 5)
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
    