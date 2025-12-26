import pytest
from unittest import mock
from owmforecast import weather

class TestWeatherGet:
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    req_args = {"lat": 44.34, "lon": 10.99, "appid": "API_KEY"}
    params = {
        "mode": ["xml", "html"],
        "units": ["standard", "metric", "imperial"],
        "lang": []
    }

    def get_weather(self, **kwargs):
        return weather.get(self.req_args["lat"],
                           self.req_args["lon"],
                           self.req_args["appid"],
                           **kwargs)

    def args_tester(self, mock_get, response, **kwargs):
        mock_get.return_value.status_code = 200
        mock_get.return_value.__setattr__(*response)
        srv_response = self.get_weather(**kwargs)
        mock_get.assert_called_with(self.endpoint,
                                    params={**self.req_args, **kwargs})

        if isinstance(response[1], str):
            assert srv_response == response[1]
        else:
            assert srv_response == response[1]()

    def required_args_tester(self, mock_get):
        self.args_tester(mock_get, ("json", lambda: {"response": "json"}))
            
    def opt_args_tester(self, mock_get):
        text = ("text", "SERVER RESPONSE")
        json = ("json", lambda: {"RESPONSE": "JSON"})
        response = text
        
        for param in self.params:
            if param == "mode":
                response = text
            else:
                response = json
                
            for value in self.params[param]:
                self.args_tester(mock_get, response, **{param: value})

        self.args_tester(mock_get, json, lang="Arabic")
        self.args_tester(mock_get,
                         text,
                         mode="html",
                         units="metric",
                         lang="Spanish")

    def invalid_kwarg_tester(self, mock_get):
        with pytest.raises(TypeError):
            self.get_weather(city="Tiflet")

    def invalid_value_tester(self, mock_get):
        for key, value in (("mode", "json"), ("units", "Celsius")):
            with pytest.raises(ValueError):
                self.get_weather(**{key: value})

    def bad_status_tester(self, mock_get):
        mock_get.return_value.status_code = 400
        self.get_weather()
        mock_get.return_value.raise_for_status.assert_called()

    def test_all(self):
        tests = [
            self.required_args_tester,
            self.opt_args_tester,
            self.invalid_kwarg_tester,
            self.invalid_value_tester,
            self.bad_status_tester
        ]
        
        for test in tests:
            with mock.patch("requests.get") as mock_get:
                test(mock_get)
