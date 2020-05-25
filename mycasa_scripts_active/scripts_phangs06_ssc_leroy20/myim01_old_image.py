import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()


#####
dir_data = "/Users/saito/data/myproj_active/proj_phangs06_ssc/data_old/"
gals = ["ngc0628"]
i=0

#####
def process_fits(image,txtdata,mode,index=0):
    done = glob.glob(txtdata)
    if not done:
        # import data
	image_r = imhead(image,mode="list")["shape"][0] - 1
	image_t = imhead(image,mode="list")["shape"][1] - 1

	value = imval(image,box="0,0,"+str(image_r)+","+str(image_t))

	if mode=="coords":
            value_masked = value[mode][:,:,index]
	else:
	    value_masked = value[mode]
	
	value_masked_1d = value_masked.flatten().tolist()

	np.savetxt(txtdata, value_masked_1d)

def import_data(imagename,
    mode,
    txtname,
    index=0):
    process_fits(imagename,txtname,mode,index=index)
    data = np.loadtxt(txtname)

    return data


#####
galname = gals[i]
#
imagenames = glob.glob(dir_data + galname + "/*.image")
#
txt_ra = imagenames[0] + "_ra.txt"
os.system("rm -rf " + txt_ra)
ra = import_data(imagename=imagenames[0], mode="coords", txtname=txt_ra)
ra = ra * 180 / np.pi
#
txt_dec = imagenames[0] + "_dec.txt"
os.system("rm -rf " + txt_dec)
dec = import_data(imagename=imagenames[0], mode="coords", txtname=txt_dec, index=1)
dec = dec * 180 / np.pi
#



for j in range(len(imagenames)):
    txtfile = imagenames[i] + ".txt"
    data = import_data(imagename=imagenames[j], mode="data", txtname=txtfile)
    #
    this_ra = ra[data>0.0001]
    this_dec = dec[data>0.0001]
    this_data = data[data>0.0001]
    #
    plt.figure(figsize=(8,8))
    plt.scatter(this_ra, this_dec, color=this_data, marker=".", cmap="rainbow", lw=1, s=5, alpha=0.5)
    plt.xlim([ra_tmp1_.max(),ra_tmp1_.min()])
    plt.ylim([dec_tmp1_.min(),dec_tmp1_.max()])
    plt.savefig(imagenames[j].split("/")[-1]+".png",dpi=100)


os.system("rm -rf *.last")
