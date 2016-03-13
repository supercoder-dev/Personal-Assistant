"""
Date created: 5.3.2016
Author: Jiri Burant

First draft of the possible weather module package.
"""

from urllib.request import Request, urlopen, URLError
from geopy.geocoders import Nominatim

import json

#Class testing the access to the forecast.io weather API and parsing the incoming json.
class QueryControl:


    def __init__(self, latitude, longitude):
        self.apikey='2fe3789874bc830a8cf2b1d98c4d7dbb' #Free apikey for up to 1000 queries per day, registered to the author
        self.latitude=latitude
        self.longitude=longitude

    def callWeatherAPI(self):
        request = Request('https://api.forecast.io/forecast/'+ self.apikey + '/' + str(self.latitude) +',' + str(self.longitude))
        print('calledWeather api')
            
        try:
            response = urlopen(request)
            data = json.loads(response.readall().decode('utf-8'))
        except URLError:
            data='There was an error'
            print ('Error')
         
        return data

    def queryControl(self, query ):                 
        data=self.callWeatherAPI();

        querySwitcher = {
            'weather?': data['daily']['summary'],
            'temperature?': data['hourly']['data'][0]['temperature'],
            'sunset?': data['daily']['data'][0]['sunsetTime'],
        }

        if (query in querySwitcher):
            answer=querySwitcher[query]
        else:
            answer='query not recognised'
        
        return answer
