#!/usr/bin/python3

import zmq
import sys
import datetime
import os
import speech_recognition as sr

class speechToText:
  """
  Speech-to-text module class.
  """

  def __init__(self, port):
    """
    Constructor of the class.
    Args:
      port (int): port of the server
    Returns:
      None
    """

    self.port = port
    self.zmqctx = zmq.Context()
    self.runServer()
    self.r = sr.Recognizer()
    self.m = sr.Microphone()


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

    print("A moment of silence, please...")
    with self.m as source: self.r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(self.r.energy_threshold))

    print("Say!")
    with self.m as source: audio = self.r.listen(source)
    print("Got it! Now to recognize it...")
    try:
        # recognize speech using Google Speech Recognition
        value = self.r.recognize_google(audio)

        # we need some special handling here to correctly print unicode characters to standard output
        if str is bytes: # this version of Python uses bytes for strings (Python 2)
            message=u"{}".format(value).encode("utf-8")
        else: # this version of Python uses unicode for strings (Python 3+)
            message="{}".format(value)
    except self.sr.UnknownValueError:
        message="Oops! Didn't catch that"
    except self.sr.RequestError as e:
        message="Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e)

    # return result
    return {'request': message}


  def saveConfig(self, config):
    """
    Saves config received from the kernel.
    Args:
      config (dict): received config
    Returns:
      bool: True if config successuflly saved, False is not
    """
    return True


if __name__ == '__main__':
  port = sys.argv[1]
  port = int(port)
  dm = speechToText(port)
  dm.listen()
