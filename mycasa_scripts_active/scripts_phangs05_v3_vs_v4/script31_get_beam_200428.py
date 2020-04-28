import os, sys
import matplotlib.pyplot as plt
plt.ioff()

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

# get bmaj
list_chan = []
list_bmaj = []
list_bmin = []
for i in range(len(data)-4):
	bmaj = data["*"+str(i)]["major"]["value"]
	bmin = data["*"+str(i)]["minor"]["value"]
	list_chan.append(i)
	list_bmaj.append(bmaj)
	list_bmin.append(bmin)

# plot
plt.figure(figsize=(8,3))
plt.grid()
plt.subplots_adjust(left=0.15, right=0.95, top=0.90, bottom=0.15)
plt.rcParams["font.size"] = 14
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:9,0:9])
ax2 = ax1.twinx()

ax1.scatter(list_chan, list_bmaj, lw=0, color="red", label="bmaj")
ax2.scatter(list_chan, list_bmin, lw=0, color="blue", label="bmin")


plt.xlabel("Channel")
plt.ylabel("bmaj (arcsec)")
plt.legend()
plt.savefig(dir_product + "ngc4304_bmaj_200428.png", dpi=300)
