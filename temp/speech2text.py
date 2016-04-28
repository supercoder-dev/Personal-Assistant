#! /usr/bin/python3
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
#from pocketsphinx import *

hmm = '/root/PocketSphinx/en-us/'
dic = '/root/PocketSphinx/en-us/cmudict-en-us.dict'
lm= '/root/PocketSphinx/en-us/en-us.lm.dmp'

config = Decoder.default_config()
config.set_string('-hmm', hmm)
config.set_string('-lm', lm)
config.set_string('-dict', dic)
config.set_float('-vad_threshold',2.5)
config.set_int('-nfft', 512)
config.set_float('-samprate', 16000)

decoder = Decoder(config)

import alsaaudio, wave, numpy
import sys

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
inp.setchannels(1)
inp.setrate(16000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(512)


in_speech_bf = True
decoder.start_utt()
while True:
    l,buf = inp.read()
    if buf:
        decoder.process_raw(buf, False, False)
        try:
            if  decoder.hyp().hypstr != '':
                print('Partial decoding result:' + decoder.hyp().hypstr)
        except AttributeError:
            pass
        if decoder.get_in_speech():
            sys.stdout.write('.')
            sys.stdout.flush()
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                try:
                    if  decoder.hyp().hypstr != '':
                        print('Stream decoding result:' + decoder.hyp().hypstr)
                except AttributeError:
                    pass
                decoder.start_utt()
    else:
        break
decoder.end_utt()
print('An Error occured:' + decoder.hyp().hypstr)
