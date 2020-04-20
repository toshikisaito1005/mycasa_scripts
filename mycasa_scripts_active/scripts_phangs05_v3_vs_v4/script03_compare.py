import os, sys, glob
import shutil


dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data_ready/"
dir_product = "/Users/saito/data/phangs/compare_v3p4_v4/product/"
galname = "ngc4303"


####################
### main
####################
# mkdir
done = glob.glob(dir_product)
if not done:
	os.mkdir(dir_product)

# get v4 CASA files
v3_image = glob.glob(dir_ready + "ngc4303_7m_co21_v3.*")
v4_image = glob.glob(dir_ready + "ngc4303_7m_co21_v4.*")
v3_image.sort()
v4_image.sort()

# get shape for imval
shape = imhead(v4image,mode="list")["shape"]
box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)

# regrid v3 and move to the ready directory
for i in range(len(v4_image)):
	# get names
	v4image = v4_image[i]
	v3image = v3_image[i]
	outputtag = v3image.split("ngc4303")[-1].split(".")[-1]
	output = dir_product + galname + "_" + outputtag + ".txt"
	# imval
	print("### imval v3 " + outputtag)
	v3data = imval(v3image, box=box)
	print("### imval v4 " + outputtag)
	v4data = imval(v4image, box=box)


os.system("rm -rf *.last")
