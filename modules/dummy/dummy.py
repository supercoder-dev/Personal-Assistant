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
    Runs the ZMQ server.

    Returns:
      None
    """

    # bind the port
    self.socket = self.zmqctx.socket(zmq.REP)
    self.socket.bind('ipc://127.0.0.1:{}'.format(port))


  def listen(self):
    """
    Listens on the port.

    Returns:
      None
    """

    while True:
      # wait for request
      message = self.socket.recv_json()

      # do
      reply = self.logic(message)

      # sebd back reply
      self.socket.send_json(reply)


  def logic(self, message):
    """
    Main logic of the module.

    Args:
      message (JSON): received data in JSON format

    Returns:
      JSON: data to send back in JSON format
    """

    # HERE GOES YOUR CODE
    print(message)

    # return result
    return message



if __name__ == '__main__':
  port = sys.argv[1]
  port = int(port)
  dm = DummyModule(port)
  dm.listen()
