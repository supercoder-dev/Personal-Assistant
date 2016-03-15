"""
Date created: 12.3.2016
Author: Jiri Burant

First draft of the possible weather module package.
"""

from urllib.request import Request, urlopen, URLError
from geopy.geocoders import Nominatim
import json
    

def getLocation(place):
    geolocator = Nominatim()
    location = geolocator.geocode(place)
    return location

def init_hook(args):
    if ('town' in args):
        location=getLocation(args['town'])
        return Weather(location.latitude,location.longitude)
    else:
        return 'Error'

class Weather:
    #keys serve as intent switch, based on them, the appropriate actions are taken
    keys=['weather','temperature','sunset'] 

    def __init__(self, latitude, longitude):
        self.apikey='2fe3789874bc830a8cf2b1d98c4d7dbb' #Free apikey for up to 1000 queries per day, registered to the author
        self.latitude=latitude
        self.longitude=longitude

    def call_weather_api(self, latitude=self.latitude, longitude=self.longitude):
        request = Request('https://api.forecast.io/forecast/'+ self.apikey + '/' + str(latitude) +',' + str(longitude))
        print('calledWeather api')
            
        try:
            response = urlopen(request)
            data = json.loads(response.readall().decode('utf-8'))
        except URLError:
            data='There was an error'
            print ('Error')
         
        return data

    def query_switcher(self, intent, query, data):
        values=[data['daily']['summary'],data['hourly']['data'][0]['temperature'],data['daily']['data'][0]['sunsetTime']]
        querySwitcher = dict(zip(self.keys,values))
        return querySwitcher[query]

    def query_resolution(self, intent, query, params ):    
        if (intent in self.keys):
            data=self.call_weather_api()
            answer=self.query_switcher(intent,query,data)
        else:
            answer='query not recognised'

        return answer
