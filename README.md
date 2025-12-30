# Overview

This library aims to be a thin, transparent wrapper around **OpenWeatherMap**
current weather, forecasts and geocoding APIs for **Python** programmers.

It avoids imposing additional constraints or defaults beyond those defined by
OWM itself. Parameters are passed through as-is most of the time, and validation
is delegated to the upstream service.

JSON responses are returned as parsed Python objects (`dict` or `list`),
depending on the upstream API.

## Quick Start

```python
import owmlib
api_key = "YOUR_API_KEY"

coordinates = owmlib.geo_direct("London", api_key)[0] # First match
latitude = coordinates["lat"]
longitude = coordinates["lon"]

data = owmlib.weather(latitude, longitude, api_key, units="metric")

print(data["weather"]["description"])
print(data["main"]["temp"])
```

## Requirements

- Python 3.9+

## Installation

```
git clone https://github.com/helanabi/owmlib

pip install owmlib
```

## Supported APIs

1. Current weather
2. 3-hour forecast for 5 days
3. Geocoding: converts city names/zip codes to geo coordinates and vice-versa

## Library API Reference

### Parameter Description

- `lat`: latitude
- `lon`: longitude
- `appid`: OWM account API key
- `mode`: `xml` | `html` --  Response format (JSON by default)
- `units`: `standard` | `metric` | `imperial` -- Units of measurement
(default: `standard`)
- `lang`: two-letter output language code (e.g. `ar` for Arabic)
- `cnt`: number of timestamps in the API response
- `city`: city name
- `state`: state code for US cities
- `country`: ISO 3166 country code
- `limit`: the number of matching locations (max: 5)
- `zip_code`: zip/post code

### `owmlib.weather(lat, lon, appid, **kwargs)`

Access current weather data for any location

#### Optional Keyword Arguments

- `mode`, `units`, `lang`

### `owmlib.forecast(lat, lon, appid, **kwargs)`

5-day forecast for any location with 3-hour step in JSON or XML format.

#### Optional Keyword Arguments

- `mode`, `units`, `lang`, `cnt`
> `forecast() does not support `html` mode

### `owmlib.geo_direct(city, appid, state='', country='', limit=None)`

Convert the specified name of a location or zip/post code into the exact
geographical coordinates

### `owmlib.geo_zip(zip_code, appid, country='')`

Get coordinates by zip/post code

### `owmlib.geo_reverse(lat, lon, appid, limit=None)`

Convert geographical coordinates to location names 

## Notes

- Missing parameters in API response means that corresponding weather phenomena
did not occur at the time of measurement.
- More information about accepted values, value interpretation and API response
fields can be found in the respective API documentation pages linked below.

## OpenWeatherMap Documentation Links

1. [Current weather](https://openweathermap.org/current)
2. [5 days forecast API](https://openweathermap.org/forecast5)
3. [Geocoding API](https://openweathermap.org/api/geocoding-api)

## Attribution and Disclaimer

This is not an official OWM software.
Documentation was adapted from openweathermap.org.

## License

This project is licensed under the MIT license.