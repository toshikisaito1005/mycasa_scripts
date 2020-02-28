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

snr = 3.0
co10rmss = [0.013,0.048,0.015]
co21rmss = [0.017,0.024,0.017]


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
    image_tpeak = glob.glob(dir_co21 + "co21_"+beamp+".moment8")[0]
    image_r21 = glob.glob(dir_r21 + "r21_"+beamp+".moment0")[0]
    image_p21 = glob.glob(dir_r21 + "r21_"+beamp+".moment8")[0]
    image_r21mask = glob.glob(dir_r21 + "r21_"+beamp+".moment0.highlowmask")[0]

    # import data
    data_ra = r21.import_data(imagename=image_co21,mode="coords")
    data_dec = r21.import_data(imagename=image_co21,mode="coords",index=1)
    data_dist = r21.distance(
        data_ra, data_dec, pas[i], incs[i], cnt_ras[i], cnt_decs[i], scales[i])

    data_co10 = r21.import_data(imagename=image_co10,mode="data")
    data_co21 = r21.import_data(imagename=image_co21,mode="data")
    data_tpeak = r21.import_data(imagename=image_tpeak,mode="data")
    data_disp = data_co21 / (np.sqrt(2*np.pi) * data_tpeak)
    data_disp[np.isnan(data_disp)] = 0

    data_r21 = r21.import_data(imagename=image_r21,mode="data")
    data_r21mask = r21.import_data(imagename=image_r21mask,mode="data")
    data_p21 = r21.import_data(imagename=image_p21,mode="data")

    data_pco10 = r21.import_data(imagename=image_pco10,mode="data")
    data_pco21 = r21.import_data(imagename=image_pco21,mode="data")

    # calc r21 error
    data_co10snr = r21.import_data(imagename=image_co10_snr,mode="data")
    data_co21snr = r21.import_data(imagename=image_co21_snr,mode="data")
    data_r21err = data_r21 \
        * np.sqrt((1.0/data_co10snr)**2 + (1.0/data_co21snr)**2)
    data_r21err[np.isnan(data_r21err)] = 0
    data_co10snr[np.isnan(data_co10snr)] = 0
    data_co21snr[np.isnan(data_co21snr)] = 0

    # calc p21 error
    data_pco10err = co10rmss[i]
    data_pco21err = co21rmss[i]
    data_pco10snr = data_pco10 / data_pco10err
    data_pco21snr = data_pco21 / data_pco21err
    data_pco10snr[np.isnan(data_pco10snr)] = 0
    data_pco21snr[np.isnan(data_pco21snr)] = 0

    data_all = np.c_[
        data_dist.astype(int),     # 0
        data_r21,                  # 1
        #
        np.round(data_co21,2),     # 2
        np.round(data_co21snr,1),  # 3
        #
        np.round(data_co10,2),     # 4
        np.round(data_co10snr,1),  # 5
        #
        np.round(data_tpeak,2),    # 6
        np.round(data_disp,2),     # 7
        #
        data_r21mask.astype(int),  # 8
        data_p21,                  # 9
        #
        data_pco10,                # 10
        data_pco10snr,             # 11
        data_pco21,                # 12
        data_pco21snr              # 13
        ]

    np.savetxt(
        galname+"_parameter_matched_res.txt",
        data_all,
        fmt = "%.7e",
        header = "distance(pc) r21 co21(Jy/b.km/s) co21snr co21(Jy/b.km/s) co10snr peak(Jy/b) disp(km/s) r21mask p21 pco10 pco10err(Jy/b) pco21 pco21err(Jy/b)"
        )

