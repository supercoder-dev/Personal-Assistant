#!/usr/bin/python3

import zmq
import time
import sys

class DummyModule:
  """
  Dummy module class, which just sends back what it receives.
  """

  def __init__(self, port):
    """
    Constructor of the dummy class.

    Args:
      port (int): port of the server

    Returns:
      None
    """

    self.port = port
    self.zmqctx = zmq.Context()
    self.runServer()


  def runServer(self):
    """
    Runs the ZQM server.

    Returns:
      None
    """

    self.socket = self.zmqctx.socket(zmq.REP)
    print('ipc://127.0.0.1:{}'.format(port))
    self.socket.bind('ipc://127.0.0.1:{}'.format(port))


  def listen(self):
    """
    Listens on the port.

    Returns:
      None
    """

    while True:
      message = self.socket.recv().decode('utf-8')
      print(message)
      time.sleep(1)
      self.reply('Reply: ' + message)


  def reply(self, message):
    """
    Sends reply back to client.

    Args:
      message (str): message to send

    Returns:
      None
    """

    self.socket.send_string(str(message))


if __name__ == '__main__':
  port = sys.argv[1]
  port = int(port)
  dm = DummyModule(port)
  dm.listen()
