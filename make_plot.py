#!/usr/bin/env python

# source /Applications/Physics/root/bin/thisroot.sh

import sys

from ROOT import *

infilename = "ntuple.root"
if len( sys.argv ) > 1:
    infilename = sys.argv[1]

infile = TFile.Open( infilename )

treename = "data"
tree = infile.Get( treename )

ofilename = "histograms.root"
ofile = TFile.Open( ofilename, "RECREATE" )

hvolt = TH1F( "hvolt", "Photodiode voltage [V]", 20, 2.95, 3.05 )
htemp = TH1F( "htemp", "Temperature [C]", 20, 25., 29. )

tree.Draw( "volt >> hvolt" )
tree.Draw( "temperature >> htemp" )

hvolt.Write()
htemp.Write()

ofile.Close()