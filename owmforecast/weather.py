import requests

API_URL = "https://api.openweathermap.org/data/2.5"

def get(lat, lon, api_key, **kwargs):
    endpoint = API_URL + "/weather"
    query = {
        "lat" : lat,
        "lon" : lon,
        "appid" : api_key
        }

    params = {
        "mode": ["xml", "html"],
        "units": ["standard", "metric", "imperial"],
        "lang": []
        }

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

