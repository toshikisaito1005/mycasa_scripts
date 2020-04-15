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
bins = 40
ratiorange = [0.0,2.0]
fontsize_general = 15
fontsize_legend = 13
gals = ["ngc0628",
		"ngc3627",
		"ngc4321"]
beam = [[4.0,8.0,12.0,16.0,20.0],
        [8.0,12.0,16.0,20.0,24.0],
        [4.0,8.0,12.0,16.0,20.0]]


#####################
### functions
#####################
def get_co_intensities(image_co10,image_co21,beamfloat):
	"""
	"""
	# get image shape
	imshape = imhead(image_co10,mode="list")["shape"]
	box = "0,0," + str(imshape[0]-1) + "," + str(imshape[1]-1)
	# imval
	data_co10_tmp = imval(image_co10,box=box)["data"].flatten()
	data_co21_tmp = imval(image_co21,box=box)["data"].flatten()
	# cut pixel = 0
	cut_data = np.where((data_co10_tmp>0) & (data_co21_tmp>0))
	data_co10 = data_co10_tmp[cut_data]
	data_co21 = data_co21_tmp[cut_data]
	# Jy-to-K
	co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
	co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2
	data_co10_Kelvin = data_co10 * co10_jy2k
	data_co21_Kelvin = data_co21 * co21_jy2k

	return data_co10_Kelvin, data_co21_Kelvin


#####################
### Main Procedure
#####################
#for i in range(len(gals)):
for i in [0]:
	list_co10 = []
	list_co21 = []
	list_r21 = []
	list_beamname = []
	#
	galname = gals[i]
	galname2 = gals[i].replace("ngc","for NGC ")
	dir_gal = dir_proj + galname
	for j in range(len(beam[i])):
		beamname = str(beam[i][j]).replace(".","p").zfill(4)
		print("# " + galname + " " + beamname)
		beamfloat = float(beam[i][j])
		# co intensities (K.km/s)
		image_co10 = dir_gal + "_co10/co10_" + beamname + ".moment0"
		image_co21 = dir_gal + "_co21/co21_" + beamname + ".moment0"
		# get values
		co10, co21 \
			= get_co_intensities(image_co10,image_co21,beamfloat)
		r21 = co21/co10
		# save to list
		list_co10.append(co10)
		list_co21.append(co21)
		list_r21.append(r21)
		list_beamname.append(beamname)

weights = None
beamsize = float(list_beamname[i].replace("p","."))

histo = np.histogram(list_r21[0],bins,range=ratiorange,weights=weights,density=True)
# import x and y data
x = np.delete(histo[1],-1)
y = histo[0]/(histo[0].max()*1.05)*2
xval = 10.
color = cm.brg(i/2.5)

# plot
fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(9, 4),sharey=True)
# preparation
step = (ratiorange[1]-ratiorange[0]) / bins
# plot violin
ax.plot(y+xval,x,drawstyle="steps",color=color)
ax.plot(y*-1+xval,x,drawstyle="steps",color=color)
ax.barh(x,y,height=step,lw=0,color=color,alpha=0.4,left=xval)
ax.barh(x,y*-1,height=step,lw=0,color=color,alpha=0.4,left=xval)

plt.savefig(dir_proj+"eps/"+gals[i]+"_violin_co21.png")

