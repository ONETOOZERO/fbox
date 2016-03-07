from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.label import Label 
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from functools import partial
from kivy.uix.image import Image 

# system librareis
import glob
from os.path import join, dirname
import piggyphoto
import time
import datetime
from threading import Thread, Lock
import numpy as np
import imp
from random import randrange, uniform, randint
from kivy.logger import Logger

from time import ctime

from subprocess import Popen
import subprocess
import os
import threading
from multiprocessing import Process
import shlex
import sys

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# SETTINGS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Folder to save the full res pictures
captureFilePath = '/full-res/'

# Folder to save the low res previews
snapshotFilePath = '/snapshot/'

# Time for countdown
timeCountdown = 3

# Picture counter. Always from 1 to 4
pictureCounter = 1

class MyWidget(Widget):
    
    camera = None


    def run_command(self, command, show_output=True, *args):
      output = ''
      self.process = subprocess.Popen(command, stdout=subprocess.PIPE)
      lines_iterator = iter(self.process.stdout.readline, "")
      for line in lines_iterator:
        output += line
        if show_output:
          self.dispatch('on_output', line)
      self.dispatch('on_complete', output)


    # Calling this function will draw a new number on the countdown
    def my_callback(screen, dt):
         global timeCountdown
         global pictureCounter
         timeCountdown = timeCountdown-1
         screen.ids.hsCountdown.text = str(timeCountdown)
         screen.ids.hsLabel.color = [1, 1, 0, 0] # black it out
         screen.ids.hsButton.color = [1, 1, 0, 0] # black it out
         screen.ids.hsButton.background_color = [1, 1, 0, 0] # black it out
         Logger.info(str(timeCountdown)) #screen.ids.hsDebug1.text = screen.ids.hsDebug1.text + str(timeCountdown)
         if (timeCountdown == 0):
              # start a new thread with the actual capturing process
             Thread(target=screen.captureImageThread, args=(screen.camera,screen.inspectImage,)).start()
             screen.ids.hsCountdown.text = ""
             timeCountdown = 5
#             screen.run_command('gphoto2 --camera "Canon EOS 60D" --capture-and-download --filename "hallo.jpg"')
              #screen.ids.hsDebug1.text = screen.ids.hsDebug1.text + str(cmd)	
             if (pictureCounter == 4):
                 preview04 = Image(source='preview04.jpg')
                 preview04.size = (400,240)
                 preview04.pos = (0,240)
                 screen.add_widget(preview04, 100)
                 Clock.unschedule(screen.my_callback)
             if (pictureCounter == 3): 
                 preview03 = Image(source='preview03.jpg')
                 preview03.size = (400,240)
                 preview03.pos = (400,0)
                 screen.add_widget(preview03, 100) # TODO move to layer 100
                 pictureCounter = 4
             if (pictureCounter == 2):
                 preview02 = Image(source='preview02.jpg')
                 preview02.size = (400,240)
                 preview02.pos = (0,0)
                 screen.add_widget(preview02, 100) # TODO move to layer 100
                 pictureCounter = 3
             if (pictureCounter == 1):
                 preview01 = Image(source='preview01.jpg')
                 preview01.size = (400,240)
                 preview01.pos = (400,240)
                 screen.add_widget(preview01, 100)
                 pictureCounter = 2
                 
             
#    def hsAddDebug(x):
#        screen.ids.hsDebug1.text = screen.ids.hsDebug1.text + str(x)
    
    
    
    # ------------------------------------------------------------------
	# Image was captured and we inspect it
	# ------------------------------------------------------------------
    def inspectImage(self, picture):

        self.state = EState.INSPECTION
		
		# make picture visible
        picture.size = (float(inspectImageWidth), float(inspectImageWidth) * picture.aspectRatio)
        picture.center_x = self.root.width / 2
        picture.center_y = self.root.height / 2
        self.latestCapturedPicture = picture
        self.root.add_widget(picture, 1)
			
		# animate image to the background - event
        Clock.schedule_once(lambda dt: self.removeLatestImage(), 3.0)
		
        pass
	
	# ------------------------------------------------------------------
	# capture the actual image to a file	
	# ------------------------------------------------------------------
    def captureImageThread(self, camera, onLoadCallback):
        timestamp = time.time()
        st = datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d_%H%M%S')
        if camera == None: st = "test"			
        filename = captureFilePath + st + ".jpg"
        self.ids.hsDebug1.text = self.ids.hsDebug1.text + str('fn: ' + filename)	
        cmd = [gphoto2, '--camera "Canon EOS 60D" --capture-and-download --filename "hallo.jpg"']
        call(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out, err = p.communicate('foo\nfoofoo\n')
        print out
        self.ids.hsDebug1.text = self.ids.hsDebug1.text + str('cmd: ' + cmd)	
    
        
    def hsInit(self):
         global timeCountdown
#         if (timeCountdown > 0):
         Clock.schedule_interval(self.my_callback, 1)

         pass
#     pass

class WidgetsApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    WidgetsApp().run()
