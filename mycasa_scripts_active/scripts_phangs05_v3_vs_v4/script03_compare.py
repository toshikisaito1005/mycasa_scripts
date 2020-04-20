import os, sys, glob
import shutil


dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data_ready/"
dir_product = "/Users/saito/data/phangs/compare_v3p4_v4/product/"


####################
### main
####################
# mkdir
done = glob.glob(dir_ready)
if not done:
	os.mkdir(dir_ready)

# get v4 CASA files
v3_image = glob.glob(dir_ready + "ngc4303_7m_co21_v3.*")
v4_image = glob.glob(dir_ready + "ngc4303_7m_co21_v4.*")
v3_image.sort()
v4_image.sort()
# regrid v3 and move to the ready directory
for i in range(len(v4_image)):
	# get names
	v4image = v4_image[i]
	v3image = v3_image[i]
	# imregrid

os.system("rm -rf *.last")
