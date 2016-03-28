#!/usr/bin/python3

import attwordListener
import speechToText
import queryProcessor

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

    # init wrappers
    self.attwordListener = attwordListener.attwordListener(self.attwordConfig)
    self.speechToText = speechToText.speechToText(self.speechToTextConfig)
    self.queryProcessor = queryProcessor.queryProcessor(self.queryProcessorConfig)


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

      # do the work
      for i in range(0, 10):
        print(self.attwordListener.sendReply({'iteration': i}))
        print(self.speechToText.sendReply({'iteration': i}))
        print(self.queryProcessor.sendReply({'iteration': i}))

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



# DEMO
if __name__ == '__main__':
  kernel = Kernel()
  kernel.run()
