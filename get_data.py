#!/usr/bin/env python

# source /Applications/Physics/root/bin/thisroot.sh

import sys
import urllib2
from ROOT import *
from array import array
#import numpy as np
import time, datetime

class EventWrapper:
    def __init__( self ):
        self.reset()
    def reset( self ):
        #array( 'i', [0] )
        self.id             = array( 'i', [0] ) # np.zeros( 1, dtype=int)
        self.timestamp      = array( 'i', [0] ) # np.zeros( 1, dtype=int)
        self.volt           = array( 'f', [0] ) # np.zeros( 1, dtype=float)
        self.temperature    = array( 'f', [0] ) # np.zeros( 1, dtype=float)
        self.startline      = -666


ew_id             = array( 'i', [0] ) # np.zeros( 1, dtype=int)
ew_timestamp      = array( 'i', [0] ) # np.zeros( 1, dtype=int)
ew_volt           = array( 'f', [0] ) # np.zeros( 1, dtype=float)
ew_temperature    = array( 'f', [0] ) # np.zeros( 1, dtype=float)
ew_startline      = -666

def ew_reset():
    ew_id[0]        = -1
    ew_timestamp    = -1
    ew_volt         = 0.
    ew_temperature  = -666.
    ew_startline    = -666

#wpage = "http://127.0.0.1:5000/photodiode"
wpage = "http://0.0.0.0:5000/get_data"

ndata2read = 1
if len(sys.argv) > 1:
    ndata2read = int( sys.argv[1] )
print "INFO: no. of data to be read:", ndata2read

ofilename = "ntuple.root"
if len(sys.argv) > 2:
    ofilename = sys.argv[2]
ofile = TFile.Open( ofilename, 'recreate' )

#ew  = EventWrapper()
ew_reset()
#ntuple = TNtuple( "data", "Arduino sensors data", "id:timestamp:volt:temperature" )
ntuple = TTree( "data", "Arduino sensors data" )
ntuple.Branch( "id",            ew_id,            "id/I" )
ntuple.Branch( "timestamp",     ew_timestamp,     "timestamp/I" )
ntuple.Branch( "volt",          ew_volt,          "volt/F" )
ntuple.Branch( "temperature",   ew_temperature,   "temperature/F" )

for n in range( ndata2read ):
    print "INFO: data request", n
    
    fetchpage = "%s?nreadings=5" % (wpage)
    downloaded_data  = urllib2.urlopen( fetchpage )
    
    nreadings = -1
    
    nl = 0
    for line in downloaded_data.readlines():
        line = line.strip()
        
        if line == "0xc1a0c1a0":
            # new request
            ew_reset()
        
        if line.startswith( "0xa0a0" ):
            nreadings = int(line[-4:], 16 )
            print "INFO: nreadings =", nreadings
        
        if line.startswith( "0xe0" ):
            # new event
            ew_reset()
            ew_startline = nl
            ew_id[0] = int( line[3:], 16 )
            print "INFO: new event detected. id =", ew_id[0]
        
        if nl == (ew_startline + 1):
            ew_timestamp[0] = int( line, 16 )
            print "INFO: event ts:", ew_timestamp[0], datetime.datetime.fromtimestamp(ew_timestamp[0])
        
        if nl == (ew_startline + 2):
            ew_volt[0] = float( int(line[4:], 16) ) / 1000.
            print "INFO: volt = %3.1f [V]" % ew_volt[0]

        if nl == (ew_startline + 3):
            ew_temperature[0] = float( int(line[4:], 16) ) / 1000.
            print "INFO: temperature = %3.1f [C]" % ew_temperature[0]

            ntuple.Fill()
#ntuple.Fill( ew_id, ew_timestamp, ew_volt, ew_temperature )

        if line == "0xb1eb1e0f":
            pass
            #print "%i) |%s|" % (nl, line )
        nl += 1

ntuple.Write()
ofile.Close()