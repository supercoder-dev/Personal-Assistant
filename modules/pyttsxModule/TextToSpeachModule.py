#!/usr/bin/python3

import zmq
import sys
import datetime
import pyttsx

class TextToSpeachModule:
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
    self.engine = pyttsx.init()
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


    msg = message['answer']
    self.engine.say(msg)
    self.engine.runAndWait()

    timestamp = datetime.datetime.now().isoformat(' ')
    result = {'timeOfAnswer': timestamp}

    return result


  def saveConfig(self, config):
    """
    Saves config received from the kernel.
    Args:
      config (dict): received config
    Returns:
      bool: True if config successuflly saved, False is not

    rate = self.engine.getProperty('rate')
    self.engine.setProperty('rate', rate+50)

    rate = self.engine.getProperty('volume')
    self.engine.setProperty('volume', rate+50)

    voices = self.engine.getProperty('voices')
    self.engine.setProperty('voice', voice.id)

    voices = self.engine.getProperty('voices')
    for voice in voices:
        self.engine.setProperty('voice', voice.id)
        self.engine.say('The quick brown fox jumped over the lazy dog.')


       try:
            #zde kod ktery se bude hlidat
       except KeyError:
           return False
        return True
    """

    # HERE SAVE YOUR CONFIG
    print(config)

    # return result
    return True # if saved successufully
    return False # if saving failed (unknown config, bad config, some config missing, ...)

    """

     """



if __name__ == '__main__':
  port = sys.argv[1]
  port = int(port)
  dm = TextToSpeachModule(port)
  dm.listen()
