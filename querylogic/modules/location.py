"""
Date created: 5.3.2016
Author: Jiri Burant

Module providing access to geopy library
"""

from geopy.geocoders import Nominatim

def init_hook(args):
    return GeoLocation()
    
class GeoLocation:
    
    def getLocation(self,place):
        geolocator = Nominatim()
        location = geolocator.geocode(place)
        return location

    def query_resolution(self, intent, query, params):
        location=self.getLocation(params['town'])
        
        querySwitcher = {
            'locationSelf': location,
            'latitudeSelf': location.latitude,
            'longitudeSelf': location.longitude,
        }

        if (intent in querySwitcher.keys()):
            answer=querySwitcher[query]
        else:
            answer='query not recognised'

        return answer
