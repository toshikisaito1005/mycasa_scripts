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


### maskname
shape = imhead(maskname,mode="list")["shape"]
box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
data = imval(maskname,box=box)
data = data["data"][data["mask"]==True]
data = data.flatten()
#
mask_low = data[data<0]
mask_mid = data[data==0]
mask_high = data[data>0]

### imagename
data = imval(imagename,box=box)
data = data["data"][data["mask"]==True]
data = data.flatten()
#
data_low = data[mask_low]


###
plt.figure()#figsize=(10,10))
plt.rcParams["font.size"] = 14
plt.grid(axis="x")

plt.hist(data_low,range=[0,1.2],bins=100,color="blue")
plt.hist(data_mid,range=[0,1.2],bins=100,color="green")
plt.hist(data_high,range=[0,1.2],bins=100,color="red")

plt.savefig(dir_data+"../eps/fig_mask_histo.png",dpi=100)
