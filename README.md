# Overview

Python client library for OpenWeatherMap current weather and forecasts API

## Description

This library wraps 3 end-points:
1. Current weather API
2. 3-hour forecast for 5 days API
3. Geocoding API: converts city names and zip codes to geo coordinates
   and vice-versa

## Requirements

- Python 3.9+

## Library API reference

- `owmforeca.weather(lat, lon, api_key, **kwargs)`
Access current weather data for any location

       - `lat`: latitude
       - `long`: longitude
       - `api_key`: OWM account API key
       - `mode`: Response format. Possible values are `xml` and `html`.
       	 If you don't use the mode parameter format is JSON by default.
       - `units`: Units of measurement. `standard`, `metric` and `imperial`
       	 units are available. If you do not use the units parameter, standard
	 units will be applied by default.
       - `lang`: You can use this parameter to get the output in your language.

## Attribution and disclaimer

This is not an official OWM software.
Documentation was adapted from openweathermap.org.
