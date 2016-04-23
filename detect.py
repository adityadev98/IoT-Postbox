#!/usr/bin/python

import os
import time
import random
import RPi.GPIO as GPIO
from send_gmail_attachment import sendMailWithAttachments

def flash(d):
      GPIO.output(11, False)
      time.sleep(d)
      GPIO.output(11, True)
      time.sleep(d)

# use Pi board pin numbers with GPIO.BOARD
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:

  while not os.path.exists('/dev/video0'):
  	print "No Camera"

  print "ready"

  go = not(GPIO.input(7))
  stop = not(GPIO.input(12))

  if go:


    print "taking picture"
    filename = "webcam%s.jpg" % (time.strftime('%d%b%H%M%S'))
    pathname = "/home/pi/pictures/" + filename
    command = "fswebcam -r 640x480 " + pathname
    os.system(command)

    if os.path.isfile(pathname):
        print "picture ok"
        time.sleep(0.5)

        print "Emailing"
    
    # Details of the email ID to which the email is to be sent
        sendMailWithAttachments( ["emailid@server.com"], 
                                "Image from the Raspberry Pi",
                                "Someone took a picture.",
                                [pathname] )
        print "Done"
       
    else:
        print "picture failed"        
    time.sleep(0.5)
    print "ready"

  if stop:

    print "goodbye"
    GPIO.cleanup()
    exit()

  time.sleep(0.1)
