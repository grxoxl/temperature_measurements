# from django.http import JsonResponse, HttpResponse
# from influxdb_client import InfluxDBClient
# from influxdb_client.client.query_api import QueryApi
# from django.shortcuts import render, redirect
# from django.conf import settings

# # Replace these with your actual InfluxDB settings

# INFLUXDB_URL = settings.INFLUXDB["url"]
# INFLUXDB_TOKEN = settings.INFLUXDB["token"]
# INFLUXDB_ORG = settings.INFLUXDB["org"]
# INFLUXDB_BUCKET = settings.INFLUXDB["bucket"]

# def get_temperature_data(request):
#     # if not request.user.is_authenticated:
#     #     return redirect('account:login')
#     try:
#         # Initialize the InfluxDB client
#         client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
#         query_api: QueryApi = client.query_api()

#         # Write the query to retrieve the last 100 points
#         query = f'''
#         from(bucket: "{INFLUXDB_BUCKET}")
#           |> range(start: -24h)
#           |> filter(fn: (r) => r._measurement == "temperature")
#           |> keep(columns: ["_time", "_value"])
#           |> sort(columns: ["_time"], desc: true)
#           |> limit(n: 100)
#         '''
#         # query = f'''
#         # from(bucket: "{INFLUXDB_BUCKET}")
#         # |> range(start: -24h)  # Retrieve data for the last 24 hours
#         # |> filter(fn: (r) => r._measurement == "temperature")
#         # |> keep(columns: ["_time", "_value"])
#         # |> sort(columns: ["_time"], desc: true)
#         # |> limit(n: 100)
#         # '''


#         tables = query_api.query(query)

#         # Extract data points
#         data = []
#         for table in tables:
#             for record in table.records:
#                 data.append({
#                     "time": record.get_time(),
#                     "value": record.get_value(),
#                 })

#         # Return as JSON response
#         return JsonResponse({"data": data}, safe=True)
    
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)
    
# def temperature_data(request):
#     if not request.user.is_authenticated:
#         return redirect('account:login')
#     try:
#         client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
#         query_api = client.query_api()

#         # Query to get temperature data
#         query = f'''
#         from(bucket: "{INFLUXDB_BUCKET}")
#           |> range(start: -24h)
#           |> filter(fn: (r) => r._measurement == "temperature")
#           |> keep(columns: ["_time", "_value"])
#           |> sort(columns: ["_time"], desc: true)
#           |> limit(n: 100)
#         '''
#         # query = f'''
#         # from(bucket: "{INFLUXDB_BUCKET}")
#         # |> range(start: -24h)  # Retrieve data for the last 24 hours
#         # |> filter(fn: (r) => r._measurement == "temperature")
#         # |> keep(columns: ["_time", "_value"])
#         # |> sort(columns: ["_time"], desc: true)
#         # |> limit(n: 100)
#         # '''
#         tables = query_api.query(query)

#         # Parse query results into a list of dictionaries
#         data = []
#         for table in tables:
#             for record in table.records:
#                 data.append({
#                     "timestamp": record.get_time(),
#                     "temperature": record.get_value(),
#                 })
        
#         # Render data in a template
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
#             return JsonResponse({"readings": data})

#         # Render data in a template
#         return render(request, 'temperature/temperature_list.html', {'readings': data})

#     except Exception as e:
#         return render(request, 'error.html', {'error': str(e)})


from django.http import JsonResponse, HttpResponse
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi
from django.shortcuts import render, redirect
from django.conf import settings
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
matplotlib.use('Agg')

# Replace these with your actual InfluxDB settings
INFLUXDB_URL = settings.INFLUXDB["url"]
INFLUXDB_TOKEN = settings.INFLUXDB["token"]
INFLUXDB_ORG = settings.INFLUXDB["org"]
INFLUXDB_BUCKET_TEMP = settings.INFLUXDB["bucket_temperature"]
INFLUXDB_BUCKET_PRES = settings.INFLUXDB["bucket_pressure"]

def fetch_temperature_data():
    """Fetches the temperature data from InfluxDB."""
    try:
        client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
        )
        query_api = client.query_api()
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET_TEMP}")
          |> range(start: -24h)
          |> filter(fn: (r) => r._measurement == "temperature")
          |> keep(columns: ["_time", "_value"])
          |> sort(columns: ["_time"], desc: true)
          |> limit(n: 100)
        '''
        return query_api.query(query)
    except Exception as e:
        raise RuntimeError(f"Error fetching data from InfluxDB: {e}")
    
def fetch_pressure_data():
    """Fetches the pressure data from InfluxDB."""
    try:
        client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
        )
        query_api = client.query_api()
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET_PRES}")
          |> range(start: -24h)
          |> filter(fn: (r) => r._measurement == "pressure")
          |> keep(columns: ["_time", "_value"])
          |> sort(columns: ["_time"], desc: true)
          |> limit(n: 100)
        '''
        return query_api.query(query)
    except Exception as e:
        raise RuntimeError(f"Error fetching data from InfluxDB: {e}")

def serve_plot(request):
    """Generates a temperature and pressure plot and serves it as a PNG image."""
    try:
        tables = fetch_temperature_data()
        table_pres = fetch_pressure_data()

        # Extract data points
        times, temperatures, pressures = [], [], []
        for table in tables:
            for record in table.records:
                times.append(record.get_time())
                temperatures.append(record.get_value())
                pressures.append(record.get_value())
        
        for table in table_pres:
            for record in table.records:
                pressures.append(record.get_value())

        # Create the plot
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(16, 10))
        
        ax[0].plot(times, temperatures, label="Temperature (°C)", color="blue")
        ax[0].set_xlabel("Time")
        ax[0].set_ylabel("Temperature (°C)")
        ax[0].set_title("Temperature Over the Last 24 Hours")
        ax[0].legend()
        ax[0].grid(True)
        
        ax[1].plot(times, pressures, label="Pressure (Pa)", color="green")
        ax[1].set_xlabel("Time")
        ax[1].set_ylabel("Pressure (Pa)")
        ax[1].set_title("Temperature Over the Last 24 Hours")
        ax[1].legend()
        ax[1].grid(True)

        # Save plot to a BytesIO buffer
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        # Return the image as an HTTP response
        return HttpResponse(buffer, content_type="image/png")

    except RuntimeError as e:
        return HttpResponse(f"Error generating plot: {str(e)}", status=500)
    except Exception as e:
        return HttpResponse(f"Unexpected error: {str(e)}", status=500)

# Keep your existing views as they are
def get_temperature_data(request):
    try:
        tables = fetch_temperature_data()

        # Extract data points
        data = []
        for table in tables:
            for record in table.records:
                data.append({
                    "time": record.get_time(),
                    "value": record.get_value(),
                })

        return JsonResponse({"data": data}, safe=True)
    except RuntimeError as e:
        return JsonResponse({"error": str(e)}, status=500)

def temperature_data(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    try:
        tables = fetch_temperature_data()

        # Parse query results into a list of dictionaries
        data = []
        for table in tables:
            for record in table.records:
                data.append({
                    "timestamp": record.get_time(),
                    "temperature": record.get_value(),
                })

        # AJAX or regular request handling
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX request
            return JsonResponse({"readings": data})
        
        # Render HTML template for non-AJAX requests
        return render(request, 'temperature/temperature_list.html', {'readings': data, 'show_devices_header': False})

    except RuntimeError as e:
        return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})
    
def pressure_data(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    try:
        tables = fetch_pressure_data()

        # Parse query results into a list of dictionaries
        data = []
        for table in tables:
            for record in table.records:
                data.append({
                    "timestamp": record.get_time(),
                    "pressure": record.get_value(),
                })

        # AJAX or regular request handling
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX request
            return JsonResponse({"readings": data})
        
        # Render HTML template for non-AJAX requests
        return render(request, 'pressure/pressure_list.html', {'readings': data, 'show_devices_header': False})

    except RuntimeError as e:
        return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})

def get_pressure_data(request):
    try:
        tables = fetch_pressure_data()

        # Extract data points
        data = []
        for table in tables:
            for record in table.records:
                data.append({
                    "time": record.get_time(),
                    "value": record.get_value(),
                })

        return JsonResponse({"data": data}, safe=True)
    except RuntimeError as e:
        return JsonResponse({"error": str(e)}, status=500)