#!/usr/bin/env python

import sys
import random
import time, datetime

nreadings = 10000
if len(sys.argv) > 1:
    nreadings = int( sys.argv[1] )

print "INFO: requested %i readings" %  nreadings

###################################

def FakeInput():
    
    volt        = random.gauss( 3.0, 0.01 )
    temp        = random.gauss( 27.0, 0.3 )
    
    txt = "%3.2f,%3.2f" % ( volt, temp )
    
    return txt

###################################

nevents = 0
stream  = [ "0xc1a0c1a0" ]

nentries = int( "0xa0a00000", 16 ) + nreadings
stream += [ hex(nentries) ]

for n in range( nreadings ):
    
    info = FakeInput()
    
    eventid = int( "0xe0000000", 16 ) + nevents
    stream += [ hex(eventid) ]
    
    info = info.split(',') #csv
    
    # number of seconds since the unix epoch
    # to decode:
    # d = datetime.datetime.fromtimestamp(ts)
    timestamp   = int( float( time.time() ) )
    volt        = int( 1000*float(info[0]) ) + int( "0xd0000000", 16 )
    temp        = int( 1000*float(info[1]) ) + int( "0xd1000000", 16 )
    
    stream += [ hex(timestamp) ]
    stream += [ hex(volt) ]
    stream += [ hex(temp) ]
    
#print "DEBUG: timestamp is", datetime.datetime.fromtimestamp(timestamp)
    
    nevents += 1

stream += [ "0xb1eb1e0f" ]

checksum = 0
text = ""
for s in stream:
    text += "%s\n" % s
    checksum = checksum ^ int(s, 16)

#print "INFO: checksum = %s" % hex(checksum)
stream += [ hex( checksum ) ]

ofile = open( "stream.dat", 'w' )
for line in stream:
    ofile.write( "%s\n" % line )
ofile.close()