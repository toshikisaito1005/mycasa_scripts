import os
import glob
import numpy as np


dir_data = "../../myproj_published/proj_phangs03_outflow/data_raw/"
galaxy = ["ngc6300"]


#####################
### Main Procedure
#####################
# mkdir
dir_working = dir_data + "../data/"
os.system("rm -rf " + dir_working)
os.mkdir(dir_working)

# import galaxy information
galinfo = np.loadtxt("key_galaxy.txt",dtype="S100")

#
for i in range(len(galaxy)):
    # import galinfo
    galname = galaxy[i]
    chans = galinfo[np.where(galinfo[:,0]==galname)][0,1]
    
    # casa2fits
    fitsimage = glob.glob(dir_data + galname + "*12m+7m+tp*.fits")[0]
    imagename = dir_working + fitsimage.split("/")[-1].replace(".fits",".image_tmp")
    importfits(fitsimage = fitsimage, imagename = imagename)

    # cut datacube
    outfile = dir_working + fitsimage.split("/")[-1].replace(".fits",".image")
    imsubimage(imagename = imagename,
               chans = chans,
               outfile = outfile)
    os.system("rm -rf " + imagename)

os.system("rm -rf *.last")
