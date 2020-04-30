import os
import re
import sys
import glob
import scipy
import matplotlib.pyplot as plt
plt.ioff()

dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/ngc0628_r21/"
maskname = dir_data + "r21_04p0.moment0.highlowmask"
imagename = dir_data + "r21_04p0.moment0"
bins=150


### maskname
shape = imhead(maskname,mode="list")["shape"]
box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
data = imval(maskname,box=box)
data = data["data"][data["mask"]==True]
mask = data.flatten()


### imagename
data = imval(imagename,box=box)
data = data["data"][data["mask"]==True]
data = data.flatten()
#
data_low = data[mask==-1]
data_mid = data[mask==0]
data_high = data[mask==1]


###
plt.figure()#figsize=(10,10))
plt.rcParams["font.size"] = 14
plt.grid(axis="x")

plt.hist(data_low,range=[0,1.5],bins=bins,color="blue",lw=0,alpha=0.5)
plt.hist(data_mid,range=[0,1.5],bins=bins,color="green",lw=0,alpha=0.5)
plt.hist(data_high,range=[0,1.5],bins=bins,color="red",lw=0,alpha=0.5)

plt.savefig(dir_data+"../eps/fig_mask_histo.png",dpi=100)
