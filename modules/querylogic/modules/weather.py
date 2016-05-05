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
import math
import random

#TODO - hourly forecast -> collect data and time(afternoon, morning, night,...)
#       now changed to daily -> line cca 555
#       mabye it's fine to do daily forecast

def getLocation(place):
    geolocator = Nominatim()
    location = geolocator.geocode(place)
    #class Location(object):
     #   def __init__(self,latitude,longitude):
      #      self.latitude=latitude
       #     self.longitude=longitude
    #return Location(50.0874654,14.4212503)	#Prague
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

    def calculate_time_offset(timeTo, timeFrom):
        diff = timeTo - timeFrom
        daysOffset = diff.days
        
        try:
            hoursOffset = diff.days*24+int(round(diff.seconds/3600))
            #if hoursOffset>daysOffset*24:
                #daysOffset=daysOffset+1
        except:
            hoursOffset = diff.days*24

        return {'days': daysOffset, 'hours': hoursOffset, 'seconds': diff.seconds}

    def get_timeperiod_offset(timeStart,timeEnd, timeDelta,grain):  # zacatek intervalu, konec intervalu, casovy posun oproti soucasnu
        utcStart = Weather.convertUTCtoDatetime(timeStart)
        utcEnd = Weather.convertUTCtoDatetime(timeEnd)
        timeOffset=Weather.calculate_time_offset(utcEnd,utcStart)	
        if timeOffset['hours']>timeOffset['days']*24:
            timeOffset['days']=timeOffset['days']+1

        if ((timeDelta['days'] >= -366) and (timeDelta['days'] <= 5)):
            if ((grain != 'hour') or (int(timeOffset['hours'])>48)):
                offset=timeOffset['days']
                timeperiod='daily'
            else:
                offset = timeOffset['hours']
                timeperiod='hourly'  
            return {'offset':offset,'timeperiod':timeperiod}
        
        if ((timeDelta['days'] > 5) and (timeDelta['days'] < 30)) or (timeDelta['days'] < -366):
            offset=timeOffset['days']
            timeperiod='daily'
            return {'offset':offset,'timeperiod':timeperiod}

        if (timeDelta['days'] > 30):
	        return 'Not supp'     #lze jeste interval hodne zvetsit(20 let dopredu), ale jsou to jen odhady 
                
    #get_simplesentence returns the answer string, currently very simple
    def get_simplesentence(self,answer,subject,units=''):
        return 'The ' + str(subject) + str(answer) + ' ' +str(units) + '.'


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
        k = 2.54 #inches to milimeter
        if(0.002*k>precipIntensity):
            return 'no precipitation'
        if(0.017*k>precipIntensity):
            return 'very light'
        if(0.1*k>precipIntensity):
            return 'ligth'
        if(0.4*k>recipIntensity):
            return 'moderate'
        return 'heavy'

    def get_phasespecif(self,phase):
        if(phase==0):
            return 'new moon'
        if(phase==0.5):
            return 'full moon'
        if(phase==0.25):
            return 'first quarter'
        if(phase==0.75):
            return 'last quarter'
        if(phase<0.25):
            return 'waxing crescent'
        if(phase>0.25 and phase<0.5):
            return 'waxing gibbous'
        if(phase>0.5 and phase<0.75):
            return 'wanning gibbous'
        return 'wanning crescent'

    def cloudintensity(self,cloudCover):
        if(cloudCover<0.1):
            return 'clear'
        if(cloudCover<0.25):
            return 'mostly clear'
        if(cloudCover<0.75):
            return 'partly cloudy'
        if(cloudCover<0.9):
            return 'mostly cloudy'
        return 'cloudy'

    def convert_time(posixtime):
        return datetime.datetime.fromtimestamp(int(posixtime)).strftime('%Y-%m-%d %H:%M:%S')
    def time_to_day(posixtime):
        return datetime.datetime.fromtimestamp(int(posixtime)).strftime('%A')

    def convertUTCtoUNIXtime(utctime, ignore = False):
        d = Weather.convertUTCtoDatetime(utctime,ignore)
        return int(tm.mktime(d.timetuple()))

    def convertUTCtoDatetime(utctime,ignore = False):
        timeZone=utctime[-6:-3]
        utctime=utctime[:-6] #ignoring time zone 
        d = datetime.datetime.strptime( utctime, "%Y-%m-%dT%H:%M:%S.%f" )
        if ignore:
            return d
        return d + datetime.timedelta(hours=-int(timeZone) + 0.01)

    def get_summary(self,data,entity,offset,timeWord,timeperiod='daily'):
        #print(offset)
        if min(offset) == 0 and (len(offset)>3 or len(offset)==8):
            sum_data = data[timeperiod]['summary']
            answers = ["The forecast for next 7 days : " + sum_data,
                       "The forcast says : " + sum_data ]
            return random.choice(answers)
        
        dictAnsSum = self.get_forecastData(data,entity,offset,timeperiod)
        answer = ''; 
        if (timeperiod=='currently'):
            entity1 = Weather.switcher[entity['currFunctions'][0]]
            dictforec1 = entity1['subfunction'](self,data,entity1,offset,timeperiod)
            entity2 = Weather.switcher[entity['currFunctions'][1]]
            dictforec2 = entity2['subfunction'](self,data,entity2,offset,timeperiod)
            for i in range(len(dictAnsSum['answer'])):
                answer = answer + dictAnsSum['answer'][i]+', ' +entity1['name']+' ' +dictforec1['answer'][i] +' ' +entity1['units']+', '+ entity2['name']+' ' + dictforec2['answer'][i] +' ' +entity2['units']+' now. '
        else:
            entity1 = Weather.switcher[entity['subFunctions'][0]]
            dictforec1 = entity1['subfunction'](self,data,entity1,offset,timeperiod)
            entity2 = Weather.switcher[entity['subFunctions'][1]]
            dictforec2 = entity2['subfunction'](self,data,entity2,offset,timeperiod) 
            entity3 = Weather.switcher[entity['subFunctions'][2]]
            dictforec3 = entity3['subfunction'](self,data,entity3,offset,timeperiod) 
            for i in range(len(dictAnsSum['answer'])):
                answer = answer + (dictAnsSum['answer'][i])[:-1]+', ' +(entity1['value'])[:-3]+' from ' +dictforec2['answer'][i] +' to '+ dictforec1['answer'][i] +' ' +entity2['units']+' '+ dictAnsSum['timespec'][i]+'. '
        
        return self.get_simplesentence(answer[:-2],' forecast says ' +timeWord+ ' ')

    def get_specialforecast(self,data,entity,offset,timeWord,timeperiod='currently'):
        dictAnswer = self.get_forecastData(data,entity,offset,timeperiod)  
        answer = '';    
        for i in range(len(dictAnswer['answer'])):
            answer = answer + dictAnswer['answer'][i] +' ' +entity['units'] + dictAnswer['timespec'][i]+', '
        return self.get_simplesentence(answer[:-2],entity['name'] +' '+timeWord+' ')
   
    def get_cloud(self,data,entity,offset,timeWord,timeperiod='currently'):
        dictAnswer = self.get_forecastData(data,entity,offset,timeperiod)  
        answer = '';    
        for i in range(len(dictAnswer['answer'])):
            answer = answer + dictAnswer['answer'][i] +' ' +entity['units'] + dictAnswer['timespec'][i]+', '
        return self.get_simplesentence(answer[:-2],'forecast says '+timeWord+' ')

    def get_astronomy(self,data,entity,offset,timeWord,timeperiod='daily'):
        dictAnswer = self.get_astronomyData(data,entity,offset,timeperiod)  
        answer = '';    
        for i in range(len(dictAnswer['answer'])):
            answer = answer + dictAnswer['answer'][i] + dictAnswer['timespec'][i]+','
        return self.get_simplesentence(answer[:-1],entity['name'] +' '+timeWord+' ')

    def get_astronomyData(self,data,entity,offset,timeperiod):
        answer = []
        timespec = []
        
        if (timeperiod=='hourly'):
            offset_days_max = int(max(list(offset))/24)
            offset_days_min = int(min(list(offset))/24)
            offset = range(offset_days_min,offset_days_max+1)
        timeperiod='daily'
        for i in offset:
            subdata = data[timeperiod]['data'][i]
            if (entity['value'] == 'moonPhase'):
                value = self.get_phasespecif(subdata[entity['value']])
            else: 
                value = Weather.convert_time(subdata[entity['value']])
            timespec.append(' on ' + Weather.time_to_day(subdata['time']))
            answer.append(str(value))
        return {'answer':answer, 'timespec':timespec }
                   
    def get_windspeed(self,data,entity,offset,timeWord,timeperiod='currently'):
        dictAnswer = self.get_forecastData(data,entity,offset,timeperiod)
        dictAnswer = self.add_side(data,entity,offset,timeperiod,dictAnswer)
        
        answer = '';    
        for i in range(len(dictAnswer['answer'])):
            answer = answer + 'the '+dictAnswer['side'][i]+' '+entity['name'] +' '+dictAnswer['answer'][i] +' ' +entity['units'] + dictAnswer['timespec'][i]+','
        return self.get_simplesentence(answer[:-1],'forecast says ' +' '+timeWord+' ')
    
    def get_windspeedData(self,data,entity,offset,timeperiod): # output> answer, timespec, side
        return self.add_side(data,entity,offset,timeperiod,self.get_forecastData(data,entity,offset,timeperiod))
    
    def add_side(self,data,entity,offset,timeperiod,answer):
        timespec = answer['timespec']
        answer = answer['answer']
        side = []
        k = 0
        for i in offset:
             if (timeperiod == 'currently'):
                 subdata = data[timeperiod]
             else:
                 subdata = data[timeperiod]['data'][i]
             
             if(answer[k] != '0'):
                 worldside = self.degreesToWorldSide(subdata[entity['side']])
             else:
                 side = ''
             k = k+1 
             side.append(str(worldside))
        return {'answer':answer, 'timespec':timespec, 'side': side}

    def get_forecastData(self,data,entity,offset,timeperiod):
        answer = []
        timespec = []

        for i in offset:
             if (timeperiod == 'currently'):
                 subdata = data[timeperiod]
                 posixday = ''
             else:
                 subdata = data[timeperiod]['data'][i]
                 posixday = ' on ' + Weather.time_to_day(subdata['time'])
             answerNew=subdata[entity['value']]

             if(entity['units'] == 'percent'):
                 answerNew = answerNew*100
             elif(entity['value'] == 'cloudCover'):
                 answerNew = self.cloudintensity(answerNew)
             elif(entity['units'] == 'degrees celsius' or entity['value'] == 'windSpeed' ):
                 answerNew = round(answerNew)
             answer.append(str(answerNew))
             timespec.append(posixday)
        return {'answer':answer, 'timespec':timespec }   


    def get_neareststorm(self,data,entity,offset,timeWord,timeperiod='currently'):
        units = 'kilomerets'
        if('nearestStormDistance' in data['currently']):
            answer=data['currently']['nearestStormDistance']
            if(answer>0):
                side = self.degreesToWorldSide(data['currently']['nearestStormBearing'])
                return self.get_simplesentence(answer,'nearest thunderstorm is ', units + ' '+side)

            else:
                return 'It\'s a thunderstorm place.'
        else:
            return 'There aren\'t any thunderstorms data for this time.'
    
    # write for full moon position but can work also for new noon etc.
    def get_moonposition(self,data,entity,offset,timeWord,timeperiod='daily'):
        dictAnswer = self.get_moonpositionData(data,entity,offset,timeperiod)
        answer = '';    
        for i in range(len(dictAnswer['answer'])):
            if (dictAnswer['answer'][i] == 0):
                answer = answer +'it\'s a '+ entity['name'] +' day '+dictAnswer['timespec'][i]+', '
            else:
                answer = answer + 'the last ' + entity['name'] +' was ' + dictAnswer['subanswer'][i] + ' days ago and the next '+ entity['name'] +' will be for ' + dictAnswer['answer'][i] + ' days ' + dictAnswer['timespec'][i]+', '
        return answer[:-2] + '.'

    # write for full moon position but can work also for new noon etc.
    def get_moonpositionData(self,data,entity,offset,timeperiod):
        answerNext = []
        answerLast = []
        timespec = []
        moonphasePerDay = 1/29.5306
        fullmoon = 0.5
        if (timeperiod=='hourly'):
            offset_days_max = int(max(list(offset))/24)
            offset_days_min = int(min(list(offset))/24)

            offset = range(offset_days_min,offset_days_max+1)
        timeperiod='daily'
        for i in offset:
            subdata = data[timeperiod]['data'][i]
            phase=subdata['moonPhase'] - fullmoon + entity['moon']
            if(phase>fullmoon-moonphasePerDay and phase<=fullmoon):
                nextfull = 0
                lastfull = -29

            if(phase<fullmoon):
                lastfull = int(round((phase + fullmoon)/moonphasePerDay))
                nextfull = int(round((-phase+ fullmoon)/moonphasePerDay))
            else:
                lastfull = int(round((phase + fullmoon-1)/moonphasePerDay))
                nextfull = int(round((-phase+ fullmoon+1)/moonphasePerDay))
                   
            timespec.append(' on ' + Weather.time_to_day(subdata['time']))
            answerNext.append(str(abs(nextfull)))
            answerLast.append(str(abs(lastfull)))
        return {'answer':answerNext, 'timespec':timespec, 'subanswer': answerLast }
    

    def get_percipitation(self, data,entity,offset,timeWord,timeperiod='currently'):
        dictAnswer = self.get_percipitationData(data,entity,offset,timeperiod)        
        answer = '';    
        for i in range(len(dictAnswer['answer'])):
            if (dictAnswer['icon'][i]):
                answer = answer + dictAnswer['answer'][i] + dictAnswer['timespec'][i]+', '
            elif(dictAnswer['answer'][i] == 'no precipitation'):
                answer = answer + dictAnswer['answer'][i] + dictAnswer['timespec'][i]+', '
            else:
                answer = answer + 'the '+dictAnswer['answer'][i]+' '+dictAnswer['precipType'][i] + ' of intensity ' + str(dictAnswer['intensity'][i]) +' ' +dictAnswer['units'][i] + dictAnswer['timespec'][i]+', '
        return 'There '+timeWord + ' ' + answer[:-1]

    def get_percipitationData(self, data,entity,offset,timeperiod):
        answer = []; timespec = [];  intensity = [];  pType = [];  units = []; icons = []
 
        for i in offset:
            precipType = ''
            unit = 'milimeters per hour'
            icon = False
            if (timeperiod == 'currently'):
                subdata = data[timeperiod]
                posixday = ''
            else:
                subdata = data[timeperiod]['data'][i]
                posixday = ' on ' + Weather.time_to_day(subdata['time'])
            intens = subdata['precipIntensity']
            
            if('precipType' in subdata):
                precipType=subdata['precipType']
                if (precipType == 'snow'):
                    unit = 'centimeters per hour'
            intensity.append(intens)     
            pType.append(precipType)
            units.append(unit)
            if(subdata['icon'] == precipType):
                answer.append(str(subdata['summary'])[:-1])
                icon = True
            else:
                answer.append(self.precipQuantity(intens))
            icons.append(icon)
            timespec.append(posixday)
        return {'answer':answer, 'timespec':timespec, 'intensity' : intensity, 'precipType': pType,  'units': units, 'icon':icons}   
    
    #check if the datetime is specified and take it into account
    def check_query_datetime(self,entities):
        now = datetime.datetime.utcnow()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if 'datetime' in entities:  #If datetime is present in the query, take it into account
            if 'interval' in entities['datetime'][0]['type']:  #In case of interval, take the beginning
                timeFrom = entities['datetime'][0]['from']['value']
                grain = entities['datetime'][0]['from']['grain']
                timeTo = entities['datetime'][0]['to']['value']
                startTime = Weather.convertUTCtoUNIXtime(timeFrom,True)

                deltaTime = Weather.calculate_time_offset(Weather.convertUTCtoDatetime(timeFrom,True),today)

                timeOffset=Weather.get_timeperiod_offset(timeFrom,timeTo, deltaTime, grain)
                #print(timeOffset)
                #print(deltaTime)
                if timeOffset != 'Not supp':
                    timeperiod= timeOffset['timeperiod']
                    offset    = timeOffset['offset']
                    if ('hourly' in timeperiod): # array from 0 to 47 = 48 hours
                        hoursOffset = deltaTime['hours']+ offset
                        if ( hoursOffset == 48):
                            offset = offset -1
                            startTime = 'now'
                        elif ( hoursOffset > 48):
                            if (offset == 24):
                                offset = offset -1
                            elif(offset > 24):
                                timeperiod = 'daily'
                                offset = round(offset/24)
                        else:
                            startTime = 'now'
            
                    if ('daily' in timeperiod):
                        
                        daysOffset = deltaTime['days']+ offset

                        if ( daysOffset <= 8) and ( daysOffset >= 0):
                            startTime = 'now'
                        elif ( offset != 0 ):
                            return 'Not supp'
                else:
                    return 'Not supp'

                return {'timeperiod':timeperiod, 'offset':offset, 'deltaTime' : deltaTime, 'startTime' : startTime}
            else:
                timeFrom = entities['datetime'][0]['value']
                
                # detlaTime because of time spesification
                deltaTime = Weather.calculate_time_offset(Weather.convertUTCtoDatetime(timeFrom,True),today) 
                grain_date = entities['datetime'][0]['grain']
                offset = 0
                startTime = Weather.convertUTCtoUNIXtime(timeFrom,True)
                #print(deltaTime)
                #print(Weather.convertUTCtoDatetime(timeFrom,True))
                #print(datetime.datetime.utcnow())
                if ('hour' in grain_date):
                    grain = 'hourly'
                elif ('day' in grain_date):
                    grain = 'daily'
                elif ('week' in grain_date):
                    if deltaTime['days'] == 0:
                        startTime = 'now'
                        grain = 'daily'
                        offset = 7
                    else:
                        return 'Not supp'
                else:
                    return 'Not supp'
                return {'timeperiod':grain, 'offset':offset, 'deltaTime' : deltaTime, 'startTime' : startTime}
        else:
            return {'timeperiod':'currently', 'offset': 0}

    #call_switcher indexes to the dictionary with key, calling the appropriate function. Firstly, it tries the call with the default timeperiod,
    #if this fails it tries it with other timeperiods.
    def call_switcher(self, key, data, timeperiod, offset,timeWord):
        entity = Weather.switcher[key]
        if timeperiod=='':
            try:
                answer=entity['function'](self,data,entity,offset,timeWord)
            except:
                try:
                    answer=entity['function'](self,data,entity,offset,timeWord,'hourly')
                except:
                    try:
                        answer=entity['function'](self,data,entity,offset,timeWord,'daily')
                    except:
                        answer='I could not receive the information'            
        else:
            answer=entity['function'](self,data,entity,offset,timeWord,timeperiod)

        return answer
    
    #switcher serves as an intent switch, based on the intent, the appropriate actions are taken. The intents might change in the future
    switcher={'weather' : {'function': get_summary, 'value': 'summary', 'units' : '', 'subFunctions':['temperaturemax', 'temperaturemin', 'windspeed'],'currFunctions':['temperature', 'windspeed'],'subfunction': get_forecastData},
              'temperature': {'function': get_specialforecast,'subfunction': get_forecastData, 'value' : 'temperature', 'name': 'temperature', 'units': 'degrees celsius'},
              'sunrise':     {'function': get_astronomy, 'subfunction': get_astronomyData, 'value' : 'sunriseTime',     'name': 'sunrise time', 'units': ''},
              'sunset':      {'function': get_astronomy, 'subfunction': get_astronomyData, 'value' : 'sunsetTime',      'name': 'sunset time', 'units': ''},
              'humidity':    {'function': get_specialforecast,'subfunction': get_forecastData, 'value' : 'humidity',    'name': 'humidity',    'units': 'percent'},
              'windspeed':   {'function': get_windspeed,'subfunction': get_windspeedData, 'value' : 'windSpeed',    'name': 'wind of speed',  'side' : 'windBearing', 'units' : 'meters per second'},
              'pressure':    {'function': get_specialforecast, 'subfunction': get_forecastData, 'value' : 'pressure',    'name': 'pressure',    'units': 'hectopascals'}, 
              'moonphase':   {'function': get_astronomy, 'subfunction': get_astronomyData, 'value' : 'moonPhase', 'name': 'moon phase', 'units': ''},
              'fullmoon':    {'function': get_moonposition,'subfunction': get_moonpositionData, 'value' : 'moonPhase', 'name': 'full moon', 'moon' : 0.5},
              'newmoon':     {'function': get_moonposition,'subfunction': get_moonpositionData, 'value' : 'moonPhase', 'name': 'new moon' , 'moon' : 0},
              'temperaturemin':{'function': get_specialforecast,'subfunction': get_forecastData, 'value' : 'temperatureMin', 'name': 'minimum temperature',    'units': 'degrees celsius'},
              'temperaturemax':{'function': get_specialforecast,'subfunction': get_forecastData, 'value' : 'temperatureMax', 'name': 'maximum temperature',    'units': 'degrees celsius'},
              'visibility':    {'function': get_specialforecast,'subfunction': get_forecastData, 'value' : 'visibility',     'name': 'visibility',             'units': 'kilometers'}, 
              'snow': {'function': get_percipitation }, 
              'rain': {'function': get_percipitation } , 
              'storm':{'function': get_neareststorm  }, 
              'cloudy':{'function': get_cloud,'subfunction': get_forecastData, 'value': 'cloudCover', 'name': '', 'units': ''}
              }

    #Called from the query logic
    def query_resolution(self, intent, query, params):
        location=''
        time='now'
        timeperiod=''
        offset=''
        timeWord = 'is'

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
                    if ('deltaTime' in  timeperiodOffset): # matching time word
                        if timeperiodOffset['deltaTime']['days']<0:
                            timeWord = 'was'
                            timeperiod = 'daily'
                        elif (timeperiodOffset['deltaTime']['days'] == 0) and (timeperiodOffset['deltaTime']['hours'] == 0):
                            timeWord = 'is'
                        else:
                            timeWord = 'will be'

                    if ('startTime' in  timeperiodOffset):
                        #print(timeperiodOffset['startTime'])
                        if (type(timeperiodOffset['startTime']) is str):
                            if ( 'hourly' in timeperiod ):
                                offset = range(timeperiodOffset['deltaTime']['hours'], timeperiodOffset['deltaTime']['hours']+offset)
                            else:
                                offset = range(timeperiodOffset['deltaTime']['days'] , timeperiodOffset['deltaTime']['days'] +offset)
                        else:
                            time = timeperiodOffset['startTime']
                            #print('startTime isnt string')
                            offset = range(offset+1)
                else:# add other answers
                    messages = ['I would like to know this forecast.',
                                "I don't tell you the forecast for this time specification.",
                                "I don't have data for this forecast.",
                                'I was unable to get the forecast information.']

                    return random.choice(messages)
                
                if (timeperiod == 'currently'):
                    offset = range(0,1)

                #If location is present in the query, take it into account
                if 'location' in query['entities']:    
                    location=query['entities']['location'][0]['value']
                    coordinates=getLocation(location)
                    longitude=coordinates.longitude
                    latitude=coordinates.latitude

                data = self.call_weather_api(latitude, longitude, time)
                # not correct - view TODO hourly forecast
                if (timeperiod=='hourly'):
                    offset_days_max = int(max(list(offset))/24)
                    offset_days_min = int(min(list(offset))/24)
                    offset = range(offset_days_min,offset_days_max+1)
                    timeperiod='daily'
                
                #If weather_type is present in the query, take it into account
                if ('weather_type' in query['entities']) and (query['entities']['weather_type'][0]['value'] in self.switcher.keys()):
                    weather_type = query['entities']['weather_type'][0]['value']
                    if ('value_size' in query['entities']) and (weather_type + query['entities']['value_size'][0]['value'] in self.switcher.keys()):
                        answersentence=Weather.call_switcher(self, weather_type + query['entities']['value_size'][0]['value'],data, timeperiod, offset,timeWord)
                    else:
                        answersentence=Weather.call_switcher(self,weather_type,data,timeperiod,offset,timeWord)
                else:
                    answersentence=Weather.call_switcher(self,intent,data,timeperiod,offset,timeWord)

                
            if not(answersentence is None):        
                answersentence = self.answer_polish(answersentence,location)                  
            else:
                answersentence = 'I am sorry, I could not retrieve the information'
            return answersentence

        else:
            answersentence='query not recognised'
            return answersentence

