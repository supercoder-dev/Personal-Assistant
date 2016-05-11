import sys
import datetime
import os
import json
import pytz


def convertToString(dt):
    strTime=dt.strftime("%Y-%m-%d %H:%M:%S")
    date=strTime[0:10]
    time=strTime[11:19]
    utc=date + 'T' + time + '.000+02:00'

    return utc


currentDir=os.path.dirname(os.path.abspath(__file__))
moduleNames=os.listdir(os.path.join(currentDir,'modules'))
moduleNames=['modules.' + s for s in moduleNames]

moduleNames = [ name for name in moduleNames if not name.startswith('modules.__') ]
modules=[]
        
for i in range(0,len(moduleNames)):
    moduleNames[i]=moduleNames[i][:-3]
    modules.append(__import__(moduleNames[i], fromlist=['']))    
    
moduleInst=[]    

for module in modules:
    initModule=module.init_hook()
    moduleInst.append(initModule)

params={'city':'Prague'}

now = datetime.datetime.now()
now = now.replace(hour=0, minute=0, second=0, microsecond=0)

timeTo=convertToString(now+datetime.timedelta(days=6))
timeFut=convertToString(now+datetime.timedelta(days=2))

test_features = []
test_features = [ 'temperaturemin', 'temperaturemax', 'temperature', 'cloudy', 'windspeed', 'humidity', 'pressure', 'sunset', 'sunrise', 'moonphase', 'newmoon', 'fullmoon', 'rain', 'snow', 'storm', 'weather']
witTest= []
for weather_type in test_features:
    witTest.append({"_text":"What is the weather ","outcomes":[{"entities":{"location":[{"suggested":'true',"type":"value","value":"Prague"}],"weather_type":[{"type":"value","value":weather_type}]},"intent":"weather"}]})
    witTest.append(
{"_text":"What is the weather today","outcomes":[{"_text":"What is the weather today","entities":{"datetime":[{"grain":"day","type":"value","value":timeFut,"values":[{"grain":"day","type":"value","value":timeFut}]}],"weather_type":[{"type":"value","value":weather_type}]},"intent":"weather"}]})
    witTest.append(
{"_text":"Will be weather nice this weekend in Tokyo","outcomes":[{"entities":{"datetime":[{"from":{"grain":"hour","value":timeFut},"to":{"grain":"hour","value":timeTo},"type":"interval","values":[{"from":{"grain":"hour","value":timeFut},"to":{"grain":"hour","value":timeTo},"type":"interval"}]}],"location":[{"suggested":'true',"type":"value","value":"Prague"}],"weather_type":[{"type":"value","value":weather_type}]},"intent":"weather"}]})


'''
witTest=[
         {"outcomes": [{"_text": "Tell me a joke about Chuck Norris", "confidence": 0.735, "entities": {'agenda_entry': 'joke'}, "intent": "agenda"}]},
    {"outcomes": [        {"_text": "Tell me the news about travel", "confidence": 0.735, "entities": {"content_type": "travel"},"intent": "news"}]},
    {"outcomes": [        {"_text": "Tell me the news for business", "confidence": 0.735, "entities": {"content_type": "business"},         "intent": "news"}]},
    {"outcomes": [{"_text": "Tell me the news about uk", "confidence": 0.735, "entities": {"content_type": "business"},                   "intent": "news"}]},
    {"outcomes": [{"_text": "Tell me the news", "confidence": 0.735, "entities": {}, "intent": "news"}]},
    {"outcomes": [        {"_text": "Tell me the news about sdanasd", "confidence": 0.735, "entities": {"content_type": "sdanasd"},         "intent": "news"}]},
    {"outcomes": [      {"_text": "Tell me a good joke", "confidence": 0.735, "entities": {"agenda_entry": "joke"},         "intent": 'agenda'}]},
         
         ]
'''

#{"_text":"What is the air pressure today","msg_id":"0d58b3e9-924f-40e7-b721-da9289a1db50","outcomes":[{"_text":"What is the air pressure today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00","values":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00"}]}],"weather_type":[{"type":"value","value":"pressure"}]},"intent":"weather"}]}
#{"_text":"What is the temperature minmium record for today","msg_id":"4709662a-7bf2-4707-90c2-ebac1bfa8871","outcomes":[{"_text":"What is the temperature minmium record for today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00","values":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00"}]}],"weather_type":[{"type":"value","value":"temperature"}]},"intent":"weather"}]}
#{"_text":"What is the temperature maximum record for today","msg_id":"a4b5557b-1160-4118-b792-47aac33c2340","outcomes":[{"_text":"What is the temperature maximum record for today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00","values":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00"}]}],"value_size":[{"type":"value","value":"max"}],"weather_type":[{"type":"value","value":"temperature"}]},"intent":"weather"}]}


for wit in witTest:
    for module in moduleInst:
        answer=module.query_resolution(wit['outcomes'][0]['intent'], wit['outcomes'][0], params)
        
        if(answer!='query not recognised'):
            print(answer)

