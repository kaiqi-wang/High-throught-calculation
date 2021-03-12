#!/bin/bash

# extract band gap and band character

for i in *S4

do 
echo -e "$i \c" >> test.log
cat $i/band/BAND_GAP | grep "Band Character" | awk '{printf $NF}' >> test.log
echo -e "   \c" >> test.log
cat $i/band/BAND_GAP | grep "Band Gap" | awk '{print $NF}' >> test.log
done
