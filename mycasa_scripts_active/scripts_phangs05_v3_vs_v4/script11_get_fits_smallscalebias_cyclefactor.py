import os, sys, glob
import shutil


dir_data = "/Users/saito/data/phangs/compare_v3p4_v4/data/"
dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data_ready_bias_cycf/"
targetbeam = "9.0arcsec"


####################
### main
####################
# mkdir
done = glob.glob(dir_ready)
if not done:
	os.mkdir(dir_ready)


# get v4 CASA files
v3_image = glob.glob(dir_data + "ngc4303_7m_co21_v3.image")
v4_image = glob.glob(dir_data + "ngc4303_7m_co21_bias*.image")
v3_image.sort()
v4_image.sort()


# regrid v4 and move to the ready directory
print("### regrid v4 and mv")
for i in range(len(v4_image)):
	# get names
	imagename = v4_image[i]
	template = v3_image[i]
	output = dir_ready + v4_image[i].split("/")[-1]
	# imregrid
	os.system("rm -rf " + output)
	imregrid(imagename=imagename, template=template, output=output)

