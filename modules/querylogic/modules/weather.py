"""
Date created: 12.3.2016
Author: Jiri Burant

First draft of the possible weather module package.
"""

#TODO: Get the forecast for next week,
#      Be able to get the weather from past
#      Select time period: Currently, Daily, Hourly


from urllib.request import Request, urlopen, URLError
from geopy.geocoders import Nominatim
import json
import datetime
import time as tm
    


def getLocation(place):
    geolocator = Nominatim()
    location = geolocator.geocode(place)
    return location

#init_hook initializes the class Weather
def init_hook():
        weather=Weather()
        location=getLocation('Prague');
        
        weather.set_init_parameters(location.latitude,location.longitude)
        return weather

class Weather:

    def set_init_parameters(self,latitude, longitude):
        self.apikey='2fe3789874bc830a8cf2b1d98c4d7dbb' #Free apikey for up to 1000 queries per day, registered to the author
        self.latitude=latitude
        self.longitude=longitude

    def call_weather_api(self, latitude, longitude, time='now'):
        if time == 'now':
            request = Request('https://api.forecast.io/forecast/'+ self.apikey + '/' + str(latitude) +',' + str(longitude) + '?units=si')
        else:
            request = Request('https://api.forecast.io/forecast/'+ self.apikey + '/' + str(latitude) +',' + str(longitude) + ',' + str(time) + '?units=si')
            
        print('calledWeather api')
            
        try:
            response = urlopen(request)
            data = json.loads(response.readall().decode('utf-8'))
        except URLError:
            data='There was an error'
            print ('Error')
         
        return data

    def calculate_time_offset(time):
        diff = time - datetime.utcnow()
        daysOffset = diff.TotalDays
        hoursOffset = diff.TotalHours

        return {'dOffset': daysOffset, 'hOffset': hoursOffset}

    #get_simplesentence returns the answer string, currently very simple
    def get_simplesentence(self,answer,subject):
        return 'The ' + str(subject) + str(answer) + '.'

    #again, very simple sentence
    def get_typeofprecipsentence(self,answer,verb):
        return 'It is ' + str(answer) + 'ing' + 'outside.'

    #append the info about the location to the answer.
    def answersentence_add_location(self,answersentence,location):
        return answersentence+' in ' + location

    def convert_time(self, posixtime):
        return datetime.datetime.fromtimestamp(int(posixtime)).strftime('%Y-%m-%d %H:%M:%S')

    def convertUTCtoUNIXtime(self,utctime):
        utctime=utctime[:-6] #ignoring tme zone 
        d = datetime.datetime.strptime( utctime, "%Y-%m-%dT%H:%M:%S.%f" )
        return int(tm.mktime(d.timetuple()))

    def get_summary(self,data,timeperiod='daily'):
        answer=data[timeperiod]['data'][0]['summary']
        return self.get_simplesentence(answer,'forecast says ')  

    def get_temperature(self,data,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['temperature']
            return self.get_simplesentence(answer,'temperature is ')  
        else:
            answer=data[timeperiod]['data'][0]['temperature']
            return self.get_simplesentence(answer,'temperature will be ')  
       
    def get_sunrise(self,data,timeperiod='daily'):
        time=self.convert_time(data[timeperiod]['data'][0]['sunriseTime']) 
        return self.get_simplesentence(time,'time of sunrise is ')  

    def get_sunset(self,data,timeperiod='daily'):
        time=self.convert_time(data[timeperiod]['data'][0]['sunsetTime'])
        return self.get_simplesentence(time,'time of sunset is ')
    
    def get_precip_intensity(self,data,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['data'][0]['precipIntensity']
            return self.get_simplesentence(answer,'intensity of the precipations is ')
        else:
            answer=data[timeperiod]['data'][0]['precipIntensity']
            return self.get_simplesentence(answer,'intensity of the precipations will be ')

    def get_humidity(self,data,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['data'][0]['humidity']
            return self.get_simplesentence(answer,'humidity is ')
        else:
            answer=data[timeperiod]['data'][0]['humidity']
            return self.get_simplesentence(answer,'humidity will be ')

    def get_windspeed(self,data,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['windSpeed']
            return self.get_simplesentence(answer,'speed of wind is ')
        else:
            answer=data[timeperiod]['data'][0]['windSpeed']
            return self.get_simplesentence(answer,'speed of wind will be ')

    def get_moonphase(self,data,timeperiod='daily'):
        phase=data['daily']['data'][0]['moonPhase']

        if(phase==0):
            answer='new moon'
        elif(phase==0.5):
            answer='full moon'
        elif(phase==0.25):
            answer='first quarter'
        elif(phase==0.75):
            answer='last quarter'
        elif(phase<0.25):
            answer='waxing crescent'
        elif(phase>0.25 and phase<0.5):
            answer='waxing gibbous'
        elif(phase>0.5 and phase<0.75):
            answer='wanning gibbous'
        elif(phase>0.75 and phase<1):
            answer='wanning crescent'

        return self.get_simplesentence(answer,'moon phase is ')

    def get_temperatureMin(self,data,timeperiod='daily'):
        answer = data[timeperiod]['data'][0]['temperatureMin']
        return self.get_simplesentence(answer,'minimum temperature will be ')

    def get_temperatureMax(self,data,timeperiod='daily'):
        answer=data[timeperiod]['data'][0]['temperatureMax']
        return self.get_simplesentence(answer,'maximum temperature will be ')

    def get_visibility(self, data,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['visibility']
            return self.get_simplesentence(answer,'visibility is ')
        else:
            answer=data[timeperiod]['data'][0]['visibility']
            return self.get_simplesentence(answer,'visibility will be ')

    def get_pressure(self, data,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['pressure']
            return self.get_simplesentence(answer,'pressure is ')
        else:
            answer=data[timeperiod]['data'][0]['pressure']
            return self.get_simplesentence(answer,'pressure will be ')

    def get_snow(self, data,timeperiod='currently'):
        if(timeperiod=='currently'):
            if('precipType' in data[timeperiod]['data'][0]):
                answer=data[timeperiod]['data'][0]['precipType']
                return self.get_typeofprecipsentence(answer,'')
            else:
                return 'Currently, there are no precipitations at the location.'
        else:
            return 'I dont know'

    #call_switcher indexes to the dictionary with key, calling the appropriate function. Firstly, it tries the call with the default timeperiod,
    #if this fails it tries it with other timeperiods.
    def call_switcher(self, key, data):
        try:
            answer=Weather.switcher[key](self,data)
        except:
            try:
                answer=Weather.switcher[key](self,data,'hourly')
            except:
                try:
                    answer=Weather.switcher[key](self,data,'daily')
                except:
                    answer='I could not receive the information'

        return answer
        
    
    #switcher serves as an intent switch, based on the intent, the appropriate actions are taken. The intents might change in the future
    switcher={'weather' : get_summary,
              'temperature': get_temperature,
              'sunrise': get_sunrise,
              'sunset': get_sunset,
              'precip':get_precip_intensity,
              'humidity':get_humidity,
              'windspeed':get_windspeed,
              'pressure':get_pressure,
              'moonphase':get_moonphase,
              'temperaturemin':get_temperatureMin,
              'temperaturemax':get_temperatureMax,
              'visibility':get_visibility,
              'snow':get_snow,
              }
        
    #Called from the query logic
    def query_resolution(self, intent, query, params):
        if 'city' in params:
            location=getLocation(params['city'])
            self.set_init_parameters(location.latitude,location.longitude)

        time='now'
        
        if intent == 'weather':
            if 'entities' in query:
                if'datetime' in query['entities']:  #If datetime is present in the query, take it into account
                    if'interval' in query['entities']['datetime'][0]['type']:  #In case of interval, take the beginning
                        time=self.convertUTCtoUNIXtime(query['entities']['datetime'][0]['from']['value'])
                        timeOffset=calculate_time_offset(time)

                        if timeOffset['hours']>48 & timeOffset['days']<7:
                            offset=timeOffset['days']
                            timeperiod=daily

                        else:
                            if timeOffset['hours']<48:
                                offset = timeOffset['hours']
                                timeperiod=hourly


                if 'location' in query['entities']:    #If location is present in the query, take it into account
                    location=query['entities']['location'][0]['value']
                    coordinates=getLocation(location)
                    
                    data=self.call_weather_api(coordinates.latitude,coordinates.longitude,time)
                else:
                    data=self.call_weather_api(self.latitude,self.longitude,time)    #Use the default coordinates
            else:
                data=self.call_weather_api(self.latitude,self.longitude,time)    #Use the default coordinates    
           
            if ('entities' in query) & ('weather_type' in query['entities']):
                if query['entities']['weather_type'][0]['value'] in self.switcher.keys():
                    weather_type = query['entities']['weather_type'][0]['value']
                    if'value_size' in query['entities']:
                        if weather_type + query['entities']['value_size'][0]['value'] in self.switcher.keys():
                            answersentence=Weather.call_switcher(self, weather_type + query['entities']['value_size'][0]['value'],data)
                    else:
                        answersentence=Weather.call_switcher(self,weather_type,data)
                else:
                    answersentence=Weather.call_switcher(self,intent,data)
            else:
                answersentence=Weather.call_switcher(self,intent,data)
             
            answersentence=self.answersentence_add_location(answersentence,location)
        
            return answersentence

        else:
            answersentence='query not recognised'
            return answersentence

