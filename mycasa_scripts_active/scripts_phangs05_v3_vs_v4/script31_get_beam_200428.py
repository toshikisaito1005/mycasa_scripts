import os, sys, glob
import shutil


dir_data = "/Users/saito/data/phangs/compare_v3p4_v4/data/"
dir_product = "/Users/saito/data/phangs/compare_v3p4_v4/product/"


####################
### main
####################
# mkdir
done = glob.glob(dir_ready)
if not done:
	os.mkdir(dir_ready)


# get CASA files
v3_image = glob.glob(dir_data + "ngc4303_7m_co21_v3_nocommonbeam_dirty.psf")[0]
v4_image = glob.glob(dir_data + "ngc4303_7m_co21_v4_nocommonbeam_dirty.psf")[0]


# move to the ready directory
output = dir_ready + v3_image.split("/")[-1]
os.system("rm -rf " + output)
shutil.copytree(v3_image, output)

output = dir_ready + v4_image.split("/")[-1]
os.system("rm -rf " + output)
shutil.copytree(v3_image, output)
