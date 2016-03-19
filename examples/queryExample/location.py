"""
Date created: 5.3.2016
Author: Jiri Burant

Module providing access to geopy library
"""

from geopy.geocoders import Nominatim

class GeoLocation:
    
    def getLocation(self,place):
        geolocator = Nominatim()
        location = geolocator.geocode(place)
        return location

