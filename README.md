HASCO2014
author: Riccardo Di Sipio <disipio@cern.ch>
=========

sw for tutor session

- Circuits described in breadboard_hasco2014.png. A thermistor and a photodiode are connected to an Arduino board
- Firmware code is in photodiode_resistor.ino . You can compile it and upload to the board with the Arduino IDE.

To run:
1) In a bash shell, launch ./post_serial.py
2) To get the readings, you can either:
- Load the web page: http://0.0.0.0:5000/get_data?nreadings=5
- Read and store in a ntuple: ./get_data [Nreadings]

then, open ntuples.root . Entries are stored in the tree called "data".

data->Draw("volt");

Also, take a look at the script called make_plot.py. To run it:
./make_plot.py 
or 
python -i make_plot.py

Enjoy.
