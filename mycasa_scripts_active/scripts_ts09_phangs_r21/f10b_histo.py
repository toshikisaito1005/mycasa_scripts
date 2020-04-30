import os
import re
import sys
import glob
import scipy
import matplotlib.pyplot as plt
plt.ioff()

dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/ngc0628_r21/"
imagename = dir_data + "r21_04p0.moment0.highlowmask"


#
shape = imhead(imagename,mode="list")["shape"]
box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
data = imval(imagename,box=box)
data = data["data"] * data["mask"]
pixvalues = data.flatten()
