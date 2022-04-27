import os
import requests as req

class Weather:
    def __init__(self, latitude, longitude) -> None:
        self.api_key = os.getenv('ACCU_API_KEY')
        self.latitude = latitude
        self.longitude = longitude
        self.location_id = '240499'
        # Hardcoded location_id for now to avoid requesting everytime a Weather object is created
        #self.__create_location_id()

    def get_1day_data(self):
        url_request = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{self.location_id}?apikey={self.api_key}&details=true&metric=true'
        response = req.get(url_request)
        return response.json()

    def get_1hour_data(self):
        url_request = f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{self.location_id}?apikey={self.api_key}&details=true&metric=true'
        response = req.get(url_request)
        return response.json()

    def get_12hours_data(self):
        url_request = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{self.location_id}?apikey={self.api_key}&details=true&metric=true'
        response = req.get(url_request)
        return response.json()

    def __create_location_id(self):
        url_request = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={self.api_key}&q={self.latitude}%2C{self.longitude}'
        response = req.get(url_request)
        data = response.json()
        self.location_id = data["Key"]
