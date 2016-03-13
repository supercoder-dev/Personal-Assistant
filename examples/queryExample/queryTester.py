"""
Date created: 5.3.2016
Author: Jiri Burant

Script testing the weather api and geolocation library
"""

from weather import QueryControl
from location import GeoLocation

geoLoc=GeoLocation()
location=geoLoc.getLocation('Prague')


while True:
    query=input("Enter query: ");

    qc=QueryControl(location.latitude,location.longitude)
    answer=qc.queryControl(query)
    print(answer);
