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
import scripts_phangs_r21 as r21
plt.ioff()


#####################
### parameters
#####################
dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628", "ngc3627", "ngc4321"]
beam = [4.0, 8.0, 4.0]
scales = [44/1.0, 52/1.3, 103/1.4]
cnt_ras = [24.174, 170.063, 185.729]
cnt_decs = [15.783, 12.9914, 15.8223]
pas = [180-21.1, 180-172.4, 180-157.8]
incs = [90-8.7, 90-56.2, 90-35.1]

co10rmss = [0.012,0.041,0.015]
co21rmss = [0.016,0.023,0.016]


#####################
### parameters
#####################
for i in range(len(gals)):
    galname = gals[i]
    beamp = str(beam[i]).replace(".","p").zfill(4)
    dir_co21 = dir_data + galname + "_co21/"
    dir_co10 = dir_data + galname + "_co10/"
    dir_r21 = dir_data + galname + "_r21/"
    dir_wise = dir_data + galname + "_wise/"

    # imagename
    image_co10 = glob.glob(dir_co10 + "co10_"+beamp+".moment0")[0]
    image_co10_snr = glob.glob(dir_co10 + "co10_"+beamp+".moment0.snratio")[0]
    image_co21 = glob.glob(dir_co21 + "co21_"+beamp+".moment0")[0]
    image_co21_snr = glob.glob(dir_co21 + "co21_"+beamp+".moment0.snratio")[0]
    image_pco10 = glob.glob(dir_co10 + "co10_"+beamp+".moment8")[0]
    image_pco21 = glob.glob(dir_co21 + "co21_"+beamp+".moment8")[0]
    image_r21 = glob.glob(dir_r21 + "r21_"+beamp+".moment0")[0]
    image_p21 = glob.glob(dir_r21 + "r21_"+beamp+".moment8")[0]
    image_r21mask = glob.glob(dir_r21 + "r21_"+beamp+".moment0.highlowmask")[0]
    image_gmcmask = glob.glob(dir_r21 + "cprops_"+beamp+".mask.fits")[0]

    # import data
    data_ra = r21.import_data(imagename=image_co21,mode="coords")
    data_dec = r21.import_data(imagename=image_co21,mode="coords",index=1)
    data_co10 = r21.import_data(imagename=image_co10,mode="data")
    data_co10snr = r21.import_data(imagename=image_co10_snr,mode="data")
    data_co21 = r21.import_data(imagename=image_co21,mode="data")
    data_co21snr = r21.import_data(imagename=image_co21_snr,mode="data")
    data_pco10 = r21.import_data(imagename=image_pco10,mode="data")
    data_pco21 = r21.import_data(imagename=image_pco21,mode="data")
    data_r21 = r21.import_data(imagename=image_r21,mode="data")
    data_p21 = r21.import_data(imagename=image_p21,mode="data")
    data_r21mask = r21.import_data(imagename=image_r21mask,mode="data")
    data_gmcmask = r21.import_data(imagename=image_gmcmask,mode="data")

    # masking
    cut_co10 = (data_co10 > 0)
    cut_co21 = (data_co21 > 0)
    cut_pco10 = (data_pco10 > 0)
    cut_pco21 = (data_pco21 > 0)
    cut_all = np.where((cut_co10) & (cut_co21) * (cut_pco10) & (cut_pco21))

    # cut data
    data_ra = data_ra[cut_all]
    data_dec = data_dec[cut_all]
    data_co10 = data_co10[cut_all]
    data_co10snr = data_co10snr[cut_all]
    data_co21 = data_co21[cut_all]
    data_co21snr = data_co21snr[cut_all]
    data_pco10 = data_pco10[cut_all]
    data_pco21 = data_pco21[cut_all]
    data_r21 = data_r21[cut_all]
    data_p21 = data_p21[cut_all]
    data_r21mask = data_r21mask[cut_all]
    data_gmcmask = data_gmcmask[cut_all]

    # rms per channel
    data_pco10err = co10rmss[i] * np.ones(len(data_pco10))
    data_pco21err = co21rmss[i] * np.ones(len(data_pco10))

    # calc parameters
    data_dist = r21.distance(data_ra, data_dec, pas[i], incs[i], cnt_ras[i], cnt_decs[i], scales[i])
    data_co10err = data_co10 / data_co10snr
    data_co21err = data_co21 / data_co21snr
    data_r21err = data_r21 * np.sqrt((1.0/data_co10snr)**2 + (1.0/data_co21snr)**2)
    data_p21err = data_r21 * np.sqrt((data_pco10err/data_pco10)**2 + (data_pco21err/data_pco21)**2)
    #
    data_all = np.c_[
        data_dist.astype(int), # 0
        data_co10,             # 1
        data_co10err,          # 2
        data_co21,             # 3
        data_co21err,          # 4
        data_pco10,            # 5
        data_pco10err,         # 6
        data_pco21,            # 7
        data_pco21err,         # 8
        data_r21,              # 9
        data_r21err,           # 10
        data_p21,              # 11
        data_p21err,           # 12
        data_r21mask,          # 13
        data_ra * 3600 * scales[i],  # 14
        data_dec * 3600 * scales[i], # 15
        data_gmcmask,          # 16
        ]

    np.savetxt(
        dir_data + "eps/" + galname + "_parameter_matched_res.txt",
        data_all,
        fmt = "%.7f",
        header = "distance(pc) co10(Jy/b.km/s) co10err co21(Jy/b.km/s) co21err r21 r21err p21 p21err"
        )

