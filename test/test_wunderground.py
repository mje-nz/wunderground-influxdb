"""Unit tests for Wunderground client.

Author: Matthew Edwards
Date: December 2016.
"""


import json
from nose.tools import assert_equal

from main import WundergroundConditions


# This is the response to
# http://api.wunderground.com/api/0128b0bd28f3c15b/conditions/q/NZCH.json
wunderground_conditions_response = json.loads('''
{
  "response": {
  "version":"0.1",
  "termsofService":"http://www.wunderground.com/weather/api/d/terms.html",
  "features": {
  "conditions": 1
  }
    }
  ,	"current_observation": {
        "image": {
        "url":"http://icons.wxug.com/graphics/wu2/logo_130x80.png",
        "title":"Weather Underground",
        "link":"http://www.wunderground.com"
        },
        "display_location": {
        "full":"Christchurch International, New Zealand",
        "city":"Christchurch International",
        "state":"",
        "state_name":"New Zealand",
        "country":"NZ",
        "country_iso3166":"NZ",
        "zip":"00000",
        "magic":"105",
        "wmo":"93781",
        "latitude":"-43.48944473",
        "longitude":"172.53443909",
        "elevation":"37.0"
        },
        "observation_location": {
        "full":"Christchurch, ",
        "city":"Christchurch",
        "state":"",
        "country":"NZ",
        "country_iso3166":"NZ",
        "latitude":"-43.48333359",
        "longitude":"172.55000305",
        "elevation":"125 ft"
        },
        "estimated": {
        },
        "station_id":"NZCH",
        "observation_time":"Last Updated on December 23, 1:30 PM NZDT",
        "observation_time_rfc822":"Fri, 23 Dec 2016 13:30:00 +1300",
        "observation_epoch":"1482453000",
        "local_time_rfc822":"Fri, 23 Dec 2016 13:58:42 +1300",
        "local_epoch":"1482454722",
        "local_tz_short":"NZDT",
        "local_tz_long":"Pacific/Auckland",
        "local_tz_offset":"+1300",
        "weather":"Rain",
        "temperature_string":"54 F (12 C)",
        "temp_f":54,
        "temp_c":12,
        "relative_humidity":"88%",
        "wind_string":"From the SW at 6 MPH",
        "wind_dir":"SW",
        "wind_degrees":230,
        "wind_mph":6,
        "wind_gust_mph":0,
        "wind_kph":9,
        "wind_gust_kph":0,
        "pressure_mb":"1006",
        "pressure_in":"29.71",
        "pressure_trend":"0",
        "dewpoint_string":"50 F (10 C)",
        "dewpoint_f":50,
        "dewpoint_c":10,
        "heat_index_string":"NA",
        "heat_index_f":"NA",
        "heat_index_c":"NA",
        "windchill_string":"NA",
        "windchill_f":"NA",
        "windchill_c":"NA",
        "feelslike_string":"54 F (12 C)",
        "feelslike_f":"54",
        "feelslike_c":"12",
        "visibility_mi":"6.2",
        "visibility_km":"10.0",
        "solarradiation":"--",
        "UV":"3","precip_1hr_string":"-9999.00 in (-9999.00 mm)",
        "precip_1hr_in":"-9999.00",
        "precip_1hr_metric":"--",
        "precip_today_string":"0.00 in (0.0 mm)",
        "precip_today_in":"0.00",
        "precip_today_metric":"0.0",
        "icon":"rain",
        "icon_url":"http://icons.wxug.com/i/c/k/rain.gif",
        "forecast_url":"http://www.wunderground.com/global/stations/93781.html",
        "history_url":"http://www.wunderground.com/history/airport/NZCH/2016/12/23/DailyHistory.html",
        "ob_url":"http://www.wunderground.com/cgi-bin/findweather/getForecast?query=-43.48333359,172.55000305",
        "nowcast":""
    }
}''')


def test_wunderground_conditions_time():
    cond = WundergroundConditions('NZCH', wunderground_conditions_response)
    assert_equal(cond.observation_time.isoformat(), '2016-12-23T00:30:00')


def test_wunderground_conditions_temperature():
    cond = WundergroundConditions('NZCH', wunderground_conditions_response)
    assert_equal(cond.temperature, 12)


def test_wunderground_conditions_humidity():
    cond = WundergroundConditions('NZCH', wunderground_conditions_response)
    assert_equal(cond.relative_humidity, 88)


def test_wunderground_conditions_dewpoint():
    cond = WundergroundConditions('NZCH', wunderground_conditions_response)
    assert_equal(cond.dewpoint, 10)


def test_wunderground_conditions_pressure():
    cond = WundergroundConditions('NZCH', wunderground_conditions_response)
    assert_equal(cond.pressure, 1006)

