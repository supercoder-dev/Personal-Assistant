#!/usr/bin/python3

import sys
sys.path.insert(1, './Personal-Assistant/kernel/')
import webApplication

webApplication.kernel = webApplication.Kernel()
webApplication.kernel.loadConfig('/root/config.yml')
webApplication.kernel.run()
webApplication.app.run(host = '0.0.0.0', port = 80)
