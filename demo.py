import os
import dotenv
import core

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

# These are the same examples shown in OpenWeatherMap API docs
core.weather(44.34, 10.99, API_KEY)
# core.forecast(44.34, 10.99, API_KEY)
# core.geo_direct("London", API_KEY, limit=5)
# core.geo_zip("E14", API_KEY, country="GB")
# core.geo_reverse(51.5098, -0.1180, API_KEY, limit=5)
