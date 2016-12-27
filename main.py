"""Simple script while pulls the current conditions for a location from Weather Underground and
pushes the temperature, dewpoint, relative humidity and pressure to an InfluxDB database.

Author: Matthew Edwards
Date: December 2016
"""


import datetime
import argparse

import requests
import influxdb


class WundergroundConditions(object):

    def __init__(self, station_name, json_response):
        self.station_name = station_name
        self.response_json = json_response

    @property
    def _current_observation(self):
        return self.response_json['current_observation']

    @property
    def observation_time(self):
        """Time of observation (UTC)."""
        epoch = float(self._current_observation['observation_epoch'])
        return datetime.datetime.utcfromtimestamp(epoch)

    @property
    def temperature(self):
        """Measured temperature in Celsius."""
        return float(self._current_observation['temp_c'])

    @property
    def dewpoint(self):
        """Measured dewpoint in Celsius."""
        return float(self._current_observation['dewpoint_c'])

    @property
    def relative_humidity(self):
        """Measured relative humidity (percent)."""
        humidity_string = self._current_observation['relative_humidity']
        return float(humidity_string.strip('%'))

    @property
    def pressure(self):
        """Measured pressure in mbar."""
        return float(self._current_observation['pressure_mb'])

    def __str__(self):
        return 'WundergroundConditions for %s at %s: temperature=%s, dewpoint=%s, humidity=%s, pressure=%s' \
            % (self.station_name, self.observation_time.isoformat(),
               self.temperature, self.dewpoint, self.relative_humidity, self.pressure)


def fetch_conditions_from_wunderground(api_key, station_name):
    response = requests.get("http://api.wunderground.com/api/%s/conditions/q/%s.json" % (api_key, station_name))
    if response.status_code != 200:
        print('WARNING: got status code', response.status_code)
        print(response.json())
    return WundergroundConditions(station_name, response.json())


def write_conditions_to_influxdb(conditions, client):
    data = [
        {
            'measurement': 'climate',
            'tags': {
                'source': 'wunderground',
                'station': conditions.station_name
            },
            'time': conditions.observation_time.isoformat(),
            'fields': {
                'temperature': conditions.temperature,
                'dewpoint': conditions.dewpoint,
                'relative_humidity': conditions.relative_humidity,
                'pressure': conditions.pressure
            }
        }
    ]
    success = client.write_points(data, time_precision='s')
    if not success:
        raise RuntimeError('Could not write conditions to database')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', required=True, dest='api_key',
                        help='Weather Underground API key')
    parser.add_argument('-o', '--host', default='localhost', metavar='HOSTNAME',
                        help='InfluxDB hostname', dest='influxdb_hostname')
    parser.add_argument('-b', '--database', default='weather', metavar='DATABASE',
                        help='InfluxDB database', dest='influxdb_database')
    parser.add_argument('-s', '--station', required=True, action='append', dest='station_names',
                        help='Weather Underground station ID or location search')
    args = parser.parse_args()

    for station_name in args.station_names:
        conditions = fetch_conditions_from_wunderground(args.api_key, station_name)
        print('Got %s' % conditions)
        age = datetime.datetime.utcnow() - conditions.observation_time
        if age > datetime.timedelta(minutes=30):
            rounded_age = datetime.timedelta(seconds=int(age.total_seconds()))
            print('WARNING: measurement is %s old' % rounded_age)
        client = influxdb.InfluxDBClient(host=args.influxdb_hostname, database=args.influxdb_database)
        write_conditions_to_influxdb(conditions, client)
        print('Written to %s on %s' % (args.influxdb_database, args.influxdb_hostname))


if __name__ == '__main__':
    main()
