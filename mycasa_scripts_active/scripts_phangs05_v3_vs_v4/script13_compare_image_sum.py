import os, sys, glob
import shutil
import matplotlib.pyplot as plt
plt.ioff()

dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data_ready_bias_cycf/"
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
v3_image = glob.glob(dir_ready + "ngc4303_7m_co21_v3.*.iamge.smooth")
v4_image = glob.glob(dir_ready + "ngc4303_7m_co21_v4*.image.smooth")
v3_image.sort()
v4_image.sort()


# get shape for imval
shape = imhead(v4_image[0],mode="list")["shape"]
box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)


# regrid v3 and move to the ready directory
plt.figure(figsize=(8,3))
plt.grid()
plt.subplots_adjust(left=0.15, right=0.95, top=0.90, bottom=0.15)
plt.rcParams["font.size"] = 14

for i in range(len(v4_image)):
#for i in [1]:
	# get names
	v4image = v4_image[i]
	v3image = v3_image[0]
	outputtag = v3image.split("ngc4303")[-1].split("v3.")[-1]
	output = dir_product + galname + "_diff_bias_cycf_" + outputtag + ".txt"
	title = "v4 sum - v3p4 sum (" + outputtag + ")"
	# imval
	done = glob.glob(output)
	if not done:
		print("### imval v3 " + outputtag)
		v3data = imval(v3image, box=box)
		print("### imval v4 " + outputtag)
		v4data = imval(v4image, box=box)
		#
		xaxis = range(np.shape(v3data['data']))[2]
		yaxis_v3 = v3data['data'].sum(axis=0).sum(axis=0)
		yaxis_v4 = v4data['data'].sum(axis=0).sum(axis=0)
		np.savetxt(output, np.c_[yaxis_v3, yaxis_v4], fmt="%.10f", header="v3sum v4sum")
	else:
		print("### skip imval " + outputtag)
		xaxis = range(len(np.loadtxt(output)[:,0]))
		yaxis_v3 = np.loadtxt(output)[:,0]
		yaxis_v4 = np.loadtxt(output)[:,1]
		#
	# plot
	xaxis = np.array(xaxis)
	yaxis = np.array(yaxis_v4 - yaxis_v3)
	#ypercent = np.array(yaxis_v4-yaxis_v3)/np.array(yaxis_v4)
	label = v4_image[i].split("/")[-1].replace("ngc4303_7m_co21_","").replace(".image","")
	label2 = label.replace("bias","smallscalebias = ").replace("_cycf",", cyclefactor = ")
	plt.scatter(xaxis, yaxis, lw=0, label=label2.replace("p","."))
	#
	plt.xlim(min(xaxis)-10,max(xaxis)+10)
	plt.xlabel("Channel")
	plt.ylabel("v4 sum - v3p4 sum")
	plt.title(title)
	#
plt.legend()
plt.savefig(output.replace(".txt",".png"), dpi=300)


os.system("rm -rf *.last")
