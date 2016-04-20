#!/usr/bin/env python

import zmq
import sys
import datetime
import wit
import json


class SpeechToTextModule:
  """
  SpeechToText module class, which accepts database code and returns processed data.
  """

  def __init__(self, port):
    """
    Constructor of the SpeechToText class.

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


  def application(self, message):
    """
    Main application logic of the module.

    Args:
      message (dict): received data as a dictionary

    Returns:
      dict: data to send back as dictionary
    """
    action = message['action']
    if action == 'listen':
        wit.init()
        response = wit.voice_query_auto(self.access_token)

        print('Response: {}'.format(response))
        print('msg_id')
        jresponse = json.loads(response)
        print(jresponse["_text"])
        wit.close()
        data = {'request': jresponse["_text"], 'JSON': response}

        # return result
        return data
    else:
        return False


  def saveConfig(self, config):
    """
    Saves config received from the kernel.

    Args:
      config (dict): received config

    Returns:
      bool: True if config successuflly saved, False is not
    """

    try:
        self.access_token = config['dbToken']
    except KeyError:
        return False
    return True


if __name__ == '__main__':
    port = sys.argv[1]
    port = int(port)
    dm = SpeechToTextModule(port)
    dm.listen()
