import zmq
import subprocess
import json
import datetime
import kernel

class queryModule:

  def __init__(self, config):
    self.config = config
    self.minPort = 6000
    self.maxPort = 6099
    self.maxRetries = 99
    self.port = None
    self.path = '../querylogic/query_control.py';
    self.configToSend = {}
    self.name = 'query module logic'

    # ZMQ
    self.zmqctx = zmq.Context()
    self.socket = self.zmqctx.socket(zmq.REQ)


  def execute(self):
    # disconnect from previus socket
    if self.port != None:
      self.socket.disconnect('ipc://127.0.0.1:{}'.format(port))

    # select free port
    tmpSocket = self.zmqctx.socket(zmq.REP)
    self.port = tmpSocket.bind_to_random_port('ipc://127.0.0.1', self.minPort, self.maxPort, self.maxRetries)
    tmpSocket.unbind('ipc://127.0.0.1:{}'.format(self.port))

    # run the process
    self.process = subprocess.Popen([self.path, str(self.port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # create client
    self.socket.connect('ipc://127.0.0.1:{}'.format(self.port))

  def start(self):
    self.execute()


  def stop(self):
    self.process.terminate()


  def sendReply(self, data):
    # prepare the data to send
    timestamp = datetime.datetime.now().isoformat(' ')
    message = {'data': data, 'config': self.configToSend, 'timestamp': timestamp}

    # send
    reply = self.commJSON(message)

    # parse the reply
    if 'config' in reply:
      pass
    else:
      raise kernel.CommunicationError(self.name, 'no field "config" in the reply')
    if 'state' in reply['config']:
      pass
    else:
      raise kernel.CommunicationError(self.name, 'no field "state" in the "config" section of the reply')
    if reply['config']['state'] == 'accepted':
      if 'data' in reply:
        return reply['data']
      else:
        raise kernel.CommunicationError(self.name, 'no field "data" in the reply')
    elif reply['config']['state'] == 'failed':
      raise kernel.ConfigError(self.name)
    else:
      raise kernel.CommunicationError(self.name, 'unknown value of the state of the configuration section')


  def comm(self, message):
    #check the process is running
    if self.process.poll() != None:
      self.execute()
    
    self.socket.send_string(message)
    return self.socket.recv().decode('utf-8')


  def commJSON(self, dct):
    return json.loads(self.comm(json.dumps(dct)))
