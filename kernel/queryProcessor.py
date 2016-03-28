#!/usr/bin/python3

import moduleWrapper

class queryProcessor(moduleWrapper.moduleWrapper):
  """
  Class maintaining query module.
  """

  def __init__(self, config):
    """
    Constuctor of the class.

    Args:
      config (dict): config of the module

    Returns:
      None
    """

    super(queryProcessor, self).__init__(config)

    self.configToSend = {'country': config['country'], 'city': config['city']}
    self.name = 'query processing module'

