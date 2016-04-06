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

    #get_simplesentence returns the answer string, currently very simple
    def get_simplesentence(self,answer,subject,units=''):
        return 'The ' + str(subject) + str(answer) + ' ' +str(units) + '.'

    #again, very simple sentence
    def get_typeofprecipsentence(self,answer,verb):
        return 'It is ' + str(answer) + 'ing' + 'outside.'

    #append the info about the location to the answer.
    def answersentence_add_location(self,answersentence,location):
        return answersentence+' in ' + location

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
        units = 'degrees of celsius'
        if(timeperiod=='currently'):
            answer=data[timeperiod]['temperature']
            return self.get_simplesentence(answer,'temperature is ', units)  
        else:
            answer=data[timeperiod]['data'][0]['temperature']
            return self.get_simplesentence(answer,'temperature will be ', units)  
       
    def get_sunrise(self,data,timeperiod='daily'):
        time=self.convert_time(data[timeperiod]['data'][0]['sunriseTime']) 
        return self.get_simplesentence(time,'time of sunrise is ')  

    def get_sunset(self,data,timeperiod='daily'):
        time=self.convert_time(data[timeperiod]['data'][0]['sunsetTime'])
        return self.get_simplesentence(time,'time of sunset is ')
    
    def get_humidity(self,data,timeperiod='currently'):
        units = 'percent'
        if(timeperiod=='currently'):
            answer=data[timeperiod]['data'][0]['humidity']*100
            return self.get_simplesentence(answer,'humidity is ',units)
        else:
            answer=data[timeperiod]['data'][0]['humidity']
            return self.get_simplesentence(answer,'humidity will be ',units)

    def get_windspeed(self,data,timeperiod='currently'):
        units = 'meters per second'
        side = ''
        if(timeperiod=='currently'):
            answer=data[timeperiod]['windSpeed']
            if(answer>0):
                side = self.degreesToWorldSide(data[timeperiod]['windBearing'])
            return self.get_simplesentence(answer,'There is ' + side + ' wind of speed ', units)
        else:
            answer=data[timeperiod]['data'][0]['windSpeed']
            if(answer>0):
                side = self.degreesToWorldSide(data[timeperiod]['data'][0]['windBearing'])
            return self.get_simplesentence(answer,'There will be ' + side + ' wind of speed ', units)

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
        units = 'degrees of celsius'
        answer = data[timeperiod]['data'][0]['temperatureMin']
        return self.get_simplesentence(answer,'minimum temperature will be ',units)

    def get_temperatureMax(self,data,timeperiod='daily'):
        answer=data[timeperiod]['data'][0]['temperatureMax']
        return self.get_simplesentence(answer,'maximum temperature will be ',units)

    def get_visibility(self, data,timeperiod='currently'):
        units= 'kilometers'
        if(timeperiod=='currently'):
            answer=data[timeperiod]['visibility']
            return self.get_simplesentence(answer,'visibility is ', units)
        else:
            answer=data[timeperiod]['data'][0]['visibility']
            return self.get_simplesentence(answer,'visibility will be ', units)

    def get_pressure(self, data,timeperiod='currently'):
        units = 'hectopascals'
        if(timeperiod=='currently'):
            answer=data[timeperiod]['pressure']
            return self.get_simplesentence(answer,'pressure is ',units)
        else:
            answer=data[timeperiod]['data'][0]['pressure']
            return self.get_simplesentence(answer,'pressure will be ',units)

    def get_snow(self, data,timeperiod='currently'):
        units = 'centimeters per hour'
        if(timeperiod=='currently'):
            if('precipType' in data[timeperiod]):
                if('snow' in data[timeperiod]['precipType']):
                    precipType='snow'
                elif('sleet' in data[timeperiod]['precipType']):
                    precipType='sleet'
                    units = 'milimeters per hour'
                else:
                    return 'Currently, there are no precipitations.'
                
                intensity = data[timeperiod]['precipIntensity']
                quantum = self.precipQuantity(self,intensity)
                if(quantum == 'no precipitation'):
                    return 'Currently, there are no precipitations.'
                return 'There is ' + quatum + ' ' + precipType + ' of intensity ' + str(intensity) + ' ' + units + '.'
            else:
                return 'Currently, there are no precipitations.'
        else:
            return 'I dont know'

    def get_rain(self, data,timeperiod='currently'):
        units = 'milimeters per hour'
        if(timeperiod=='currently'):
            if('precipType' in data[timeperiod]):
                if('rain' in data[timeperiod]['precipType']):
                    precipType='rain'
                elif('sleet' in data[timeperiod]['precipType']):
                    precipType='sleet'
                elif('hail' in data[timeperiod]['precipType']):
                    precipType='hail'
                else:
                    return 'Currently, there are no precipitations.'
                
                intensity = data[timeperiod]['precipIntensity']
                quantum = self.precipQuantity(self,intensity)
                if(quantum == 'no precipitation'):
                    return 'Currently, there are no precipitations.'
                return 'There is ' + quatum + ' ' + precipType + ' of intensity ' + str(intensity) + ' ' + units + '.'
            else:
                return 'Currently, there are no precipitations.'
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
              'humidity':get_humidity,
              'windspeed':get_windspeed,
              'pressure':get_pressure,
              'moonphase':get_moonphase,
              'temperaturemin':get_temperatureMin,
              'temperaturemax':get_temperatureMax,
              'visibility':get_visibility,
              'snow':get_snow,
              'rain':get_rain,
              }
        
    #Called from the query logic
    def query_resolution(self, intent, query, params):
        if 'city' in params:
            location=params['city']
            homelocation=getLocation(location)
            self.set_init_parameters(homelocation.latitude,homelocation.longitude)

        time='now'
        
        if intent == 'weather':
            if 'entities' in query:
                if'datetime' in query['entities']:  #If datetime is present in the query, take it into account
                    if'interval' in query['entities']['datetime'][0]['type']:  #In case of interval, take the beginning
                        time=self.convertUTCtoUNIXtime(query['entities']['datetime'][0]['from']['value'])
                        timeOffset=calculate_time_offset(time)

                        if timeOffset['hours']>48 & timeOffset['days']<7:
                            offset=timeOffset['days']
                            timeperiod='daily'

                        else:
                            if timeOffset['hours']<48:
                                offset = timeOffset['hours']
                                timeperiod='hourly'


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

