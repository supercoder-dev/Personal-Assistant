#!/usr/bin/python3

"""
Date created: 12.3.2016
Author: Jiri Burant

The main control script of the Query logic part
At init, the currently present modules are loaded and initialized bz the info from config file,

"""

import zmq
import sys
import datetime
import os
import json

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
        query = message['JSON']
        parsedQuery=json.loads(query)['outcomes'][0]          
		
        try:
            print(parsedQuery['_text'])
            intent=parsedQuery['intent']
        except:
            return 'malformed json'
        
        for module in self.moduleInst:
            answer=module.query_resolution(intent, parsedQuery, self.config)
            if(answer!='query not recognised'):
                return {'answer': answer}

        return {'answer': answer}

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
          configSaved = self.saveConfig(config)

          # do what is needed with the data
          replyData = self.application(data)

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
