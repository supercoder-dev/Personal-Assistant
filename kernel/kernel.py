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
        print(self.actwordListener.comm(str(i)))
        print(self.actwordListener.commJSON({'iteration': i}))

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


# DEMO
if __name__ == '__main__':
  kernel = Kernel()
  kernel.run()
