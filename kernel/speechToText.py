#!/usr/bin/python3

import moduleWrapper

class speechToText(moduleWrapper.moduleWrapper):
  """
  Class maintaining speech-to-text module.
  """

  def prepareConfigToSend(self, config):
    """
    Prepares config specific for each module.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    self.configToSend = {'modelPath': config['modelPath'], 'dictionaryPath': config['dictionaryPath'], 'grammarPath': config['grammarPath']}

