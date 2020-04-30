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
#
line_high = np.percentile(data,50+33.3/2)
line_low = np.percentile(data,50-33.3/2)



###
plt.figure(figsize=(8,8))#figsize=(10,10))
plt.rcParams["font.size"] = 16
plt.grid(axis="x")

plt.hist(data_low,range=[0,1.5],bins=bins,color="blue",lw=0,alpha=0.5,label="Low")
plt.hist(data_mid,range=[0,1.5],bins=bins,color="green",lw=0,alpha=0.5,label="Mid ")
plt.hist(data_high,range=[0,1.5],bins=bins,color="red",lw=0,alpha=0.5,label="high")

plt.plot([line_high,line_high],[0,400],"--",lw=3,color="black")
plt.plot([line_low,line_low],[0,400],"--",lw=3,color="black")

plt.text(line_high+0.02,380,"66.7%")
plt.text(line_low-0.15,380,"33.3%")

plt.legend()
plt.savefig(dir_data+"../eps/fig_mask_histo.png",dpi=100)
