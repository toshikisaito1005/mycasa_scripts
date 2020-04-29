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

# smooth
imsmooth(imagename=v3_image,
	targetres=True,
	major="9.0arcsec",
	minor="9.0arcsec",
	outfile=v3_image+".smooth")

### v4 data
# get shape for imval
print("### get v4 data")
shape = imhead(v4_image,mode="list")["shape"]
box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
# imval
data = imval(v4_image, box=box)
# xaxis
xaxis_v4 = range(np.shape(data['data'])[2])
# yaxis
num_pixel_per_chan = np.shape(data['data'])[0]*np.shape(data['data'])[1]
yaxis_v4 = []
for i in range(len(xaxis_v4)):
	data_thischan = data['data'][:,:,i]
	data_clipped = data_thischan[data_thischan>0.00000001]
	if len(data_clipped)==0:
		rms = 0
		yaxis_v4.append(rms)
	else:
		rms = np.sqrt(np.mean(data_clipped**2))
		yaxis_v4.append(rms)


### v3 data
# get shape for imval
print("### get v3 data")
shape = imhead(v3_image,mode="list")["shape"]
box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
# imval
data = imval(v3_image, box=box)
# xaxis
xaxis_v3 = range(np.shape(data['data'])[2])
# yaxis
num_pixel_per_chan = np.shape(data['data'])[0]*np.shape(data['data'])[1]
yaxis_v3 = []
for i in range(len(xaxis_v3)):
	data_thischan = data['data'][:,:,i]
	data_clipped = data_thischan[data_thischan>0.00000001]
	if len(data_clipped)==0:
		rms = 0
		yaxis_v3.append(rms)
	else:
		rms = np.sqrt(np.mean(data_clipped**2))
		yaxis_v3.append(rms)


# plot
plt.figure(figsize=(8,3))
plt.grid()
plt.subplots_adjust(left=0.15, right=0.95, top=0.90, bottom=0.15)
plt.rcParams["font.size"] = 14
plt.scatter(xaxis_v3, yaxis_v3, lw=0, color="red", alpha=0.5, label="v3p4")
plt.scatter(xaxis_v4, yaxis_v4, lw=0, color="blue", alpha=0.5, label="v4")
plt.xlim(min(xaxis_v4)-10,max(xaxis_v4)+10)
plt.xlabel("Channel")
plt.ylabel("rms per pixel (Jy beam$^{-1}$)")
plt.legend()
plt.savefig(dir_product + "ngc4303_rms_200429.png", dpi=300)
#

os.system("rm -rf *.last")
