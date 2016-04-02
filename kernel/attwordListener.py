#!/usr/bin/python3

import moduleWrapper

class attwordListener(moduleWrapper.moduleWrapper):
  """
  Class maintaining attention word listener module.
  """

  def prepareConfigToSend(self, config):
    """
    Prepares config specific for each module.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    self.configToSend = {'attentionWord': config['attentionWord'], 'threshold': float(config['threshold']), 'modelPath': config['modelPath'], 'dictionaryPath': config['dictionaryPath']}
