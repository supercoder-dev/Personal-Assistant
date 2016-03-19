"""
Date created: 5.3.2016
Author: Jiri Burant

Script testing the weather api and geolocation library
"""
import yaml
from weather import QueryControl
from location import GeoLocation

config = yaml.safe_load(open('config.yml'))

name=config['user']['name']
mail=config['user']['mail']
town=config['location']['town']
country=config['location']['country']

geoLoc=GeoLocation()
location=geoLoc.getLocation(town)

while True:
    query=input('Enter query: ');

    qc=QueryControl(location.latitude,location.longitude)
    answer=qc.queryControl(query)
    print(answer)
