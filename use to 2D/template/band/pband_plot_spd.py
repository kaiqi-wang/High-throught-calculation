#!/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib as mpl
import os
mpl.use('Agg')  # silent mode
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import sys
import math

#------------------- rc.Params 1----------------------
plt.rcParams['xtick.direction'] = 'out'
plt.rcParams['ytick.direction'] = 'out'

#------------------- Data Read ----------------------

def getelementinfo():
    try:
        with open("POSCAR",'r') as reader:
            line_s=reader.readlines()
    except:
        print("No POSCAR found!")
    try:    
        element_s=line_s[5].rstrip('\r\n').rstrip('\n')
        elements=element_s.split()
    except:
        print("POSCAR element line is wrong!")

    data = {}
    for i in range(len(elements)):
        data[elements[i]]=np.loadtxt("PBAND_" + elements[i] + ".dat")
        derta=float(input("the difference of gap value between PBE and correct gap value:\n"))
        s=len(data[elements[i]][:,0])
        for j in range(0,s) :         
           if data[elements[i]][j][1] >= 0 :
              data[elements[i]][j][1] +=  derta
    return data,elements

def getHighSymmetryPoints():
    hsp = np.loadtxt("KLABELS", dtype=np.string_, skiprows=1, usecols=(0, 1))
    group_labels = hsp[:-1, 0].tolist()
    group_labels = [i.decode('utf-8', 'ignore') for i in group_labels]
    for index in range(len(group_labels)):
        if group_labels[index] == "GAMMA":
            group_labels[index] = u"Γ"
    return group_labels, hsp


def getPbandData(data, scaler):
    kpt = data[:, 0]  # kpath
    eng = data[:, 1]  # energy level
    wgt_s = data[:, 2] * scaler  # weight, 20 is enlargement factor
    #wgt_s = maxminnorm(wgt_s) * scaler  # Normlized

    wgt_py = data[:, 3] * scaler  # weight, 20 is enlargement factor
    #wgt_py = maxminnorm(wgt_py)*scaler
    wgt_pz = data[:, 4] * scaler  # weight, 20 is enlargement factor
    #wgt_pz = maxminnorm(wgt_pz)*scaler

    wgt_px = data[:, 5] * scaler  # weight, 20 is enlargement factor
    #wgt_px = maxminnorm(wgt_px)*scaler

    wgt_p = np.array(wgt_py) + np.array(wgt_px) + np.array(wgt_pz)
    #wgt_p = maxminnorm(wgt_p) * scaler  # Normlized


    wgt_dxy = data[:, 6] * scaler
    #wgt_dxy = maxminnorm(wgt_dxy) * scaler  # Normlized

    wgt_dyz = data[:, 7] * scaler
    #wgt_dyz = maxminnorm(wgt_dyz) * scaler
    wgt_dz2 = data[:, 8] * scaler
    #wgt_dz2 = maxminnorm(wgt_dz2) * scaler
    wgt_dxz = data[:, 9] * scaler
    #wgt_dxz = maxminnorm(wgt_dxz) * scaler
    wgt_dx2y2 = data[:, 10] * scaler
    #wgt_dx2y2 = maxminnorm(wgt_dx2y2) * scaler
    wgt_d = np.array(wgt_dxy) + np.array(wgt_dyz) + np.array(wgt_dz2) \
             + np.array(wgt_dxz) + np.array(wgt_dx2y2)
    #wgt_d = maxminnorm(wgt_d) * scaler  # Normlized

    #wgt_tot = maxminnorm(data[:, 11]) * scaler
    wgt_tot = data[:, 11] * scaler
    return kpt, eng, wgt_s, wgt_py, wgt_pz, wgt_px, wgt_p, wgt_dxy,  \
            wgt_dyz, wgt_dz2, wgt_dxz, wgt_dx2y2, wgt_d, wgt_tot

######read chemical formula
element=[];formula=""
with open('POSCAR','r') as reader :
    lines = reader.readlines()[5:7]
for i in lines :
    s=i.split()
    element.append(s)
lens=len(element[0])
for j in range(lens) :
    if element[1][j] == "1":
       element[1][j] = "" 
    # formula += element[0][j]+element[1][j]
    formula += element[0][j]+str(math.floor(int(element[1][j])/2))
    
#------------------- Pband Plot ----------------------


class pbandplots(object):
    def __init__(self,lwd,op,scaler,energy_limits,font,dpi,figsize,corlor0):
        from matplotlib import pyplot as plt
        self.data,self.elements=getelementinfo()
        self.group_labels, self.hsp = getHighSymmetryPoints()    # HighSymmetryPoints_labels 
        self.x = [float(i) for i in self.hsp[:-1, 1].tolist()]   # HighSymmetryPoints_coordinate
        self.lwd=lwd ; self.op=op;self.scaler=scaler;self.energy_limits=energy_limits
        self.font=font;self.dpi=dpi;self.figsize=figsize
        self.corlor0=corlor0 
    def plotfigure(self,ax, kpt, eng, title):
        ax.plot(kpt, eng, color=self.corlor0, lw=self.lwd, linestyle='-', alpha=1)
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.25))  # determine the minor locator of y-axis
        ax.set_ylim(self.energy_limits)
        ytick = np.arange(self.energy_limits[0], self.energy_limits[1], 2)  # determine the major loctor of y-axis
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))  # determine the major loctor of y-axis
        # a = int(len(ytick) / 2)
        # plt.yticks(np.insert(ytick, a, 0))
        ax.set_xticks(self.x)
        plt.yticks(fontsize=self.font['size']-2,fontname=self.font['family'],fontweight=self.font['weight'])
        plt.ylabel(r'Energy (eV)', fontdict=self.font)
        # plt.suptitle(title)
        ax.set_xticklabels(self.group_labels, rotation=0, fontsize=self.font['size']-2,fontname=self.font['family'],fontweight=self.font['weight'])
        #ax.axhline(y=0, xmin=0, xmax=1, linestyle='--', linewidth=0.5, color='k') # determine the line style of E-fermi energy
        for i in self.x[1:-1]:
            ax.axvline(x=i, ymin=0, ymax=1, linestyle='--', linewidth=0.5, color='k') # determine the line style of HighSymmetry lines
        ax.set_xlim((self.x[0], self.x[-1]))
        return plt


    def plotPbandAllElements(self):
        from matplotlib import pyplot as plt
        print("start plot PBAND including Elements...")
        colorcode = ['pink', 'orange', 'cyan', 'blue', 'red']
        markerorder=['v', '*', 'o', '>', 'p']
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111)
        # ax.text(0.2,0.5,'gap = 1.55 eV',fontdict=font)
        ###设置图像题目
        # ax.set_title('$\mathregularformula$',fontsize=font['size'],fontname=font['family'])
        ax.set_title('$\mathregularformula$' + '   ' + 'Eg = 0.01 eV',fontsize=font['size'],fontname=font['family'])
        for elementorder in range(len(self.elements)):
            #del wgt_s, wgt_py, wgt_pz, wgt_px, wgt_p, wgt_dxy, wgt_dyz, wgt_dz2, wgt_dxz, wgt_dx2y2, wgt_d, wgt_tot
            kpt, eng, wgt_s, wgt_py, wgt_pz, wgt_px, wgt_p, wgt_dxy, wgt_dyz, wgt_dz2, wgt_dxz, wgt_dx2y2, wgt_d, wgt_tot \
                = getPbandData(self.data[self.elements[elementorder]],self.scaler)
            ax.scatter(kpt, eng, wgt_tot, color=colorcode[elementorder], edgecolor=colorcode[elementorder], \
                       linewidths=0.2, alpha=self.op-elementorder*0.2,marker=markerorder[elementorder])

        if len(self.elements) == 5:
            ax.legend(('' + self.elements[0] + '', '' + self.elements[1] + '', '' + self.elements[2] + '', '' + self.elements[3] + '', '' + self.elements[4] + ''),\
                      loc='best', shadow=False, labelspacing=0.1)
        elif len(self.elements) == 4:
            ax.legend(('' + self.elements[0] + '', '' + self.elements[1] + '', '' + self.elements[2] + '', '' + self.elements[3] + ''),\
                      bbox_to_anchor=(0.13,0.64),handlelength=1.0,handleheight=0.2,loc='center', shadow=False, labelspacing=0.1)
        elif len(self.elements) == 3:
            ax.legend(('' + self.elements[0]+'', '' + self.elements[1] + '', '' + self.elements[2] + ''),\
                      loc='best', shadow=False, labelspacing=0.1)
        elif len(self.elements) == 2:
            ax.legend(('' + self.elements[0] + '', '' + self.elements[1] + ''), \
                      loc='best', shadow=False, labelspacing=0.1)
        elif len(self.elements) == 1:
            ax.legend(('' + self.elements[0] + ''), \
                      loc='best', shadow=False, labelspacing=0.1)
        title0=" "
        for atom in range(len(self.elements)):
            title0=self.elements[atom] + title0 
        ax.spines['bottom'].set_linewidth(1.2)
        ax.spines['top'].set_linewidth(1.2)
        ax.spines['right'].set_linewidth(1.2)
        ax.spines['left'].set_linewidth(1.2)
        plt = self.plotfigure(ax, kpt, eng, title0)
        # plt = self.plotfigure(ax, kpt, eng, self.elements[elementorder])
        # plt.subplots_adjust(top=0.950,bottom=0.110,left=0.165,right=0.855,wspace=0)
        plt.savefig('Projected_Band.png', bbox_inches='tight', pad_inches=0.1, dpi=self.dpi)
        #del ax, fig



    def plottotalBands(self):
        from matplotlib import pyplot as plt
        print("start plot total BANDs ...")
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111)
        datas=np.loadtxt('BAND.dat',dtype=np.float64)
        kpt, eng, wgt_s, wgt_py, wgt_pz, wgt_px, wgt_p, wgt_dxy, wgt_dyz, wgt_dz2, wgt_dxz, wgt_dx2y2, wgt_d, wgt_tot \
        = getPbandData(self.data[self.elements[0]],self.scaler) 
        title0=" "
        for atom in range(len(self.elements)):
            title0=self.elements[atom] + title0 
        ax.set_title('$\mathregularformula$' + '   ' + 'Eg = value eV',fontsize=font['size'],fontname=font['family'],fontweight=self.font['weight'])
        ax.spines['bottom'].set_linewidth(1.2)
        ax.spines['top'].set_linewidth(1.2)
        ax.spines['right'].set_linewidth(1.2)
        ax.spines['left'].set_linewidth(1.2)
        plt = self.plotfigure(ax, kpt, eng, title0)
        # plt = self.plotfigure(ax, kpt, eng, self.elements[elementorder])
        # plt.subplots_adjust(top=0.950,bottom=0.110,left=0.165,right=0.855,wspace=0)
        plt.savefig('Total_Band.png', bbox_inches='tight', pad_inches=0.1, dpi=self.dpi)
        #del ax, fig

if __name__ == "__main__":
    
    #___________________________________SETUP____________________________________
    
        
    print("    ****************************************************************")
    print("    *     Type of bandstructures are obtained as below:            *") 
    print("    * 1).For total bandstructure of all atoms in one figure        *")
    print("    * 2).For a total bandstructure                                 *")
    print("    ****************************************************************")
    print("                       (^o^)GOOD LUCK!(^o^)                         ")
    print( "\n")
    
    print( " Band plot initialization... ")
    print( "*******************************************************************")
    print("Please set the color and width of line in figure,input line=0.2")
    print(" and color = 'black' for choice 1->5,input line >= 1 and color =")
    print(" 'red','blue' or .... for choice 6")
    print( "********************************************************************")

    corlor0 = str(input("Input color = ? according to your choice number:"))
    lwd = float(input("Input line =? according to your choice number:"))
    print("*********************************************************************")
    print(  "Which kind of bandstructure do you need plot ?")
    print(  "Please type in a number to select a function: e.g.1, 2 ....,")
    print("*********************************************************************")

    
    op = 1  # Max alpha blending value, between 0 (transparent) and 1 (opaque).
    scaler = 80  # Scale factor for projected band
    energy_limits=(-1, 1)  # energy ranges for PBAND
    dpi=600          # figure_resolution
    figsize=(3, 5)   #figure_inches
    font = {'family' : 'Arial', 
        'color'  : 'black',
        'weight' : 'bold',
        'size' : 13.0,
        }       #FONT_setup
    pband_plots=pbandplots(lwd,op,scaler,energy_limits,font,dpi,figsize,corlor0)
	
    try:
        bandtype = int(input("Input number--->"))
    except ValueError:
        raise ValueError(" You have input wrong ! Please rerun this code !")
	
    if bandtype == 1:
        pband_plots.plotPbandAllElements()  # plot pband for all element in one figure
    elif bandtype == 2:
        pband_plots.plottotalBands()	
    else :
        print(" You have input wrong ! Please rerun this code !" )
        sys.exit(0)
