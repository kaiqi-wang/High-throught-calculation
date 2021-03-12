#!/bin/bash

echo $(date +%F%n%T) >> ./job

for B_ele in Ta Nb Sb V Bi As Mo Tc Ru Rh W Re Pt

do
	A_ele=La
	C_ele=S
	cp -r ./template ./${A_ele}${B_ele}${C_ele}4
	cd ./${A_ele}${B_ele}${C_ele}4/relax
	sed -i "194s/formula/{{$A_ele}{$B_ele}{$C_ele}_4}/g" ../band/pband_plot_spd.py
	sed -i "6s/A_ele/${A_ele}/g" ./POSCAR
	sed -i "6s/B_ele/${B_ele}/g" ./POSCAR
	sed -i "6s/C_ele/${C_ele}/g" ./POSCAR
	sed -i "2s/name/${A_ele}${B_ele}${C_ele}4/g" ./vasp.5.4.4
	qsub ./vasp.5.4.4
	cd $OLDPWD
done
