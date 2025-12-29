import requests

BASE_URL = "https://api.openweathermap.org"

def forecast(lat, lon, appid, **kwargs):
    return request_data("/forecast",
                        lat,
                        lon,
                        appid,
                        add_param=("cnt", ''),
                        **kwargs)

def weather(lat, lon, appid, **kwargs):
    return request_data("/weather",
                        lat,
                        lon,
                        appid,
                        add_param=("mode", "html"),
                        **kwargs)

def geo_direct(city, appid, state='', country='', limit=None):
    return request_geo("/direct", {
        "q": collate(city, state, country),
        "appid": appid,
        "limit": limit
    })

def geo_zip(zip_code, appid, country=''):
    return request_geo("/zip", {
        "zip": collate(zip_code, country),
        "appid": appid
    })

def geo_reverse(lat, lon, appid, limit=None):
   return request_geo("/reverse", {
       "lat": lat,
       "lon": lon,
       "appid": appid,
       "limit": limit
   })

def request_geo(path, query):
    if query["limit"]:
        try:
            query["limit"] = int(limit)
        except ValueError:
            raise ValueError(
                f"invalid integer value for parameter limit: {limit}"
            )
    else:
         query.pop("limit", '')

    return make_request("/geo/1.0" + path, query)

def request_data(path, lat, lon, appid, add_param=(), **kwargs):
    """Make an HTTP call to the specified PATH with the given parameters

    `add_param` (tuple) of the form (name, value)
    """
    endpoint = BASE_URL + "/data/2.5" + path
    query = {
        "lat" : lat,
        "lon" : lon,
        "appid" : appid
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

    if not set(kwargs) <= set(params):
        raise TypeError("Invalid keyword arguments for weather(): "
                        + str(set(kwargs) - set(params)))
    
    for arg in kwargs:
        if not params[arg] or kwargs[arg] in params[arg]:
            query[arg] = kwargs[arg]
        else:
            raise ValueError(
                f"Invalid value for parameter {arg}: {kwargs[arg]}")

    return make_request("/data/2.5" + path, query, query.get("mode"))

def make_request(path, query, return_text=False):
    response = requests.get(BASE_URL + path, params=query)
    if response.status_code == 200:
        if return_text:
            return response.text
        else:
            return response.json()
    else:
        response.raise_for_status()

def collate(*args):
    return ','.join(str(arg) for arg in args if arg)
