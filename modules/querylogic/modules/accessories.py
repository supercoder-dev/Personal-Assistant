import json
import datetime
import os
#import modules.access_util.joke as joke
from urllib.request import Request, urlopen, URLError
from geopy.geocoders import Nominatim
import json
import html
import random
from tzwhere import tzwhere
from pytz import timezone, utc

#import modules.access_util.timer as timer 
def getLocation(place):
    geolocator = Nominatim()
    location = geolocator.geocode(place,timeout = 10)
    return location

def init_hook():
        access=Accessories()
        tz = tzwhere.tzwhere()
        location='Prague'
        homeloc=getLocation(location)
        tz = tzwhere.tzwhere()
        tz_name =tz.tzNameAt(homeloc.latitude,homeloc.longitude)
        timez = timezone(tz_name) 
        d = datetime.datetime.utcnow()
        d = timez.localize(d)
        access.set_init_parameters(homeloc.latitude,homeloc.longitude,d.utcoffset().seconds/3600)
        return access

class Accessories:

    def set_init_parameters(self,latitude, longitude,utcoffset = 0):
        self.latitude=latitude
        self.longitude=longitude
        self.utcoffset=round(utcoffset)

    def get_timeNow(self,query):
        dt=datetime.datetime.utcnow();
        dt=dt + datetime.timedelta(hours=self.utcoffset)
        return 'It is ' + dt.strftime('%I:%M %p') + '.'

    def get_dayInWeek(self,query):
        dt=query['entities']['datetime']
        timeZone = dt[-6:-3]
        utctime = dt[:-6]  # ignoring time zone
        d = datetime.datetime.strptime(utctime, "%Y-%m-%dT%H:%M:%S.%f")+ datetime.timedelta(hours=-int(timeZone))
        return 'The given day is ' + d.strftime('%A') + '.'

    def get_date(self,query):
        dt = query['entities']['datetime']
        return 'The date is: ' + dt.strftime('%d of %m %Y') + '.'

    def tell_joke(self,query):
        #return('No jokes now!!!')
        with open('./Personal-Assistant/modules/querylogic/jokes.json') as data_file:
            data = json.load(data_file)
        choise = round(len(data)*random.random());
        joke = data[choise]['joke']
        return joke

    switcher = {'timeNow' : get_timeNow,
                'dayInWeek': get_dayInWeek,
                'date' : get_date,
                'joke' : tell_joke
    }

    def call_switcher(self,query):
        if 'entities' in query and 'agenda_en' in query['entities']:
            key=query['entities']['agenda_en'][0]['value']
            return Accessories.switcher[key](self,query)
        else:
            return 'query not recognised'

    def query_resolution(self, intent, query, params):
        if intent == 'agenda':
            return self.call_switcher(query)
        else:
            return 'query not recognised'
