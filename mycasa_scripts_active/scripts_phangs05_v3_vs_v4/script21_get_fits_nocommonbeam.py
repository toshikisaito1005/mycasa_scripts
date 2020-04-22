import os, sys, glob
import shutil


dir_data = "/Users/saito/data/phangs/compare_v3p4_v4/data/"
dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data_ready_nocommonbeam/"
targetbeam = "9.0arcsec"


####################
### main
####################
# mkdir
done = glob.glob(dir_ready)
if not done:
	os.mkdir(dir_ready)


# get v4 CASA files
v3_image = glob.glob(dir_data + "ngc4303_7m_co21_v3_nocommonbeam_dirty.psf")[0]
v4_image = glob.glob(dir_data + "ngc4303_7m_co21_v4_nocommonbeam_dirty.psf")[0]


# move v3 to the ready directory
print("### mv v3")
for i in range(len(v3_image)):
	imagename = v3_image[0]
	output = dir_ready + imagename.split("/")[-1]
	os.system("rm -rf " + output)
	shutil.copytree(imagename, output)
