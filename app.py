import os
import requests
import json
from influxdb import InfluxDBClient
from datetime import datetime, timezone

def record_weather(api_key, latitude, longitude, fields_to_record, influx_client):
    """
    Retrieves the current weather conditions from the OpenWeather API, location from OpenStreetMap API and
    writes the selected fields to an InfluxDB database.
    """
    try:
        # make the weather API request
        weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
        weather_response = requests.get(weather_api_url)
        weather_data = weather_response.json()

        # make the location API request
        osm_api_url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&zoom=8"
        location_response = requests.get(osm_api_url)
        location_data = location_response.json()

        #Create the database if doesn't exist
        #influx_client.create_database(influxdbname)

        # create the InfluxDB record
        record = {
            "measurement": "weathernow",
            "tags": {
                "location": location_data['address']['county'],
                "country": location_data['address']['country']
            },
            "fields": {}
        }

        # add the selected fields to the record
        for field in fields_to_record:
            if field == 'temperature':
                record['fields']['temperature'] = weather_data['main']['temp']
            elif field == 'weather_description':
                record['fields']['weather_description'] = weather_data['weather'][0]['description']
            elif field == 'sunrise':
                record['fields']['sunrise'] = weather_data['sys']['sunrise']
            elif field == 'sunset':
                record['fields']['sunset'] = weather_data['sys']['sunset']
            elif field == 'pressure':
                record['fields']['pressure'] = weather_data['main']['pressure']

        # the print lines here only during development and replaced by the commented client writes when done
        #print(weather_data, '\n')
        #print(location_data, '\n')
        print(record)
        
        # write the record to InfluxDB
        #influx_client.write_points([record])
        print(f"Measurement taken at {datetime.now().isoformat(timespec='seconds')}", '\n')
    
    # check for errors
    except requests.exceptions.RequestException as e:
        print(f"Error while connecting: {e} at {datetime.now().isoformat(timespec='seconds')}")
    except InfluxDBClient as e:
        print(f"Error while connecting: {e} at {datetime.now().isoformat(timespec='seconds')}")
    except Exception as e:
        print(f"An error occurred: {e} at {datetime.now().isoformat(timespec='seconds')}")

if __name__ == '__main__':
    # retrieve the API key and location from the environment variables
    api_key = os.environ['OPENWEATHER_API_KEY']
    latitude = os.environ['LATITUDE']
    longitude = os.environ['LONGITUDE']
    influxdbhost = os.environ['INFLUXDBHOST']
    influxdbuser = os.environ['INFLUXDBUSER']
    influxdbpwd = os.environ['INFLUXDBPWD']
    influxdbname = os.environ['INFLUXDBNAME']

    # create a list of the fields to record in the database
    # the default is to record all fields
    fields_to_record = ['temperature', 'weather_description', 'sunrise', 'sunset', 'pressure']

    # check if the user has specified a list of fields to record
    if 'FIELDS_TO_RECORD' in os.environ:
        fields_to_record = os.environ['FIELDS_TO_RECORD'].split(',')

    # create an InfluxDB client
    influx_client = InfluxDBClient(influxdbhost, 8086, influxdbuser, influxdbpwd, influxdbname)

    # retrieve the current weather conditions and write them to the database
    record_weather(api_key, latitude, longitude, fields_to_record, influx_client)