#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
 
import os
from gps import *
from time import *
import time
import threading
import math
import sqlite3 as lite
import datetime


global max_latitude
global max_longitude
global min_latitude
global min_longitude


max_latitude = 38.69805556
max_longitude = 39.27083333
min_latitude = 38.63000000
min_longitude = 39.12611111


os.system('sudo kilall gpsd')
os.system('stty -F /dev/ttyS0 9600')
os.system('sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock')
gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
      

      
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  con = None
  try:
    con = lite.connect('logs.db')


  except lite.Error, e:

    print "Error {}:".format(e.args[0])
    sys.exit(1)

  try:
    gpsp.start() # start it up
    last_speed=gpsd.fix.speed
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      os.system('clear')

 #----------------------------------------------------------------------------
      #print
      #print ' GPS reading'
      #print '----------------------------------------'
      #print 'latitude    ' , gpsd.fix.latitude
      #print 'longitude   ' , gpsd.fix.longitude
      #print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      #print 'altitude (m)' , gpsd.fix.altitude
      #print 'eps         ' , gpsd.fix.eps
      #print 'epx         ' , gpsd.fix.epx
      #print 'epv         ' , gpsd.fix.epv
      #print 'ept         ' , gpsd.fix.ept
      #print 'speed (m/s) ' , gpsd.fix.speed
      #print 'climb       ' , gpsd.fix.climb
      #print 'track       ' , gpsd.fix.track
      #print 'mode        ' , gpsd.fix.mode
      #print
      #print 'sats        ' , gpsd.satellites
 
       #set to whatever
 
 #---------------------------------------------------------------------------
      speed = gpsd.fix.speed*3.6
      print speed
      if (gpsd.fix.latitude > min_latitude and gpsd.fix.latitude < max_latitude) and (gpsd.fix.longitude > min_longitude and gpsd.fix.longitude < max_longitude):
          if (speed > 0) and (speed<80) :
              now = datetime.datetime.now()
              con.execute('INSERT INTO gps(konum, asim, tarih, ceza) values("'+str(gpsd.fix.latitude)+', '+str(gpsd.fix.longitude)+'", "'+str(speed)+'", "'+str(now)+'", 10);');
              con.commit()
          elif (speed > 80) and (speed<90) :
              now = datetime.datetime.now()
              con.execute('INSERT INTO gps(konum, asim, tarih, ceza) values("'+str(gpsd.fix.latitude)+', '+str(gpsd.fix.longitude)+'", "'+str(speed)+'", "'+str(now)+'", 20);');
              con.commit()
          elif speed > 90:
              now = datetime.datetime.now()
              con.execute('INSERT INTO gps(konum, asim, tarih, ceza) values("'+str(gpsd.fix.latitude)+', '+str(gpsd.fix.longitude)+'", "'+str(speed)+'", "'+str(now)+'", 40);');
              con.commit()
      else:
          if speed > 120:
              now = datetime.datetime.now()
              con.execute('INSERT INTO gps(konum, asim, tarih, ceza) values("'+str(gpsd.fix.latitude)+', '+str(gpsd.fix.longitude)+'", "'+str(speed)+'", "'+str(now)+'", 15);');
              con.commit()
      
      ivme = (gpsd.fix.speed - last_speed)/3
      print ivme
      if ivme > 4.604:
         now = datetime.datetime.now()
         con.execute('INSERT INTO gps_ivme(konum, asim, tarih, ceza) values("'+str(gpsd.fix.latitude)+', '+str(gpsd.fix.longitude)+'", "'+str(ivme)+'", "'+str(now)+'", 50);');
         con.commit()
      elif ivme < -4.604:
          now = datetime.datetime.now()
          con.execute('INSERT INTO gps_ivme(konum, asim, tarih, ceza) values("'+str(gpsd.fix.latitude)+', '+str(gpsd.fix.longitude)+'", "'+str(ivme)+'", "'+str(now)+'", 50);');
          con.commit()
          
      last_speed=gpsd.fix.speed
      time.sleep(3)
      

      
      
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    con.close()
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
