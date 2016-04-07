"""
Date created: 12.3.2016
Author: Jiri Burant, Jakub Drapela

First demo of the possible weather module package.
"""

#      Be able to get the weather from past


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
        diff = time - datetime.utcnow()
        daysOffset = diff.TotalDays
        hoursOffset = diff.TotalHours

        return {'dOffset': daysOffset, 'hOffset': hoursOffset}

    def get_timeperiod_offset(timeIn,grain):
        timeConv=self.convertUTCtoUNIXtime(timeIn)
        timeOffset=calculate_time_offset(timeConv)

        if (grain == 'day' | timeOffset['hours']>48) & timeOffset['days']<7 :
            offset=timeOffset['days']
            timeperiod='daily'
            return {'offset':offset,'timeperiod':timeperiod}
        else:
            if timeOffset['hours']<48 & grain=='hour':
                offset = timeOffset['hours']
                timeperiod='hourly'
                return {'offset':offset,'timeperiod':timeperiod}
            else:
                return 'Not supp'
                
    #get_simplesentence returns the answer string, currently very simple
    def get_simplesentence(self,answer,subject):
        return 'The ' + str(subject) + str(answer) + '.'

    #again, very simple sentence
    def get_typeofprecipsentence(self,answer,verb):
        return 'It is ' + str(answer) + 'ing' + 'outside.'

    def answer_polish(self,answersentence,location):
        if self.check_answer(answersentence):
            return self.answersentence_add_location(answersentence,location)
        else:
            return answersentence
    def check_answer(self,answersentence):
        if answersentence!='Not supp' & answersentence!='' & answersentence!='I could not receive the information':
            return True
        else:
            return False

    #append the info about the location to the answer.
    def answersentence_add_location(self,answersentence,location):
        if location != '':
            return answersentence+' in ' + location
        else:
            return answersentence
  
    def convert_time(self, posixtime):
        return datetime.datetime.fromtimestamp(int(posixtime)).strftime('%Y-%m-%d %H:%M:%S')

    def convertUTCtoUNIXtime(self,utctime):
        utctime=utctime[:-6] #ignoring tme zone 
        d = datetime.datetime.strptime( utctime, "%Y-%m-%dT%H:%M:%S.%f" )
        return int(tm.mktime(d.timetuple()))

    def get_summary(self,data,offset,timeperiod='daily'):
        answer=data[timeperiod]['data'][offset]['summary']
        return self.get_simplesentence(answer,'forecast says ')  

    def get_temperature(self,data,offset,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['temperature']
            return self.get_simplesentence(answer,'temperature is ')  
        else:
            answer=data[timeperiod]['data'][offset]['temperature']
            return self.get_simplesentence(answer,'temperature will be ')  
       
    def get_sunrise(self,data,offset,timeperiod='daily'):
        time=self.convert_time(data[timeperiod]['data'][offset]['sunriseTime']) 
        return self.get_simplesentence(time,'time of sunrise is ')  

    def get_sunset(self,data,offset,timeperiod='daily'):
        time=self.convert_time(data[timeperiod]['data'][offset]['sunsetTime'])
        return self.get_simplesentence(time,'time of sunset is ')
    
    def get_precip_intensity(self,data,offset,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['data'][offset]['precipIntensity']
            return self.get_simplesentence(answer,'intensity of the precipations is ')
        else:
            answer=data[timeperiod]['data'][offset]['precipIntensity']
            return self.get_simplesentence(answer,'intensity of the precipations will be ')

    def get_humidity(self,data,offset,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['data'][offset]['humidity']
            return self.get_simplesentence(answer,'humidity is ')
        else:
            answer=data[timeperiod]['data'][offset]['humidity']
            return self.get_simplesentence(answer,'humidity will be ')

    def get_windspeed(self,data,offset,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['windSpeed']
            return self.get_simplesentence(answer,'speed of wind is ')
        else:
            answer=data[timeperiod]['data'][offset]['windSpeed']
            return self.get_simplesentence(answer,'speed of wind will be ')

    def get_moonphase(self,data,offset,timeperiod='daily'):
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

    def get_temperatureMin(self,data,offset,timeperiod='daily'):
        answer = data[timeperiod]['data'][offset]['temperatureMin']
        return self.get_simplesentence(answer,'minimum temperature will be ')

    def get_temperatureMax(self,data,offset,timeperiod='daily'):
        answer=data[timeperiod]['data'][offset]['temperatureMax']
        return self.get_simplesentence(answer,'maximum temperature will be ')

    def get_visibility(self, data,offset,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['visibility']
            return self.get_simplesentence(answer,'visibility is ')
        else:
            answer=data[timeperiod]['data'][offset]['visibility']
            return self.get_simplesentence(answer,'visibility will be ')

    def get_pressure(self, data,offset,timeperiod='currently'):
        if(timeperiod=='currently'):
            answer=data[timeperiod]['pressure']
            return self.get_simplesentence(answer,'pressure is ')
        else:
            answer=data[timeperiod]['data'][offset]['pressure']
            return self.get_simplesentence(answer,'pressure will be ')

    def get_snow(self, data,offset,timeperiod='currently'):
        if(timeperiod=='currently'):
            if('precipType' in data[timeperiod]['data'][offset]):
                answer=data[timeperiod]['data'][offset]['precipType']
                return self.get_typeofprecipsentence(answer,'')
            else:
                return 'Currently, there are no precipitations at the location.'
        else:
            return 'I dont know'
    
    #check if the datetime is specified and take it into account
    def check_query_datetime(self,entities):
        if 'datetime' in entities:  #If datetime is present in the query, take it into account
            if 'interval' in entities['datetime'][0]['type']:  #In case of interval, take the beginning

                timeOffsetB=get_timeperiod_offset(entities['datetime'][0]['from']['value'],entities['datetime'][0]['from']['grain'])
                if timeOffsetB != 'Not supp':
                    timeperiodB=timeOffsetB['timeperiod']
                    offsetB=timeOffsetB['offset']
                else:
                    return 'Not supp'

                timeOffsetE=get_timeperiod_offset(entities['datetime'][0]['to']['value'],entities['datetime'][0]['to']['grain'])
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
                return get_timeperiod_offset(entities['datetime'][0]['value'],entities['datetime'][0]['grain'])
        else:
            return 'Not supp'

    #call_switcher indexes to the dictionary with key, calling the appropriate function. Firstly, it tries the call with the default timeperiod,
    #if this fails it tries it with other timeperiods.
    def call_switcher(self, key, data, timeperiod, offset):
        if timeperiod=='':
            try:
                answer=Weather.switcher[key](self,data,offset)
            except:
                try:
                    answer=Weather.switcher[key](self,data,offset,'hourly')
                except:
                    try:
                        answer=Weather.switcher[key](self,data,offset,'daily')
                    except:
                        answer='I could not receive the information'            
        else:
            answer=Weather.switcher[key](self,data,timeperiod,offset)

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

                data = call_weather_api(self, latitude, longitude, time)
                
                #If weather_type is present in the query, take it into account
                if ('weather_type' in query['entities']) & (query['entities']['weather_type'][0]['value'] in self.switcher.keys()):
                    weather_type = query['entities']['weather_type'][0]['value']
                    if ('value_size' in query['entities']) & (weather_type + query['entities']['value_size'][0]['value'] in self.switcher.keys()):
                        answersentence=Weather.call_switcher(self, weather_type + query['entities']['value_size'][0]['value'],data, timeperiod, offset)
                    else:
                        answersentence=Weather.call_switcher(self,weather_type,data,timeperiod,offset)
                else:
                    answersentence=Weather.call_switcher(self,intent,data,timeperiod,offset)
                
                answersentence = self.answer_polish(answersentence,locaion)                  
        
            return answersentence

        else:
            answersentence='query not recognised'
            return answersentence

