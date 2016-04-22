'''
Taken from : https://chrisbaume.wordpress.com/2013/02/09/aubio-alsaaudio/
Instal python-alsaaudio 
Runs for python 2.7, for python 3- compile manually: http://stackoverflow.com/questions/23190348/alsaaudio-library-not-working
But on Python3 problems with setchannels.
'''

import alsaaudio, struct
 
# constants
CHANNELS    = 1
INFORMAT    = alsaaudio.PCM_FORMAT_FLOAT_LE
RATE        = 44100
FRAMESIZE   = 1024
 
# set up audio input
recorder=alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE)
#recorder.setchannels(CHANNELS)
recorder.setrate(RATE)
recorder.setformat(INFORMAT)
recorder.setperiodsize(FRAMESIZE)
 
# main loop
runflag = 1
while runflag:
 
  # read data from audio input
  [length, data]=recorder.read()
 
 
  print (data)
