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


now=convertToString(datetime.datetime.now())
timeTo=convertToString(datetime.datetime.now()+datetime.timedelta(days=4))
timeFut=convertToString(datetime.datetime.now()+datetime.timedelta(days=2))

witTest=[{"_text":"What is the weather today","msg_id":"20853b05-3c62-4766-8404-601b6d5eb6fa","outcomes":[{"_text":"What is the weather today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":timeFut,"values":[{"grain":"day","type":"value","value":timeFut}]}]},"intent":"weather"}]},
{"_text":"Will be weather nice this weekend in Liberec","msg_id":"e4ff481d-0421-4b80-9b03-b0eab2bb7638","outcomes":[{"_text":"Will be weather nice this weekend in Liberec","confidence":0.735,"entities":{"datetime":[{"from":{"grain":"hour","value":timeFut},"to":{"grain":"hour","value":timeTo},"type":"interval","values":[{"from":{"grain":"hour","value":timeFut},"to":{"grain":"hour","value":timeTo},"type":"interval"}]}],"location":[{"suggested":'true',"type":"value","value":"Liberec"}]},"intent":"weather"}]},
{"_text":"wind in Brno tonight","msg_id":"067b058c-61cd-4ae2-bfba-7f70edb6ba77","outcomes":[{"_text":"wind in Brno tonight","confidence":0.735,"entities":{"datetime":[{"from":{"grain":"hour","value":"2016-04-9T19:00:00.000+02:00"},"to":{"grain":"hour","value":timeTo},"type":"interval","values":[{"from":{"grain":"hour","value":"2016-04-10T19:00:00.000+02:00"},"to":{"grain":"hour","value":timeTo},"type":"interval"}]}],"location":[{"suggested":'true',"type":"value","value":"Brno"}],"weather_type":[{"metadata":"","type":"value","value":"windspeed"}]},"intent":"weather"}]},
{"_text":"What is the temperature maximum record for today","msg_id":"a4b5557b-1160-4118-b792-47aac33c2340","outcomes":[{"_text":"What is the temperature maximum record for today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":timeFut,"values":[{"grain":"day","type":"value","value":timeFut}]}],"value_size":[{"type":"value","value":"max"}],"weather_type":[{"type":"value","value":"temperature"}]},"intent":"weather"}]},
{"_text":"when is the sunset in London","msg_id":"7317188a-af4a-4a93-8635-24e91f4ac839","outcomes":[{"_text":"when is the sunset in London","confidence":0.735,"entities":{"location":[{"suggested":'true',"type":"value","value":"London"}],"weather_type":[{"type":"value","value":"sunset"}]},"intent":"weather"}]},
{"_text":"Tell me the outside temperature in Paris","msg_id":"6dadd35b-3595-4322-9ad8-6bf2f25aa084","outcomes":[{"_text":"Tell me the outside temperature in Paris","confidence":0.735,"entities":{"location":[{"suggested":'true',"type":"value","value":"Paris"}],"weather_type":[{"type":"value","value":"temperature"}]},"intent":"weather"}]},
{"_text":"Sunrise tomorrow in Prague","msg_id":"8228e694-7f9d-4ec5-9b46-f0b2b81aa05e","outcomes":[{"_text":"Sunrise tomorrow in Prague","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":timeFut,"values":[{"grain":"day","type":"value","value":timeFut}]}],"location":[{"suggested":'true',"type":"value","value":"Prague"}],"weather_type":[{"type":"value","value":"sunrise"}]},"intent":"weather"}]},
{"_text":"What lunar phase is it","msg_id":"e64a37a3-9613-4beb-9b8f-115f99136fca","outcomes":[{"_text":"What lunar phase is it","confidence":0.735,"entities":{"weather_type":[{"type":"value","value":"moonphase"}]},"intent":"weather"}]},
{"_text":"Will be the stars visible tonight","msg_id":"d2c5be02-82c5-4a71-a2be-462013e8502a","outcomes":[{"_text":"Will be the stars visible tonight","confidence":0.735,"entities":{"datetime":[{"from":{"grain":"hour","value":timeFut},"to":{"grain":"hour","value":timeTo},"type":"interval","values":[{"from":{"grain":"hour","value":timeFut},"to":{"grain":"hour","value":timeTo},"type":"interval"}]}],"weather_type":[{"type":"value","value":"cloudy"}]},"intent":"weather"}]}

]

#{"_text":"What is the air pressure today","msg_id":"0d58b3e9-924f-40e7-b721-da9289a1db50","outcomes":[{"_text":"What is the air pressure today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00","values":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00"}]}],"weather_type":[{"type":"value","value":"pressure"}]},"intent":"weather"}]}
#{"_text":"What is the temperature minmium record for today","msg_id":"4709662a-7bf2-4707-90c2-ebac1bfa8871","outcomes":[{"_text":"What is the temperature minmium record for today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00","values":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00"}]}],"weather_type":[{"type":"value","value":"temperature"}]},"intent":"weather"}]}
#{"_text":"What is the temperature maximum record for today","msg_id":"a4b5557b-1160-4118-b792-47aac33c2340","outcomes":[{"_text":"What is the temperature maximum record for today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00","values":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00"}]}],"value_size":[{"type":"value","value":"max"}],"weather_type":[{"type":"value","value":"temperature"}]},"intent":"weather"}]}

for wit in witTest:
    for module in moduleInst:
        answer=module.query_resolution(wit['outcomes'][0]['intent'], wit['outcomes'][0], params)
        
        if(answer!='query not recognised'):
            print(answer)

