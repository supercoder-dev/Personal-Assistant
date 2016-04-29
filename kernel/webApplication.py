#!/usr/bin/python3

import getIntent
import queryProcessor
import os
import yaml
import flask


class Kernel:
  """
  Class maintaining run of the whole web application.
  """


  def __init__(self):
    """
    Initialization of the application.

    Returns:
      None
    """

    # load default config
    self.loadConfig('defaultConfig.yml')

    # init wrappers
    self.getIntent = getIntent.getIntent(self.getIntentConfig, 'get intent module')
    self.queryProcessor = queryProcessor.queryProcessor(self.queryProcessorConfig, 'query processing module')


  def loadConfig(self, path):
    """
    Loads config from the given path.

    Args:
      path (str): path to the config file

    Returns:
      None
    """

    configFileName = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

    with open(configFileName, 'r') as ymlfile:
      cfg = yaml.load(ymlfile)

    self.globalConfig = cfg['global']
    self.getIntentConfig = cfg['getIntent']
    self.queryProcessorConfig = cfg['queryProcessor']

    self.globalConfig['configFileName'] = configFileName

    self.getIntentConfig.update(self.globalConfig)
    self.queryProcessorConfig.update(self.globalConfig)

    # propage the new config into the module
    if hasattr(self, 'getIntent'):
      self.getIntent.loadConfig(self.getIntentConfig)
    if hasattr(self, 'queryProcessor'):
      self.queryProcessor.loadConfig(self.queryProcessorConfig)

  def run(self):
    """
    Runs the application.

    Returns:
      None
    """

    # run all processes
    self.getIntent.start()
    self.queryProcessor.start()


  def ask(self, query):
    """
    """

    intent = self.getIntent.sendReply({'request': query})['JSON']
    answer = self.queryProcessor.sendReply({'JSON': intent})['answer']
    return answer


  def stop(self):
    """
    Stops all processes that have been run.

    Returns:
      None
    """

    self.getIntent.stop()
    self.queryProcessor.stop()

    del self.getIntent
    del self.queryProcessor


app = flask.Flask('Phoenix', template_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'))

@app.route('/', methods = ['GET', 'POST'])
def index():
  if flask.request.method == 'POST':
    query = flask.request.form['query']
    answer = kernel.ask(query)
  else:
    query = None
    answer = None
  return flask.render_template('index.html', query = query, answer = answer)


# DEMO
if __name__ == '__main__':
  kernel = Kernel()
  kernel.run()
  app.run(port = 5000)
