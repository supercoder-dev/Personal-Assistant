#!/usr/bin/python3

class ConfigError(Exception):
  """
  Exception class handling module configuration error.
  """

  def __init__(self, module):
    """
    Init of the exception.

    Args:
      module (str): name of module failed to config

    Returns:
      None
    """

    self.module = module
  
  def __str__(self):
    """
    Converts exception to a string.

    Returns:
      str: string representation of the exception
    """

    return 'Module "' + self.module  + '" failed to config.'



class CommunicationError(Exception):
  """
  Exception class handling communication error with the module.
  """

  def __init__(self, module, message):
    """
    Init of the exception.

    Args:
      module (str): name of module failed to communicate to
      message (str): description of the problem

    Returns:
      None
    """

    self.module = module
    self.message = message
  
  def __str__(self):
    """
    Converts exception to a string.

    Returns:
      str: string representation of the exception
    """

    return 'Communication failed with the module "' + self.module  + '" (' + self.message + ').'
