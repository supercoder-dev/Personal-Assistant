"""
Date created: 12.3.2016
Author: Jiri Burant

The main control script of the Query logic part
At init, the currently present modules are loaded and initialized bz the info from config file,

"""

import os
import yaml
import json

class Query_control:

    def __init__(self):
        currentDir=os.path.dirname(os.path.abspath(__file__))
        moduleNames=os.listdir(os.path.join(currentDir,'modules'))
        moduleNames=['modules.' + s for s in moduleNames]

        moduleNames = [ name for name in moduleNames if not name.startswith('modules.__') ]
        self.modules=[]
        
        for i in range(0,len(moduleNames)):
            moduleNames[i]=moduleNames[i][:-3]
            self.modules.append(__import__(moduleNames[i], fromlist=['']))
            
        config = yaml.safe_load(open('config.yml'))

        self.args={}
        self.args['name'] = config['user']['name']
        self.args['mail']=config['user']['mail']
        self.args['town']=config['location']['town']
        self.args['country']=config['location']['country']
        
        self.moduleInst=[]
        
        for module in self.modules:
            initModule=module.init_hook(self.args)
            if(initModule!='Error'):
                self.moduleInst.append(initModule)

    def query_request(self, query):
        #jsonData = query.split("(")[1].strip(")")
        #jsonData = query.replace('[','').replace(']','')
        parsedQuery=json.loads(query)['outcomes'][0]          
		
        try:
            print(parsedQuery['_text'])
            intent=parsedQuery['intent']
        except:
            return 'malformed json'
        
        for module in self.moduleInst:
            answer=module.query_resolution(intent, parsedQuery, self.args)
            if(answer!='query not recognised'):
                return answer

        return answer
