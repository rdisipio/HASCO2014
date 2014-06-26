#!/usr/bin/env python

import serial
import socket
import random
import time, datetime
from flask import Flask, request

#port = "/dev/tty.usbserial"
port = "/dev/tty.usbserial-A7006Rup"

class Mode:
    offline = 0
    online  = 1

mode = Mode.offline
try:
    ser = serial.Serial( port, 9600)
    mode = Mode.online
except:
    mode = Mode.offline

nevents = 0

##################################################


def FakeInput():
    
    volt        = random.gauss( 3.0, 0.01 )
    temp        = random.gauss( 27.0, 0.3 )

    txt = "%3.2f,%3.2f" % ( volt, temp )

    return txt


##################################################


app = Flask(__name__)

@app.route("/")
def main_page():
    return "Main page"


@app.route("/get_data" )
def get_data_page():
    global nevents
    
    stream = []
    
    #nreadings = 1 #random.randint(1,10)
    #print request.form
    #nreadings = int( request.form['nreadings'] )
    nreadings = int( request.args.get('nreadings') )
    print "INFO: requested %i readings" %  nreadings

    stream += [ "0xc1a0c1a0" ]
    
    nentries = int( "0xa0a00000", 16 ) + nreadings
    stream += [ hex(nentries) ]
    
    for n in range( nreadings ):
        
        if mode == Mode.online:
            print "INFO: data taken from Arduino board connected on", port
            info = ser.readline()
        else:
            print "INFO: data from fake input"
            info = FakeInput()
    
        eventid = int( "0xe0000000", 16 ) + nevents
        stream += [ hex(eventid) ]
    
        info = info.split(',') #csv
        print len(info), info
        
        # number of seconds since the unix epoch
        # to decode:
        # d = datetime.datetime.fromtimestamp(ts)
        timestamp   = int( float( time.time() ) )
        volt        = int( 1000*float(info[0]) ) + int( "0xd0000000", 16 )
        temp        = int( 1000*float(info[1]) ) + int( "0xd1000000", 16 )
        
        stream += [ hex(timestamp) ]
        stream += [ hex(volt) ]
        stream += [ hex(temp) ]
        
        time.sleep(1.0)

        print "DEBUG: timestamp is", datetime.datetime.fromtimestamp(timestamp)

        nevents += 1

    stream += [ "0xb1eb1e0f" ]

    print stream
    
    checksum = 0
    text = ""
    for s in stream:
        text += "%s\n" % s
        checksum = checksum ^ int(s, 16)
    
    print "INFO: checksum = %s" % hex(checksum)
    text += "%s\n" % hex( checksum )
    
    return text


#####################################################


if __name__ == "__main__":
    
    ipaddress = socket.gethostbyname(socket.gethostname())
    
    print "INFO: IP address:", ipaddress
    
    app.run( host='0.0.0.0', debug=True )

