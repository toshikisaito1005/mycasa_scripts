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
beam = [13.6, 15.0, 9.5]
scales = [44/1.0, 52/1.3, 103/1.4]
cnt_ras = [24.174, 170.063, 185.729]
cnt_decs = [15.783, 12.9914, 15.8223]
pas = [180-21.1, 180-172.4, 180-157.8]
incs = [90-8.7, 90-56.2, 90-35.1]


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
        value_masked = value[mode][:,:,index] * 180 / pi
    else:
        value_masked = value[mode]

    value_masked_1d = value_masked.flatten()

    return value_masked_1d

def distance(x, y, pa, inc, ra_cnt, dec_cnt, scale):
    tilt_cos = math.cos(math.radians(pa))
    tilt_sin = math.sin(math.radians(pa))
    
    x_tmp = x - ra_cnt
    y_tmp = y - dec_cnt
    
    x_new = (x_tmp*tilt_cos - y_tmp*tilt_sin)
    y_new = (x_tmp*tilt_sin + y_tmp*tilt_cos) * 1/math.sin(math.radians(inc))
    
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale # arcsec * pc/arcsec
    
    return r


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
    image_tpeak = glob.glob(dir_co21 + "co21_"+beamp+".moment8")[0]
    image_r21 = glob.glob(dir_r21 + "r21_"+beamp+".moment0")[0]
    image_r21mask = glob.glob(dir_r21 + "r21_"+beamp+".moment0.highlowmask")[0]
    image_w1 = glob.glob(dir_wise + galname+"_w1_gauss"+beamp+".image")[0]
    image_w2 = glob.glob(dir_wise + galname+"_w2_gauss"+beamp+".image")[0]
    image_w3 = glob.glob(dir_wise + galname+"_w3_gauss"+beamp+".image")[0]

    # import data
    data_ra = import_data(imagename=image_co21,mode="coords")
    data_dec = import_data(imagename=image_co21,mode="coords",index=1)
    data_dist = distance(
        data_ra, data_dec, pas[i], incs[i], cnt_ras[i], cnt_decs[i], scales[i])

    data_co21 = import_data(imagename=image_co21,mode="data")
    data_tpeak = import_data(imagename=image_tpeak,mode="data")
    data_disp = data_co21 / (np.sqrt(2*pi) * data_tpeak)
    data_disp[np.isnan(data_disp)] = 0

    data_r21 = import_data(imagename=image_r21,mode="data")
    data_w1 = import_data(imagename=image_w1,mode="data")
    data_w2 = import_data(imagename=image_w2,mode="data")
    data_w3 = import_data(imagename=image_w3,mode="data")

    np.set_printoptions(precision=4, floatmode='maxprec')
    data_all = np.c_[
        data_dist,data_r21,data_co21,data_tpeak,data_disp,data_w1,data_w2,data_w3]

    np.savetxt(
        galname+"_parameter_600pc.txt",
        data_all,
        header = "distance(pc) r21 co21(Jy/b.km/s) peak(Jy/b) disp(km/s) w1(Jy/b) w2(Jy/b) w3(Jy/b)"
        )

