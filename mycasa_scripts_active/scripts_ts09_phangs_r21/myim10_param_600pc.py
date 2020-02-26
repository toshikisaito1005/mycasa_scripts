import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
from scipy.optimize import curve_fit
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
snr = 5
dir_data = "/Users/saito/data/phangs/co_ratio/"
gals = ["ngc0628", "ngc3627", "ngc4254", "ngc4321"]
beam = [[13.6],[15.0],[8.0],[8.2]]



#####################
### functions
#####################
def process_fits(image,txtdata,mode,index=0):
    """
    """
    done = glob.glob(txtdata)
    if not done:
        ### import data
        image_r = imhead(image,mode="list")["shape"][0] - 1
        image_t = imhead(image,mode="list")["shape"][1] - 1
        
        value = imval(image,box="0,0,"+str(image_r)+","+str(image_t))
        
        if mode=="coords":
            value_masked = value[mode][:,:,index]
        else:
            value_masked = value[mode]
    
        value_masked_1d = value_masked.flatten()
        
        np.savetxt(txtdata, value_masked_1d)

def import_data(dir_data,
                gal,
                line,
                suffix,
                ext,
                mode,
                txtname,
                index=0):
    """
    """
    image = dir_data+line+"_"+suffix+"."+ext
    txtdata = dir_data+"f04_"+line+"_"+suffix+"."+txtname+".txt"
    process_fits(image,txtdata,mode,index=index)
    data = np.loadtxt(txtdata)

    return data


#####################
### parameters
#####################
for i in range(len(gals)):
    galname = gals[i]
    dir_co21 = dir_data + galname + "_co21/"
    dir_r21 = dir_data + galname + "_r21/"
    dir_wise = dir_data + galname + "_co21/"






