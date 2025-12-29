import requests
import util

# HOSTNAME = ""
API_URL = "https://api.openweathermap.org/data/2.5"
DATA_URL = "https://api.openweathermap.org/data/2.5"
GEO_URL = "https://api.openweathermap.org/geo/1.0"

def forecast(lat, lon, api_key, **kwargs):
    return request_data("/forecast",
                        lat,
                        lon,
                        api_key,
                        add_param=("cnt", ''),
                        **kwargs)

def weather(lat, lon, api_key, **kwargs):
    return request_data("/weather",
                        lat,
                        lon,
                        api_key,
                        add_param=("mode", "html"),
                        **kwargs)

def geo_direct(city, appid, state='', country='', limit=None):
    query = {
        "q": util.collate(city, state, country),
        "appid": appid
    }

    if limit:
        try:
            query["limit"] = int(limit)
        except ValueError:
            raise ValueError(
                f"invalid integer value for parameter limit: {limit}"
            )

    return request_geo("/direct", query)

def geo_zip(zip_code, appid, country=''):
    return request_geo("/zip", {
        "zip": util.collate(zip_code, country),
        "appid": appid
    })

def geo_reverse():
    pass

def request_geo(path, query):
    response = requests.get(GEO_URL + path, params=query)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def request_data(path, lat, lon, api_key, add_param=(), **kwargs):
    """Make an HTTP call to the specified PATH with the given parameters

    `add_param` (tuple) of the form (name, value)
    """
    endpoint = API_URL + path
    query = {
        "lat" : lat,
        "lon" : lon,
        "appid" : api_key
        }

    params = {
        "mode": ["xml"],
        "units": ["standard", "metric", "imperial"],
        "lang": []
        }

    if add_param:
        param, value = add_param
        if param in params:
            params[param].append(value)
        else:
            params[param] = [value] if value else []

    if not set(kwargs.keys()) <= set(params.keys()):
        raise TypeError("Invalid keyword arguments for weather(): " +
                        str(set(kwargs.keys()) - set(params.keys())))
    
    for arg in kwargs.keys():
        if not params[arg] or kwargs[arg] in params[arg]:
            query[arg] = kwargs[arg]
        else:
            raise ValueError(
                f"Invalid value for parameter {arg}: {kwargs[arg]}")

    response = requests.get(endpoint, params=query)

    if response.status_code == 200:
        if query.get("mode"):
            return response.text
        else:
            return response.json()
    else:
        response.raise_for_status()
