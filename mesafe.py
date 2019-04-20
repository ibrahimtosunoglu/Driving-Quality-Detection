import RPi.GPIO as GPIO
import time
import sqlite3 as lite
import datetime
GPIO.setmode(GPIO.BCM)

TRIG=23
ECHO=24
con = None

con = lite.connect('logs.db')




GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
time.sleep(2)
while(True):
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start=time.time()

    while GPIO.input(ECHO)==1:
        pulse_end=time.time()

    pulse_duration=pulse_end-pulse_start

    distance=pulse_duration*17150

    distance=round(distance,2)

    if(distance>400):
        now = datetime.datetime.now()
        con.execute('INSERT INTO carpisma(ceza, tarih) values("300","'+str(now)+'");');
        con.commit()
        
    print ("uzaklık: ",distance,"cm")
    time.sleep(3)

GPIO.cleanup()

