import sys
import datetime
import os
import json

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



wit={"_text":"What is the weather today","msg_id":"20853b05-3c62-4766-8404-601b6d5eb6fa","outcomes":[{"_text":"What is the weather today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":"2016-04-12T00:00:00.000+02:00","values":[{"grain":"day","type":"value","value":"2016-04-12T00:00:00.000+02:00"}]}]},"intent":"weather"}]}
#+01:00 +01:00
params={'city':'Prague'}

for module in moduleInst:
    answer=module.query_resolution(wit['outcomes'][0]['intent'], wit['outcomes'][0], params)
        
    if(answer!='query not recognised'):
        print(answer)

wit={"_text":"wind in Brno tonight","msg_id":"067b058c-61cd-4ae2-bfba-7f70edb6ba77","outcomes":[{"_text":"wind in Brno tonight","confidence":0.735,"entities":{"datetime":[{"from":{"grain":"hour","value":"2016-04-9T19:00:00.000+02:00"},"to":{"grain":"hour","value":"2016-04-10T00:00:00.000+02:00"},"type":"interval","values":[{"from":{"grain":"hour","value":"2016-04-10T19:00:00.000+02:00"},"to":{"grain":"hour","value":"2016-04-10T00:00:00.000+02:00"},"type":"interval"}]}],"location":[{"suggested":'true',"type":"value","value":"Brno"}],"weather_type":[{"metadata":"","type":"value","value":"windspeed"}]},"intent":"weather"}]}
#+01:00 +01:00
params={'city':'Prague'}

for module in moduleInst:
    answer=module.query_resolution(wit['outcomes'][0]['intent'], wit['outcomes'][0], params)
        
    if(answer!='query not recognised'):
        print(answer)

wit={"_text":"What is the temperature maximum record for today","msg_id":"a4b5557b-1160-4118-b792-47aac33c2340","outcomes":[{"_text":"What is the temperature maximum record for today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":"2016-04-10T19:00:00.000+02:00","values":[{"grain":"day","type":"value","value":"2016-04-10T19:00:00.000+02:00"}]}],"value_size":[{"type":"value","value":"max"}],"weather_type":[{"type":"value","value":"temperature"}]},"intent":"weather"}]}

params={'city':'Prague'}

for module in moduleInst:
    answer=module.query_resolution(wit['outcomes'][0]['intent'], wit['outcomes'][0], params)
        
    if(answer!='query not recognised'):
        print(answer)

wit={"_text":"when is the sunset in London","msg_id":"7317188a-af4a-4a93-8635-24e91f4ac839","outcomes":[{"_text":"when is the sunset in London","confidence":0.735,"entities":{"location":[{"suggested":'true',"type":"value","value":"London"}],"weather_type":[{"type":"value","value":"sunset"}]},"intent":"weather"}]}
params={'city':'Prague'}

for module in moduleInst:
    answer=module.query_resolution(wit['outcomes'][0]['intent'], wit['outcomes'][0], params)
        
    if(answer!='query not recognised'):
        print(answer)


