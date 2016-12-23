"""Minimal Wunderground API library.

Author: Matthew Edwards
Date: December 2016
"""


import datetime
import requests


class WundergroundConditions(object):

    def __init__(self, json_response):
        self.json_response = json_response

    @property
    def _current_observation(self):
        return self.json_response['current_observation']

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
        return 'WundergroundConditions at %s: temperature=%s, dewpoint=%s, humidity=%s, pressure=%s' \
            % (self.observation_time.isoformat(), self.temperature, self.dewpoint,
               self.relative_humidity, self.pressure)


def fetch_conditions(api_key, station):
    response = requests.get("http://api.wunderground.com/api/%s/conditions/q/%s.json" % (api_key, station))
    return WundergroundConditions(response.json())

