import os, sys

dir_data = "/Users/saito/data/phangs/compare_v3p4_v4/data/"
dir_product = "/Users/saito/data/phangs/compare_v3p4_v4/product/"
imgaename = "ngc4303_7m_co21_dirty_200428.image"


####################
### main
####################
# mkdir
done = glob.glob(dir_product)
if not done:
	os.mkdir(dir_product)


# get CASA files
imgaename = dir_data + imgaename


# get beam
data = imhead(imgaename, mode="list")["perplanebeams"]

list_bmaj = []
for i in range(len(data)-3):
	bmaj = data["*"+str(i)]["major"]["value"]
	list_bmaj.append(bmaj)
