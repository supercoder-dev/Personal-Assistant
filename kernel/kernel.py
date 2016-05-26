#!/usr/bin/python3

import attwordListener
import speechToText
import getIntent
import queryProcessor
import textToSpeech
import os
import yaml

class Kernel:
  """
  Class maintaining run of the whole application.
  """


  def __init__(self):
    """
    Initialization of the kernel.

    Returns:
      None
    """

    # load default config
    self.loadConfig('defaultConfig.yml')

    # init wrappers
    self.attwordListener = attwordListener.attwordListener(self.attwordConfig, 'attention word module')
    self.speechToText = speechToText.speechToText(self.speechToTextConfig, 'speech-to-text module')
    self.getIntent = getIntent.getIntent(self.getIntentConfig, 'get intent module')
    self.queryProcessor = queryProcessor.queryProcessor(self.queryProcessorConfig, 'query processing module')
    self.textToSpeech = textToSpeech.textToSpeech(self.textToSpeechConfig, 'text-to-speech module')


  def loadConfig(self, path):
    """
    Loads config from the given path.

    Args:
      path (str): path to the config file

    Returns:
      None
    """

    configFileName = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

    with open(configFileName, 'r') as ymlfile:
      cfg = yaml.load(ymlfile)

    self.globalConfig = cfg['global']
    self.attwordConfig = cfg['attword']
    self.speechToTextConfig = cfg['speechToText']
    self.getIntentConfig = cfg['getIntent']
    self.queryProcessorConfig = cfg['queryProcessor']
    self.textToSpeechConfig = cfg['textToSpeech']

    self.globalConfig['configFileName'] = configFileName

    self.attwordConfig.update(self.globalConfig)
    self.speechToTextConfig.update(self.globalConfig)
    self.getIntentConfig.update(self.globalConfig)
    self.queryProcessorConfig.update(self.globalConfig)
    self.textToSpeechConfig.update(self.globalConfig)

    # propage the new config into the module
    if hasattr(self, 'attwordListener'):
      self.attwordListener.loadConfig(self.attwordConfig)
    if hasattr(self, 'speechToText'):
      self.speechToText.loadConfig(self.speechToTextConfig)
    if hasattr(self, 'getIntent'):
      self.getIntent.loadConfig(self.getIntentConfig)
    if hasattr(self, 'queryProcessor'):
      self.queryProcessor.loadConfig(self.queryProcessorConfig)
    if hasattr(self, 'textToSpeech'):
      self.textToSpeech.loadConfig(self.textToSpeechConfig)


  def run(self):
    """
    Runs the application.

    Returns:
      None
    """

    try:
      # run all processes
      self.attwordListener.start()
      self.speechToText.start()
      self.getIntent.start()
      self.queryProcessor.start()
      self.textToSpeech.start()

      # do the work
      while True:
        print('Listening for the attention word...')
        activationWordTimestamp = self.attwordListener.sendReply({'action': 'listen'})['timeOfActivation']
        answerTimestamp = self.textToSpeech.sendReply({'answer': 'Listening honey'})['timeOfAnswer']
        print('Attention word spotted at {}'.format(activationWordTimestamp))
        print('Listening for the query...')
        sttResult = self.speechToText.sendReply({'action': 'listen'})
        #intent = sttResult['JSON']
        answerTimestamp = self.textToSpeech.sendReply({'answer':'Beep'})['timer']
        query = sttResult['request']
        print('Transcribed query: {}'.format(query))
        intent = self.getIntent.sendReply({'request': query})['JSON']
        answer = self.queryProcessor.sendReply({'JSON': intent})['answer']
        print('The answer is: {}'.format(answer))
        answerTimestamp = self.textToSpeech.sendReply({'answer': answer})['timeOfAnswer']
        print('The answer has been told.')

    except KeyboardInterrupt:
      print('Ctrl-C pressed. Exiting...')

    finally:
      # clean after all
      self.stop()


  def stop(self):
    """
    Stops all processes that have been run.

    Returns:
      None
    """

    self.attwordListener.stop()
    self.speechToText.stop()
    self.getIntent.stop()
    self.queryProcessor.stop()
    self.textToSpeech.stop()

    del self.attwordListener
    del self.speechToText
    del self.getIntent
    del self.queryProcessor
    del self.textToSpeech


# DEMO
if __name__ == '__main__':
  kernel = Kernel()
  kernel.run()
