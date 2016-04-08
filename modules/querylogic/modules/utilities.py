import json
import datetime
import os


def init_hook():
        weather=Weather()
        location='Prague'
        homelocation=getLocation(location);
        weather.set_init_parameters(homelocation.latitude,homelocation.longitude)
        return weather

class Utilities:

   # switcher={'time' : get_summary,
    #          }
#def call_switcher(self, key, data, timeperiod, offset):

def query_resolution(self, intent, query, params):
    if intent == 'timer':
        modules.timer.run(6)
