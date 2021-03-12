#!/bin/bash


(echo "21"; echo "211"; echo "0") | vaspkit.1.12 >> band.log
(echo "21"; echo "213"; echo "0") | vaspkit.1.12 >> band.log

## modify gap value of python scripts
gap_value=$(cat BAND_GAP | sed -n '3p' | awk '{printf "%.2f\n",$NF}')
sed -i "194s/value/$gap_value/g" ./pband_plot_spd.py

## plot band structure
(echo "red";echo "1.5";echo "0.0";echo "0.0";echo "0.0";echo "2")| python3 pband_plot_spd.py  >> band.log

## delete temporary file
rm band.log

