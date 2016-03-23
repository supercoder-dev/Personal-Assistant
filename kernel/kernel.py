#!/usr/bin/python3

import subprocess
import zmq

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

    self.zmqctx = zmq.Context()


  def run(self):
    """
    Runs the application.

    Returns:
      None
    """

    try:
      # run all processes
      self.executeActwordListener()

      # do the work
      for i in range(0, 10):
        self.actwordListenerS.send_string(str(i))
        print(self.actwordListenerS.recv().decode('utf-8'))

    finally:
      # clean after all
      self.stop()


  def stop(self):
    """
    Stops all processes that have been run.

    Returns:
      None
    """

    self.actwordListenerP.terminate()

  def executeActwordListener(self):
    """
    Executes activation word listener as independent process.

    Returns:
      None
    """

    port = 5556

    # run the process
    self.actwordListenerP = subprocess.Popen(['../modules/dummy/dummy.py', str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # create client
    self.actwordListenerS = self.zmqctx.socket(zmq.REQ)
    self.actwordListenerS.connect('tcp://127.0.0.1:{}'.format(port))


# DEMO
if __name__ == '__main__':
  kernel = Kernel()
  kernel.run()
