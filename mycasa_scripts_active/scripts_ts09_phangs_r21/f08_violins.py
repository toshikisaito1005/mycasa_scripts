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
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
fontsize_general = 15
fontsize_legend = 13
gals = ["ngc0628",
		"ngc3627",
		"ngc4321"]
beam = [[4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0],
        [8.0,10.0,12.0,14.0,16.0,18.0,20.0,22.0,24.0],
        [4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0]]


#####################
### functions
#####################
def get_co_intensities(image_co10,image_co21,noise_co10,noise_co21,beamfloat):
	"""
	"""
	# get image shape
	imshape = imhead(image_co10,mode="list")["shape"]
	box = "0,0," + str(imshape[0]-1) + "," + str(imshape[1]-1)
	# imval
	data_co10_tmp = imval(image_co10,box=box)["data"].flatten()
	data_co21_tmp = imval(image_co21,box=box)["data"].flatten()
	data_noise_co10_tmp = imval(noise_co10,box=box)["data"].flatten()
	data_noise_co21_tmp = imval(noise_co21,box=box)["data"].flatten()
	# cut pixel = 0
	cut_data = np.where((data_co10_tmp>0) & (data_co21_tmp>0) & (data_noise_co10_tmp>0) & (data_noise_co21_tmp>0))
	data_co10 = data_co10_tmp[cut_data]
	data_co21 = data_co21_tmp[cut_data]
	noise_co10 = data_noise_co10_tmp[cut_data]
	noise_co21 = data_noise_co21_tmp[cut_data]
	# Jy-to-K
	co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
	co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2
	data_co10_Kelvin = data_co10 * co10_jy2k
	data_co21_Kelvin = data_co21 * co21_jy2k
	data_noise_co10_Kelvin = noise_co10 * co10_jy2k
	data_noise__Kelvin = noise_co21 * co21_jy2k

	return data_co10_Kelvin, data_co21_Kelvin, data_noise_co10_Kelvin, data_noise__Kelvin


#####################
### Main Procedure
#####################
for i in range(len(gals)):
	list_co10 = []
	list_co21 = []
	list_r21 = []
	for j in range(len(beam[i])):




