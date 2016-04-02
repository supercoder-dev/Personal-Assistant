#!/usr/bin/python3

import moduleWrapper

class queryProcessor(moduleWrapper.moduleWrapper):
  """
  Class maintaining query module.
  """

  def prepareConfigToSend(self, config):
    """
    Prepares config specific for each module.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    self.configToSend = {'country': config['country'], 'city': config['city']}
