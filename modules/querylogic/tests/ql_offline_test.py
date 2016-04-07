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


while True:
    wit={"_text":"What is the weather today","msg_id":"20853b05-3c62-4766-8404-601b6d5eb6fa","outcomes":[{"_text":"What is the weather today","confidence":0.735,"entities":{"datetime":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00","values":[{"grain":"day","type":"value","value":"2016-03-27T00:00:00.000+01:00"}]}]},"intent":"weather"}]}

    params={'city':'Prague'}

    json=json.dumps()

    for module in moduleInst:
        answer=module.query_resolution(wit['intent'], wit['outcomes'][0], params)
        
        if(answer!='query not recognised'):
            return {'answer': answer}
