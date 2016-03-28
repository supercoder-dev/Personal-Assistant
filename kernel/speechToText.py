#!/usr/bin/python3

import moduleWrapper

class speechToText(moduleWrapper.moduleWrapper):
  """
  Class maintaining speech-to-text module.
  """

  def __init__(self, config):
    """
    Constuctor of the class.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    super(speechToText, self).__init__(config)

    self.configToSend = {'dbToken': config['dbToken']}
    self.name = 'speech-to-text module'

