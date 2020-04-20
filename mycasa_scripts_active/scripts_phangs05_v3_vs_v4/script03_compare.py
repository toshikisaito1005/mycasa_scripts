import os, sys, glob
import shutil
import matplotlib.pyplot as plt
plt.ioff()

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
shape = imhead(v4_image[0],mode="list")["shape"]
box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)


# regrid v3 and move to the ready directory
for i in range(len(v4_image)):
	# get names
	v4image = v4_image[i]
	v3image = v3_image[i]
	outputtag = v3image.split("ngc4303")[-1].split("v3.")[-1]
	output = dir_product + galname + "_diff_" + outputtag + ".txt"
	title = "Difference " + outputtag
	# imval
	print("### imval v3 " + outputtag)
	v3data = imval(v3image, box=box)
	print("### imval v4 " + outputtag)
	v4data = imval(v4image, box=box)
	# plot
	plt.figure(figsize=(8,3))
	plt.grid()
	plt.subplots_adjust(left=0.15, right=0.95, top=0.90, bottom=0.15)
	plt.rcParams["font.size"] = 14
	xaxis = range( np.shape(v3data['data'])[2])
	yaxis_v3 = v3data['data'].sum(axis=0).sum(axis=0)
	yaxis_v4 = v4data['data'].sum(axis=0).sum(axis=0)
	plt.scatter(xaxis, yaxis_v4-yaxis_v3, lw=0)
	plt.xlabel("Channel")
	plt.ylabel("Diffference")
	plt.title(title)
	plt.savefig(dir_product+"test.png")

os.system("rm -rf *.last")

