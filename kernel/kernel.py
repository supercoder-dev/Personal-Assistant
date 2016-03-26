#!/usr/bin/python3

import actwordListener

class Kernel:
  """
  Class maintaining run of the whole application.
  """


  def __init__(self):
    """
    Initialization of the kernel.

    Returns:
      None
    """

    self.actwordListener = actwordListener.actwordListener('')


  def run(self):
    """
    Runs the application.

    Returns:
      None
    """

    try:
      # run all processes
      self.actwordListener.start()

      # do the work
      for i in range(0, 10):
        print(self.actwordListener.sendReply({'iteration': i}))

    finally:
      # clean after all
      self.stop()


  def stop(self):
    """
    Stops all processes that have been run.

    Returns:
      None
    """

    self.actwordListener.stop()



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



# DEMO
if __name__ == '__main__':
  kernel = Kernel()
  kernel.run()
