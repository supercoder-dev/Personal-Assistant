"""
Date created: 12.3.2016
Author: Jiri Burant, Jakub Drapela

First demo of the weather module package.
"""

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
        location='Prague'
        homelocation=getLocation(location);
        weather.set_init_parameters(homelocation.latitude,homelocation.longitude)
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
        diff = time - datetime.datetime.utcnow()
        daysOffset = diff.days

        try:
            hoursOffset = diff.days*24+int(diff.seconds/3600)
            if hoursOffset>daysOffset*24:
                daysOffset=daysOffset+1
        except:
            hoursOffset = diff.days*24

        return {'days': daysOffset, 'hours': hoursOffset}

    def get_timeperiod_offset(timeIn,grain):
        t= timeIn[:-6] #Ignore timezone
        utc = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.000')
        timeOffset=Weather.calculate_time_offset(utc)

        if ((grain == 'day') | (int(timeOffset['hours'])>48)) and int(timeOffset['days'])<7 :
            offset=timeOffset['days']
            timeperiod='daily'
            return {'offset':offset,'timeperiod':timeperiod}
        else:
            if int(timeOffset['hours'])<48 and grain=='hour':
                offset = timeOffset['hours']
                timeperiod='hourly'
                return {'offset':offset,'timeperiod':timeperiod}
            else:
                return 'Not supp'
                
    #get_simplesentence returns the answer string, currently very simple
    def get_simplesentence(self,answer,subject,units=''):
        return 'The ' + str(subject) + str(answer) + ' ' +str(units) + '.'

    #again, very simple sentence
    def get_typeofprecipsentence(self,answer,verb):
        return 'It is ' + str(answer) + 'ing' + 'outside.'

    def answer_polish(self,answersentence,location):
        if self.check_answer(answersentence):
            return self.answersentence_add_location(answersentence,location)
        else:
            return answersentence
    def check_answer(self,answersentence):
        if (answersentence!='Not supp') and answersentence!='' and answersentence!='I could not receive the information':
            return True
        else:
            return False

    #append the info about the location to the answer.
    def answersentence_add_location(self,answersentence,location):
        if not(location is None) and location != '' and not(answersentence is None):
            return answersentence[:-1] + ' in ' + location + '.'
        else:
            return answersentence
  
    def degreesToWorldSide(self,degrees):
        if(degrees<22.5):
            return 'North'
        if(degrees<67.5):
            return 'North-East'
        if(degrees<112.5):
            return 'East'
        if(degrees<157.5):
            return 'South-East'
        if(degrees<202.5):
            return 'South'
        if(degrees<247.5):
            return 'South-West'
        if(degrees<292.5):
            return 'West'
        if(degrees<337.5):
            return 'North-West'
        return 'North'

    def precipQuantity(self,precipIntensity):
        k = 2.54
        if(0.002*k<precipIntensity):
            return 'no precipitation'
        if(0.017*k<precipIntensity):
            return 'very light'
        if(0.1*k<precipIntensity):
            return 'ligth'
        if(0.4*k<precipIntensity):
            return 'moderate'
        return 'heavy'

    def convert_time(posixtime):
        return datetime.datetime.fromtimestamp(int(posixtime)).strftime('%Y-%m-%d %H:%M:%S')

    def convertUTCtoUNIXtime(utctime):
        utctime=utctime[:-6] #ignoring tme zone 
        d = datetime.datetime.strptime( utctime, "%Y-%m-%dT%H:%M:%S.%f" )
        return int(tm.mktime(d.timetuple()))

    def get_summary(self,data,entity,offset,timeperiod='daily'):
        answer=data[timeperiod]['data'][offset]['summary']
        return self.get_simplesentence(answer,'forecast says ')  

    def get_specialforecast(self,data,entity,offset,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['data'][offset][entity['value']]
            return self.get_simplesentence(answer,'The '+ entity['name'] +' is ', entity['units'])  
        else:
            answer=data[timeperiod]['data'][offset][entity['value']]
            return self.get_simplesentence(answer,'The '+ entity['name'] +' will be ', entity['units'])  

    def get_sunTime(self,data,entity,offset,timeperiod='daily'):
        time=Weather.convert_time(data[timeperiod]['data'][offset][entity['value']]) 
        return self.get_simplesentence(time,'The '+ entity['name'] +' is ')  
                   
    def get_windspeed(self,data,entity,offset,timeperiod='currently'):
        units = 'meters per second'
        side = ''
        if(timeperiod=='currently'):
            answer=data[timeperiod]['windSpeed']
            if(answer>0):
                side = self.degreesToWorldSide(data[timeperiod]['windBearing'])
            return self.get_simplesentence(answer,'There is ' + side + ' wind of speed ', units)
        else:
            answer=data[timeperiod]['data'][offset]['windSpeed']
            if(answer>0):
                side = self.degreesToWorldSide(data[timeperiod]['data'][0]['windBearing'])
            return self.get_simplesentence(answer,'There will be ' + side + ' wind of speed ', units)

    def get_moonphase(self,data,entity,offset,timeperiod='daily'):
        phase=data['daily']['data'][offset]['moonPhase']

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

    def get_percipitation(self, data,entity,offset,timeperiod='currently'):
        units=['milimeters per second', 'centimeters per second']
        unit_index = 0
        if(timeperiod=='currently'):
            if('precipType' in data[timeperiod]):
                if('rain' in data[timeperiod]['precipType']):
                    precipType='rain'
                elif('sleet' in data[timeperiod]['precipType']):
                    precipType='sleet'
                elif('hail' in data[timeperiod]['precipType']):
                    precipType='hail'
                elif('snow' in data[timeperiod]['precipType']):
                    precipType='snow'
                    unit_index = 1
                else:
                    return 'Currently, there are no precipitations.'
                
                intensity = data[timeperiod]['precipIntensity']
                quantum = self.precipQuantity(self,intensity)
                if(quantum == 'no precipitation'):
                    return 'Currently, there are no precipitations.'
                return 'There is ' + quatum + ' ' + precipType + ' of intensity ' + str(intensity) + ' ' + units[unit_index] + '.'
            else:
                return 'Currently, there are no precipitations.'
        else:
            return 'I dont know'
    
    #check if the datetime is specified and take it into account
    def check_query_datetime(self,entities):
        if 'datetime' in entities:  #If datetime is present in the query, take it into account
            if 'interval' in entities['datetime'][0]['type']:  #In case of interval, take the beginning

                timeOffsetB=Weather.get_timeperiod_offset(entities['datetime'][0]['from']['value'],entities['datetime'][0]['from']['grain'])
                if timeOffsetB != 'Not supp':
                    timeperiodB=timeOffsetB['timeperiod']
                    offsetB=timeOffsetB['offset']
                else:
                    return 'Not supp'

                timeOffsetE=Weather.get_timeperiod_offset(entities['datetime'][0]['to']['value'],entities['datetime'][0]['to']['grain'])
                if timeOffsetE != 'Not supp':
                    timeperiodE=timeOffsetE['timeperiod']
                    offsetE=timeOffsetE['offset']
                else:
                    return 'Not supp'
                
                if timeperiodB==timeperiodE:
                    offset=(offsetB+offsetE)/2
                    timeperiod=timeperiodB
                else:
                    if timeperiodB=='daily':
                        offset=offsetB
                        timeperiod=timeperiodB
                    else:
                        offset=offsetE
                        timeperiod=timeperiodE

                return {'timeperiod':timeperiod, 'offset':offset}
            else:
                return Weather.get_timeperiod_offset(entities['datetime'][0]['value'],entities['datetime'][0]['grain'])
        else:
            return 'Not supp'

    #call_switcher indexes to the dictionary with key, calling the appropriate function. Firstly, it tries the call with the default timeperiod,
    #if this fails it tries it with other timeperiods.
    def call_switcher(self, key, data, timeperiod, offset):
        entity = Weather.switcher[key]
        if timeperiod=='':
            try:
                answer=entity['function'](self,data,entity,offset)
            except:
                try:
                    answer=entity['function'](self,data,entity,offset,'hourly')
                except:
                    try:
                        answer=entity['function'](self,data,entity,offset,'daily')
                    except:
                        answer='I could not receive the information'            
        else:
            answer=entity['function'](self,data,entity,offset,timeperiod)

        return answer
    
    #switcher serves as an intent switch, based on the intent, the appropriate actions are taken. The intents might change in the future
    switcher={'weather' : {'function': get_summary},
              'temperature': {'function': get_specialforecast, 'value' : 'temperature', 'name': 'temperature', 'units': 'degrees celsius'},
              'sunrise':     {'function': get_sunTime, 'value' : 'sunriseTime',     'name': 'sunrise time'},
              'sunset':      {'function': get_sunTime, 'value' : 'sunsetTime',      'name': 'sunset time'},
              'humidity':    {'function': get_specialforecast, 'value' : 'humidity',    'name': 'humidity',    'units': 'percent'},
              'windspeed':   {'function': get_windspeed, 'value' : 'windspeed',    'name': 'wind speed',    'units': 'percent', 'side' : 'true'},
              'pressure':    {'function': get_specialforecast, 'value' : 'pressure',    'name': 'pressure',    'units': 'hectopascals'}, 
              'moonphase':   {'function': get_moonphase, 'value' : 'humidity',    'name': 'humidity',    'units': 'percent'},
              'temperaturemin':{'function': get_specialforecast, 'value' : 'temperatureMin', 'name': 'minimum temperature',    'units': 'degrees celsius'},
              'temperaturemax':{'function': get_specialforecast, 'value' : 'temperatureMax', 'name': 'maximum temperature',    'units': 'degrees celsius'},
              'visibility':    {'function': get_specialforecast, 'value' : 'visibility',     'name': 'visibility',             'units': 'kilometers'}, 
              'snow':{'function': get_percipitation}, 
              'rain':{'function': get_percipitation}, 
              }

    #Called from the query logic
    def query_resolution(self, intent, query, params):
        location=''
        time='now'
        timeperiod=''
        offset=0

        if 'city' in params:
            location=params['city']
            homelocation=getLocation(location)
            self.set_init_parameters(homelocation.latitude,homelocation.longitude)

        latitude=self.latitude
        longitude=self.longitude
        
        if intent == 'weather':
            if 'entities' in query:
                timeperiodOffset=self.check_query_datetime(query['entities'])
                
                if timeperiodOffset!='Not supp':
                    try:
                        timeperiod=timeperiodOffset['timeperiod']
                        offset=timeperiodOffset['offset']
                    except:
                        timeperiod=''
                        offset=0

                #If location is present in the query, take it into account
                if 'location' in query['entities']:    
                    location=query['entities']['location'][0]['value']
                    coordinates=getLocation(location)
                    longitude=coordinates.longitude
                    latitude=coordinates.latitude

                data = self.call_weather_api(latitude, longitude, time)
                
                #If weather_type is present in the query, take it into account
                if ('weather_type' in query['entities']) and (query['entities']['weather_type'][0]['value'] in self.switcher.keys()):
                    weather_type = query['entities']['weather_type'][0]['value']
                    if ('value_size' in query['entities']) and (weather_type + query['entities']['value_size'][0]['value'] in self.switcher.keys()):
                        answersentence=Weather.call_switcher(self, weather_type + query['entities']['value_size'][0]['value'],data, timeperiod, int(offset))
                    else:
                        answersentence=Weather.call_switcher(self,weather_type,data,timeperiod,int(offset))
                else:
                    answersentence=Weather.call_switcher(self,intent,data,timeperiod,int(offset))

                
            if not(answersentence is None):        
                answersentence = self.answer_polish(answersentence,location)                  
            else:
                answersentence = 'I am sorry, I could not retrieve the information'
            return answersentence

        else:
            answersentence='query not recognised'
            return answersentence

