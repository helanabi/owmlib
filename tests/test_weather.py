import pytest
from unittest import mock
from owmforecast import weather

class TestWeatherGet:
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    required_args = {"lat": 44.34, "lon": 10.99, "appid": "API_KEY"}
    optional_args = {
        "mode": ["xml", "html"],
        "units": ["standard", "metric", "imperial"],
        "lang": ["ar"]
    }
    response_text = ("text", "SERVER RESPONSE")
    response_json = ("json", lambda: {"RESPONSE": "JSON"})

    def get_weather(self, **kwargs):
        return weather.get(self.required_args["lat"],
                           self.required_args["lon"],
                           self.required_args["appid"],
                           **kwargs)

    def args_tester(self, expected_response, **kwargs):
        with mock.patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            setattr(mock_get.return_value, *expected_response)
            returned_response = self.get_weather(**kwargs)

        mock_get.assert_called_once_with(
            self.endpoint,
            params={**self.required_args, **kwargs}
        )

        if callable(expected_response[1]):
            assert returned_response == expected_response[1]()
        else:
            assert returned_response == expected_response[1] 

    def test_required_args(self):
        self.args_tester(self.response_json)
            
    def test_optional_args(self):
        response = self.response_text

        for param in self.optional_args:
            if param == "mode":
                response = self.response_text
            else:
                response = self.response_json
                
            for value in self.optional_args[param]:
                self.args_tester(response, **{param: value})

    def test_combined_args(self):
        self.args_tester(self.response_text,
                         mode="html",
                         units="metric",
                         lang="Spanish")

    def test_invalid_kwarg(self):
        with pytest.raises(TypeError):
            self.get_weather(city="Tiflet")

    def test_invalid_value(self):
        for key, value in (("mode", "json"), ("units", "Celsius")):
            with pytest.raises(ValueError):
                self.get_weather(**{key: value})

    @mock.patch("requests.get") #, autospec=True)
    def test_bad_status(self, mock_get):
        mock_get.return_value.status_code = 400
        self.get_weather()
        mock_get.return_value.raise_for_status.assert_called()
