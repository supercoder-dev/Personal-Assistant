install:
	1. git clone https://github.com/MycroftAI/mimic.git
	2. cd mimic
	3. ./configure
	4. make


Requirements
	1. make
	2. gcc
	3. libasound2-dev


Get installed voices:
	./bin/mimic -lv
	for change voice you must call config of TextToSpeach module (config.voice) where is written name of voice.
