#!/usr/bin/python3

import moduleWrapper

class textToSpeech(moduleWrapper.moduleWrapper):
  """
  Class maintaining text-to-speech module.
  """

  def prepareConfigToSend(self, config):
    """
    Prepares config specific for each module.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    self.configToSend = {}
