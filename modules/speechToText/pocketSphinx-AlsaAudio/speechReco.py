#!/usr/bin/python3

import zmq
import sys
import datetime
import os
import alsaaudio
import wave
import numpy
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

class SpeechReco:
  """
  SpeechReco class, which converts speech to text.
  """
  configured = False
  def __init__(self, port):
    """
    Constructor of the AttentionWord class.
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
      if bool(config) and not self.configured:
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

    # start Decoder
    self.decoder.start_utt()
    
    # configure input strem
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(32)
    
    in_speech_bf = True

    while True:
        l,buf = inp.read()
        if buf:
            self.decoder.process_raw(buf, False, False)
            if self.decoder.hyp() != None:
                try:
                    if self.decoder.hyp().hypstr != '':
                        print('Partial decoding result:' + self.decoder.hyp().hypstr)
                except AttributeError:
                    pass
                if self.decoder.get_in_speech():
                    sys.stdout.write('.')
                    sys.stdout.flush()
                if self.decoder.get_in_speech() != in_speech_bf:
                    in_speech_bf = self.decoder.get_in_speech()
                    if not in_speech_bf:
                        self.decoder.end_utt()
                        try:
                            if self.decoder.hyp().hypstr != '':
                                print('Stream decoding result:' + self.decoder.hyp().hypstr)
                                message = {'request': self.decoder.hyp().hypstr}
                                break
                        except AttributeError:
                            pass
        else:
            pass

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
    
    modelPath = config['modelPath']
    dictionaryPath = config['dictionaryPath']
    grammarPath = config['grammarPath']

    if bool(modelPath) and bool(dictionaryPath) and bool(grammarPath):
        # Create a decoder with certain model
        self.config = Decoder.default_config()
        self.config.set_string('-hmm', modelPath)
        self.config.set_string('-lm', grammarPath)
        self.config.set_string('-dict', dictionaryPath)
        self.config.set_float('-vad_threshold', 2.5)
        self.config.set_int('-nfft', 512)
        self.config.set_float('-samprate', 16000)
        
        self.decoder = Decoder(self.config)
        
        self.configured = True
        return True
    else: 
        return False


if __name__ == '__main__':
  port = sys.argv[1]
  port = int(port)
  dm = SpeechReco(port)
  dm.listen()
