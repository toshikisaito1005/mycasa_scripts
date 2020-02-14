import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()

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
	
	value_masked_1d = value_masked.flatten()

	np.savetxt(txtdata, value_masked_1d)

def import_data(imagename,
		mode,
		txtname,
		index=0):
    """
    """
    process_fits(imagename,txtname,mode,index=index)
    data = np.loadtxt(txtname)

    return data

#####
imagenames = glob.glob("../*_sim01/*.accuracy")
txt_ra = imagenames[0]+"_ra.txt"
os.system("rm -rf " + txt_ra)
ra_tmp_ = import_data(imagename = imagenames[0],
                      mode = "coords",
		      txtname = txt_ra)
ra_tmp1_ = ra_tmp_ * 180 / np.pi
txt_dec = imagenames[0]+"_dec.txt"
os.system("rm -rf " + txt_dec)
dec_tmp_ = import_data(imagename = imagenames[0],
                       mode = "coords",
 		       txtname = txt_dec,
		       index = 1)
dec_tmp1_ = dec_tmp_ * 180 / np.pi

for i in range(len(imagenames)):
    txt_caf = imagenames[i] + ".txt"
    data_tmp_ = import_data(imagename = imagenames[i],
                            mode = "data",
                            txtname = txt_caf)

    plt.figure(figsize=(8,8))
    plt.scatter(ra_tmp1_,dec_tmp1_,
                edgecolors="none",color=data_tmp_,marker=".",cmap="rainbow",lw=0,s=1,alpha=0.5)
    #plt.pcolor(ra_tmp1_,dec_tmp1_,data_tmp_,cmap="rainbow")
    plt.xlim([ra_tmp1_.max(),ra_tmp1_.min()])
    plt.ylim([dec_tmp1_.min(),dec_tmp1_.max()])
    plt.savefig(imagenames[i]+".png",dpi=100)


os.system("rm -rf *.last")
