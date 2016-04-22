#!/usr/bin/python3

import moduleWrapper

class getIntent(moduleWrapper.moduleWrapper):
  """
  Class maintaining get intent module.
  """

  def prepareConfigToSend(self, config):
    """
    Prepares config specific for each module.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    self.configToSend = {'dbToken': config['dbToken']}

