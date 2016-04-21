#!/usr/bin/python3

import zmq
import subprocess
import json
import datetime
import kernelErrors
import os

class moduleWrapper:
  """
  Class maintaining module.
  """

  def __init__(self, config, name):
    """
    Constuctor of the class.

    Args:
      config (dict): config of the module
      name (str): name of the module

    Returns:
      None
    """

    self.startUpTime = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    self.loadConfig(config)
    self.port = None
    self.name = name

    # ZMQ
    self.zmqctx = zmq.Context()
    self.socket = self.zmqctx.socket(zmq.REQ)


  def __del__(self):
    """
    Destructor of the object.

    Returns:
      None
    """

    self.socket.close()
    self.zmqctx.term()


  def loadConfig(self, config):
    """
    Loads config into the module.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    self.config = config
    self.minPort = config['minPort']
    self.maxPort = config['maxPort']
    self.maxRetries = config['maxRetries']
    self.logPath = config['logPath']
    self.path = os.path.normpath(os.path.join(os.path.dirname(config['configFileName']), config['path']))
    self.prepareConfigToSend(config)

    # send config to the process
    if hasattr(self, 'process'):
      self.sendReply({});


  def prepareConfigToSend(self, config):
    """
    Prepares config specific for each module.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    raise NotImplementedError
    self.configToSend = {}


  def execute(self):
    """
    Execute the subprocess and connect to server.

    Returns:
      None
    """

    # disconnect from previus socket
    if self.port != None:
      self.socket.disconnect('ipc://127.0.0.1:{}'.format(self.port))

    # select free port
    tmpSocket = self.zmqctx.socket(zmq.REP)
    self.port = tmpSocket.bind_to_random_port('ipc://127.0.0.1', self.minPort, self.maxPort, self.maxRetries)
    tmpSocket.unbind('ipc://127.0.0.1:{}'.format(self.port))

    # open files to log
    os.makedirs(self.logPath, exist_ok = True)
    self.logStdout = open(os.path.join(self.logPath, self.startUpTime + '-' + self.name + '.out'), 'w')
    self.logStderr = open(os.path.join(self.logPath, self.startUpTime + '-' + self.name + '.err'), 'w')

    # run the process
    self.process = subprocess.Popen([self.path, str(self.port)], stdout=self.logStdout, stderr=self.logStderr)

    # create client
    self.socket.connect('ipc://127.0.0.1:{}'.format(self.port))

    # send config to the process
    self.sendReply({});


  def start(self):
    """
    Start the module.

    Returns:
      None
    """

    self.execute()


  def stop(self):
    """
    Terminate the module.

    Returns:
      None
    """

    # close files to log
    if hasattr(self, 'logStdout') and not self.logStdout.closed:
      self.logStdout.close()
    if hasattr(self, 'logStderr') and not self.logStderr.closed:
      self.logStderr.close()

    # disconnect from the server
    if self.port != None:
      self.socket.disconnect('ipc://127.0.0.1:{}'.format(self.port))

    # stop the process
    self.process.terminate()


  def sendReply(self, data):
    """
    Constructs the message from given data and sends it to the server. Waits for the reply, parse it and return received data.

    Args:
      data (dict): data to send in dictionary

    Returns:
      dict: received data
    """

    # prepare the data to send
    timestamp = datetime.datetime.now().isoformat(' ')
    message = {'data': data, 'config': self.configToSend, 'timestamp': timestamp}

    # send
    reply = self.commJSON(message)

    # parse the reply
    if 'config' in reply:
      pass
    else:
      raise kernelErrors.CommunicationError(self.name, 'no field "config" in the reply')
    if 'state' in reply['config']:
      pass
    else:
      raise kernelErrors.CommunicationError(self.name, 'no field "state" in the "config" section of the reply')
    if reply['config']['state'] == 'accepted':
      if 'data' in reply:
        return reply['data']
      else:
        raise kernelErrors.CommunicationError(self.name, 'no field "data" in the reply')
    elif reply['config']['state'] == 'failed':
      raise kernelErrors.ConfigError(self.name)
    else:
      raise kernelErrors.CommunicationError(self.name, 'unknown value of the state of the configuration section')


  def comm(self, message):
    """
    Sends string to the server and waits for the reply.

    Args:
      message (str): message to send

    Returns:
      str: received massage
    """

    #check the process is running
    if self.process.poll() != None:
      self.execute()
    
    self.socket.send_string(message)
    return self.socket.recv().decode('utf-8')


  def commJSON(self, dct):
    """
    Converts dictionary to a JSON string and sends it to the server. Then waits for the reply and converts is back to dictionary.

    Args:
      dct (dict): dictionary to send

    Returns:
      dict: received reply as dictionary
    """

    return json.loads(self.comm(json.dumps(dct)))
