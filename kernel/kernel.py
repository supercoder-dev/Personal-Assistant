#!/usr/bin/python3

import attwordListener
import speechToText
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
    self.attwordListener = attwordListener.attwordListener(self.attwordConfig)
    self.speechToText = speechToText.speechToText(self.speechToTextConfig)
    self.queryProcessor = queryProcessor.queryProcessor(self.queryProcessorConfig)
    self.textToSpeech = textToSpeech.textToSpeech(self.textToSpeechConfig)


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
    self.queryProcessorConfig = cfg['queryProcessor']
    self.textToSpeechConfig = cfg['textToSpeech']

    self.globalConfig['configFileName'] = configFileName

    self.attwordConfig.update(self.globalConfig)
    self.speechToTextConfig.update(self.globalConfig)
    self.queryProcessorConfig.update(self.globalConfig)
    self.textToSpeechConfig.update(self.globalConfig)


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
      self.queryProcessor.start()
      self.textToSpeech.start()

      # do the work
      while True:
        activationWordTimestamp = self.attwordListener.sendReply({'action': 'listen'})['timeOfActivation']
        print(activationWordTimestamp)
        intend = self.speechToText.sendReply({'action': 'listen'})['JSON']
        print(intend)
        answer = self.queryProcessor.sendReply({'JSON': intend})['answer']
        print(answer)
        answerTimestamp = self.textToSpeech.sendReply({'answer': answer})['timeOfAnswer']
        print(answerTimestamp)

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
    self.queryProcessor.stop()
    self.textToSpeech.stop()



# DEMO
if __name__ == '__main__':
  kernel = Kernel()
  kernel.run()
