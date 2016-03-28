#!/usr/bin/python3

import moduleWrapper

class textToSpeech(moduleWrapper.moduleWrapper):
  """
  Class maintaining text-to-speech module.
  """

  def __init__(self, config):
    """
    Constuctor of the class.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    super(textToSpeech, self).__init__(config)

    self.configToSend = {}
    self.name = 'text-to-speech module'

