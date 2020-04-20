import os, sys, glob
import shutil


dir_data = "/Users/saito/data/phangs/compare_v3p4_v4/data/"
dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data_ready/"
# v3 channel width = 2.54 km/s
# v4 channel width = 2.22 km/s
# v3 velocity width = 1914.68 ~ 1218.07 km/s (0~279)
# v3 velocity width = 1911.32 ~ 1217.90 km/s (0`312)
# v3 imsize = [255, 255,   0, 274]
# v4 imsize = [255, 255,   0, 312]


####################
### main
####################
# mkdir
done = glob.glob(dir_ready)
if not done:
	os.mkdir(dir_ready)

# get v4 CASA files
v3_image = glob.glob(dir_data + "ngc4303_7m_co21_v3.*")
v4_image = glob.glob(dir_data + "ngc4303_7m_co21_v4.*")
v3_image.sort()
v4_image.sort()
# regrid v3 and move to the ready directory
for i in range(len(v4_image)):
	# get names
	imagename = v4_image[i]
	template = v3_image[i]
	output = dir_ready + v4_image[i].split("/")[-1]
	# imregrid
	os.system("rm -rf " + output)
	imregrid(imagename=imagename, template=template, output=output)

# move v3 to the ready directory
for i in range(len(v3_image)):
	imagename = v3_image[i]
	output = dir_ready + imagename.split("/")[-1]
	os.system("rm -rf " + output)
	shutil.copytree(imagename, output)

os.system("rm -rf " + dir_ready + "ngc4303_7m_co21_v3.psf")
os.system("rm -rf *.last")
