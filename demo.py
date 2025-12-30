import os
import dotenv
import owmlib as owm

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

# These are the same examples shown in OpenWeatherMap API docs
print(owm.weather(44.34, 10.99, API_KEY))
# print(owm.forecast(44.34, 10.99, API_KEY))
# print(owm.geo_direct("London", API_KEY, limit=5))
# print(owm.geo_zip("E14", API_KEY, country="GB"))
# print(owm.geo_reverse(51.5098, -0.1180, API_KEY, limit=5))
