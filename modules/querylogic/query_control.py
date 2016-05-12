#!/usr/bin/python3

"""
Date created: 12.3.2016
Author: Jiri Burant

The main control script of the Query logic part
At init, the currently present modules are loaded and initialized by the info from config file,

"""

import zmq
import sys
import datetime
import os
import json
import random

class Query_control:

    def __init__(self,port):
        self.port = port
        self.zmqctx = zmq.Context()
        
        currentDir=os.path.dirname(os.path.abspath(__file__))
        moduleNames=os.listdir(os.path.join(currentDir,'modules'))
        moduleNames=['modules.' + s for s in moduleNames]

        moduleNames = [ name for name in moduleNames if not name.startswith('modules.__') ]
        self.modules=[]

        self.runServer()
        
        for i in range(0,len(moduleNames)):
            moduleNames[i]=moduleNames[i][:-3]
            self.modules.append(__import__(moduleNames[i], fromlist=['']))
        
        self.moduleInst=[]
        
        for module in self.modules:
            initModule=module.init_hook()
            self.moduleInst.append(initModule)

    def runServer(self):
        self.socket = self.zmqctx.socket(zmq.REP)
        self.socket.bind('ipc://127.0.0.1:{}'.format(self.port))
    
    def application(self, message):
        #jsonData = query.split("(")[1].strip(")")
        #jsonData = query.replace('[','').replace(']','')

        testMode=0;
        
        query = message['JSON']
        parsedQuery=json.loads(query)['outcomes'][0]          
		
        try:
            print(parsedQuery['_text'])
            intent=parsedQuery['intent']
        except:
            return {'answer':"Query didn't parsed correctly."}
            
        message = ["I'm not able to answer your question",
                   "I don't know the asnwer.",
                   "I don't have answer for your query.",
                   "What about try some other query?",
                   "Query not recognised."]

        if(testMode==0):
            if ('weather' in intent): # try confidence score
               if parsedQuery['confidence'] < 0.93: 
                   return {'answer': random.choice(message)}
            elif parsedQuery['confidence'] < 0.75:
               return {'answer': random.choice(message)}
                
            for module in self.moduleInst:
                answer=module.query_resolution(intent, parsedQuery, self.config)
                if(answer!='query not recognised'):
                    return {'answer': answer}
        else:
            return {'answer': 'Query test answer string.'}

        return {'answer': random.choice(message)}

    def saveConfig(self, config):
        self.config=config
        # return result
        return True # if saved successufully
        return False # if saving failed (unknown config, bad config, some config missing, ...)

    def listen(self):
        while True:
          # wait for request
          message = self.socket.recv_json()

          config = message['config']
          data = message['data']

          # save config
          if bool(config):
            configSaved = self.saveConfig(config)
          else:
            # no config send
            configSaved = True

          # do what is needed with the data
          if bool(data):
            replyData = self.application(data)
          else:
            # no data send
            replyData = {}

          # prepare data before send
          replyTimestamp = datetime.datetime.now().isoformat(' ')
          reply = {'timestamp': replyTimestamp, 'data': replyData, 'config': {}}
          if configSaved == True:
            reply['config']['state'] = 'accepted'
          else:
            reply['config']['state'] = 'failed'

          # send back reply
          self.socket.send_json(reply)
      
if __name__ == '__main__':
    port = sys.argv[1]
    port = int(port)
    qc = Query_control(port)
    qc.listen()
