import os, sys, glob
import shutil
import matplotlib.pyplot as plt
plt.ioff()

dir_ready = "/Users/saito/data/phangs/compare_v3p4_v4/data_ready_200428/"
dir_product = "/Users/saito/data/phangs/compare_v3p4_v4/product/"
galname = "ngc4303"


####################
### main
####################
# mkdir
done = glob.glob(dir_product)
if not done:
	os.mkdir(dir_product)


# get CASA files
v3_image = glob.glob(dir_ready + "ngc4303_7m_co21_v3.image")[0]
v4_image = glob.glob(dir_ready + "ngc4303_7m_co21_v4.image")[0]


### v4 data
# get shape for imval
shape = imhead(v4_image,mode="list")["shape"]
box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
# imval
data = imval(v3_image, box=box)
data_v4 = range(np.shape(data['data'])[2])
#


# plot
plt.figure(figsize=(8,3))
plt.grid()
plt.subplots_adjust(left=0.15, right=0.95, top=0.90, bottom=0.15)
plt.rcParams["font.size"] = 14
xaxis = np.array(xaxis)
yaxis = np.array(yaxis_v4 - yaxis_v3)
#ypercent = np.array(yaxis_v4-yaxis_v3)/np.array(yaxis_v4)
plt.scatter(xaxis[abs(yaxis)!=0.0], yaxis[abs(yaxis)!=0.00], lw=0, color="red")
if np.sum([abs(yaxis)==0.00])>0:
	plt.scatter(xaxis[abs(yaxis)==0.00], yaxis[abs(yaxis)==0.00], lw=0, color="blue")
#
plt.xlim(min(xaxis)-10,max(xaxis)+10)
plt.xlabel("Channel")
plt.ylabel("v4 rms - v3p4 rms")
plt.title(title)
plt.savefig(output.replace(".txt",".png"), dpi=300)
#

os.system("rm -rf *.last")
