#!/usr/bin/python3

import zmq
import subprocess
import json

class actwordListener:
  """
  Class maintaining action word listener module.
  """

  def __init__(self, config):
    """
    Constuctor of the class.

    Args:
      config (json): config of the module

    Returns:
      None
    """

    self.config = config
    self.port = 5556
    self.path = '../modules/dummy/dummy.py';

    # ZMQ
    self.zmqctx = zmq.Context()
    self.socket = self.zmqctx.socket(zmq.REQ)


  def execute(self):
    """
    Execute the subprocess and connect to server.

    Returns:
      None
    """

    # run the process
    self.process = subprocess.Popen([self.path, str(self.port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # create client
    self.socket.connect('ipc://127.0.0.1:{}'.format(self.port))

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

    self.process.terminate()


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
