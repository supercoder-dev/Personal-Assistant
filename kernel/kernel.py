#!/usr/bin/python3

import attwordListener
import speechToText
import queryProcessor
import textToSpeech

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

    # global config
    self.minPort = 5000
    self.maxPort = 5999
    self.maxRetries = 99

    # attention word module config
    self.attwordConfig = {'path': '../modules/dummy/dummy.py', 'attentionWord': 'Fenix', 'threshold': 1}
    self.attwordConfig['minPort'] = self.minPort
    self.attwordConfig['maxPort'] = self.maxPort
    self.attwordConfig['maxRetries'] = self.maxRetries

    # speech-to-text module config
    self.speechToTextConfig = {'path': '../modules/dummy/dummy.py', 'dbToken': 'someToken'}
    self.speechToTextConfig['minPort'] = self.minPort
    self.speechToTextConfig['maxPort'] = self.maxPort
    self.speechToTextConfig['maxRetries'] = self.maxRetries

    # query module config
    self.queryProcessorConfig = {'path': '../modules/dummy/dummy.py', 'country': 'Czech Republic', 'city': 'Prague'}
    self.queryProcessorConfig['minPort'] = self.minPort
    self.queryProcessorConfig['maxPort'] = self.maxPort
    self.queryProcessorConfig['maxRetries'] = self.maxRetries

    # text-to-speech module config
    self.textToSpeechConfig = {'path': '../modules/dummy/dummy.py'}
    self.textToSpeechConfig['minPort'] = self.minPort
    self.textToSpeechConfig['maxPort'] = self.maxPort
    self.textToSpeechConfig['maxRetries'] = self.maxRetries

    # init wrappers
    self.attwordListener = attwordListener.attwordListener(self.attwordConfig)
    self.speechToText = speechToText.speechToText(self.speechToTextConfig)
    self.queryProcessor = queryProcessor.queryProcessor(self.queryProcessorConfig)
    self.textToSpeech = textToSpeech.textToSpeech(self.textToSpeechConfig)


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
        print(attwordConfig)
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
