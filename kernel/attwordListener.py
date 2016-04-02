#!/usr/bin/python3

import moduleWrapper

class attwordListener(moduleWrapper.moduleWrapper):
  """
  Class maintaining attention word listener module.
  """

  def __init__(self, config):
    """
    Constuctor of the class.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    super(attwordListener, self).__init__(config)

    self.configToSend = {'attentionWord': config['attentionWord'], 'threshold': float(config['threshold']), 'modelPath': config['modelPath'], 'dictionaryPath': config['dictionaryPath']}
    self.name = 'attention word module'

