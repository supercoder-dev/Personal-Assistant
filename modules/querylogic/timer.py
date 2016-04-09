import sys
import multiprocessing
import time

def timer_run(mins):
    print(mins)
    minutes=int(mins)
    while minutes > 0:
        time.sleep(60)
        minutes = minutes - 1
        print (str(minutes) + " minute(s) left")

    print('wake up')

def run(mins):
    p = multiprocessing.Process(target=timer_run, args=(mins,))
    p.start()



