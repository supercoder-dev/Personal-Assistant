#!/usr/bin/python3

import zmq
import sys
import datetime

class DummyModule:
  """
  Dummy module class, which just sends back what it receives.
  """

  def __init__(self, port):
    """
    Constructor of the dummy class.

    Args:
      port (int): port of the server

    Returns:
      None
    """

    self.port = port
    self.zmqctx = zmq.Context()
    self.runServer()


  def runServer(self):
    """
    Runs the ZMQ server.

    Returns:
      None
    """

    # bind the port
    self.socket = self.zmqctx.socket(zmq.REP)
    self.socket.bind('ipc://127.0.0.1:{}'.format(port))


  def listen(self):
    """
    Listens on the port.

    Returns:
      None
    """

    while True:
      # wait for request
      message = self.socket.recv_json()

      config = message['config']
      data = message['data']
      timestamp = message['timestamp']

      # save config
      configSaved = self.saveConfig(config)

      # do what is needed with the data
      replyData = self.logic(data)

      # prepare data before send
      replyTimestamp = datetime.datetime.now().isoformat(' ')
      reply = {'timestamp': replyTimestamp, 'data': replyData, 'config': {}}
      if configSaved == True:
        reply['config']['state'] = 'accepted'
      else:
        reply['config']['state'] = 'failed'

      # send back reply
      self.socket.send_json(reply)


  def logic(self, message):
    """
    Main logic of the module.

    Args:
      message (JSON): received data in JSON format

    Returns:
      JSON: data to send back in JSON format
    """

    # HERE GOES YOUR CODE
    print(message)

    # return result
    return message


  def saveConfig(self, config):
    """
    Saves config received from the kernel.

    Args:
      config (dict): received config

    Returns:
      bool: True if config successuflly saved, False is not
    """

    # HERE SAVE YOUR CONFIG
    print(config)

    # return result
    return True # if saved successufully
    return False # if saving failed (unknown config, bad config, some config missing, ...)



if __name__ == '__main__':
  port = sys.argv[1]
  port = int(port)
  dm = DummyModule(port)
  dm.listen()
