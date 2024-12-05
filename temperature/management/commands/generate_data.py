import random
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, WriteOptions
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generates synthetic temperature data'

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write(self.style.NOTICE('Generating synthetic temperature data...'))
            token = 'BgmcjiYgjhHiXwb2hF5aAqFFPU_Y6AUDU_E2gZy-5uOjCXMp60YUf6PyuBJsqbcvEvnl-bsIl56LCJyQ19UrOg=='
            client = InfluxDBClient(
                url='http://localhost:8086',
                token=token,
                org='GGWP'
            )
            write_api = client.write_api()
            for i in range(100):
                temperature = random.uniform(18.0, 30.0)
                timestamp = datetime.utcnow() - timedelta(minutes=i)
                point = (
                    'temperature',
                    {},
                    { 'value': temperature },
                    timestamp.isoformat() + 'Z'
                )
                write_api.write(bucket="temperature_data", record=point)
            self.stdout.write(self.style.SUCCESS('Synthetic data generated and stored in InfluxDB'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating data: {e}'))
        finally:
            client.close()