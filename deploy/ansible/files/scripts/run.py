#!/usr/bin/python3

import sys
sys.path.insert(1, './Personal-Assistant/kernel/')
import kernel

kernel = kernel.Kernel()
kernel.loadConfig('/root/config.yml')
kernel.run()

