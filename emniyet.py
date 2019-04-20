import RPi.GPIO as GPIO
import time
import math
import sqlite3 as lite
import datetime

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

con = None
try:
    con = lite.connect('logs.db')

except lite.Error, e:
    print "Error {}:".format(e.args[0])
    sys.exit(1)
while True:
    input_state = GPIO.input(4)
    if input_state == True:
        now = datetime.datetime.now()
        con.execute('INSERT INTO emniyet(ceza, tarih) values("5","'+str(now)+'");');
        con.commit()
        time.sleep(10)
    else:
        print "takili"