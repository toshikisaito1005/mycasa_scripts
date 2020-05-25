import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
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
dir_product = dir_data + "../eps/"
done = glob.glob(dir_product)
if not done:
    os.mkdir(dir_product)


galname = gals[i]
#
imagenames = glob.glob(dir_data + galname + "/*.smooth.pbcor")
template = glob.glob(dir_data + galname + "/*_skymodel.smooth")[0]
#
for i in range(len(imagenames)):
    os.system("rm -rf " + imagenames[i] + ".clip*")
    immath(imagename = [imagenames[i], template],
        expr = "iif(IM1>0.0394, IM0, 0.0)",
        outfile = imagenames[i] + ".clip")

    exportfits(imagename = imagenames[i] + ".clip",
        fitsimage = imagenames[i] + ".clip.fits")

os.system("rm -rf *.last")
