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
dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628", "ngc3627", "ngc4321"]
beam = [13.6, 15.0, 8.2]



#####################
### functions
#####################
def import_data(
    imagename,
    mode,
    index=0,
    ):
    """
    """
    image_r = imhead(imagename,mode="list")["shape"][0] - 1
    image_t = imhead(imagename,mode="list")["shape"][1] - 1
    value = imval(imagename,box="0,0,"+str(image_r)+","+str(image_t))

    if mode=="coords":
        value_masked = value[mode][:,:,index]
    else:
        value_masked = value[mode]

    value_masked_1d = value_masked.flatten()

    return value_masked_1d


#####################
### parameters
#####################
for i in range(len(gals)):
    galname = gals[i]
    beamp = str(beam[i]).replace(".","p").zfill(4)
    dir_co21 = dir_data + galname + "_co21/"
    dir_r21 = dir_data + galname + "_r21/"
    dir_wise = dir_data + galname + "_wise/"

    # imagename
    image_co21 = glob.glob(dir_co21 + "co21_"+beamp+".moment0")[0]
    image_r21 = glob.glob(dir_r21 + "r21_"+beamp+".moment0")[0]
    image_r21mask = glob.glob(dir_r21 + "r21_"+beamp+".moment0.highlowmask")[0]
    image_w1 = glob.glob(dir_wise + galname+"_w1_gauss"+beamp+".image")[0]
    image_w2 = glob.glob(dir_wise + galname+"_w2_gauss"+beamp+".image")[0]
    image_w3 = glob.glob(dir_wise + galname+"_w3_gauss"+beamp+".image")[0]

    # import data
    data_ra = import_data(imagename=image_co21,mode="coords")
    data_dec = import_data(imagename=image_co21,mode="coords",index=1)
    data_co21 = import_data(imagename=image_co21,mode="data")
    data_r21 = import_data(imagename=image_r21,mode="data")
    data_w1 = import_data(imagename=image_w1,mode="data")
    data_w2 = import_data(imagename=image_w2,mode="data")
    data_w3 = import_data(imagename=image_w3,mode="data")



