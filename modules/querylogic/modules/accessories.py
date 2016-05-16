import json
import datetime
import os
#import modules.access_util.joke as joke
from urllib.request import Request, urlopen, URLError
import json
import html
import random

#import modules.access_util.timer as timer

def init_hook():
    access=Accessories()
    return access

class Accessories:

    def get_timeNow(self,query):
        dt=datetime.datetime.utcnow();
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

    def query_resolution(self, intent, query, params):
        if intent == 'agenda':
            return self.call_switcher(query)
        else:
            return 'query not recognised'
