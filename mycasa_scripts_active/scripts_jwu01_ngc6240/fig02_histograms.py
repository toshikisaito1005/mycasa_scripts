import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
plt.ioff()


dir_product = "/Users/saito/data/myproj_active/proj_jwu01_ngc6240/eps/"


###
def weighted_percentile(data, weights, percent):
    """
    Args:
        data (list or numpy.array): data
        weights (list or numpy.array): weights
    """
    data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
    s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
    midpoint = percent * sum(s_weights)
    if any(weights > midpoint):
        w_median = (data[weights == np.max(weights)])[0]
    else:
        cs_weights = np.cumsum(s_weights)
        idx = np.where(cs_weights <= midpoint)[0][-1]
        if cs_weights[idx] == midpoint:
            w_median = np.mean(s_data[idx:idx+2])
        else:
            w_median = s_data[idx+1]

    return w_median


###
data = np.loadtxt("n6240_mom8_data.txt")
dist = data[:,0]
co10 = data[:,1]
co21 = data[:,2]


###
#
fig = plt.figure(figsize=(10,5))             #
ax1 = fig.add_subplot(111)                   #
ax1.grid(axis="x",linestyle='--')            #
plt.rcParams["font.size"] = 20               #
plt.subplots_adjust(bottom=0.15, left=0.12, right=0.95, top=0.9)  #


#
bins = 80                                    #
historange = [0.001,25.]                     #

hist_co10 = np.histogram(co10, bins = bins, range = historange, weights = co10) #
hist_co21 = np.histogram(co21, bins = bins, range = historange, weights = co21) #

#
ax1.step(np.delete(hist_co10[1],-1),
	      hist_co10[0]/float(sum(hist_co10[0])),
	      alpha=0.4,
	      lw = 2,
	      color = "blue",
	      label = "CO(1-0)")

#
ax1.step(np.delete(hist_co21[1],-1),
	      hist_co21[0]/float(sum(hist_co21[0])),
	      alpha=0.4,
	      lw = 2,
	      color = "red",
	      label = "CO(2-1)")

ax1.set_xlim(historange)                     #
ax1.set_ylim([0,0.25])                       #

ax1.set_ylabel("Normlized Count")            #
ax1.set_xlabel("Brightness Temperature (K)") #

plt.legend()                                 #
plt.savefig(dir_product + "figure_histo_mom8.png",dpi=300)


###
#
fig = plt.figure(figsize=(10,5))             #
ax1 = fig.add_subplot(111)                   #
ax1.grid(axis="x",linestyle='--')            #
plt.rcParams["font.size"] = 20               #
plt.subplots_adjust(bottom=0.15, left=0.12, right=0.95, top=0.9)  #


#
bins = 80
historange = [0.001,4.]

hist_r21 = np.histogram(co21/co10, bins = bins, range = historange) #
hist_r21_wco10 = np.histogram(co21/co10, bins = bins, range = historange, weights = co10) #
hist_r21_wco21 = np.histogram(co21/co10, bins = bins, range = historange, weights = co21) #

#
median_r21 = np.median(co21/co10)
median_r21_wco10 = weighted_percentile(co21/co10,co10,0.5)
median_r21_wco21 = weighted_percentile(co21/co10,co21,0.5)

#
p16_r21 = np.percentile(co21/co10,16)
p16_r21_wco10 = weighted_percentile(co21/co10,co10,0.16)
p16_r21_wco21 = weighted_percentile(co21/co10,co21,0.16)

#
p84_r21 = np.percentile(co21/co10,84)
p84_r21_wco10 = weighted_percentile(co21/co10,co10,0.84)
p84_r21_wco21 = weighted_percentile(co21/co10,co21,0.84)

#
ax1.plot([median_r21,median_r21],[0.14,0.14],"o",markersize=7,alpha=0.5,lw=0,color="blue")
ax1.plot([median_r21_wco10,median_r21_wco10],[0.13,0.13],"o",markersize=7,alpha=0.5,lw=0,color="green")
ax1.plot([median_r21_wco21,median_r21_wco21],[0.12,0.12],"o",markersize=7,alpha=0.5,lw=0,color="red")

#
ax1.plot([p16_r21,p84_r21],[0.14,0.14],"-",markersize=7,alpha=0.5,lw=2,color="blue")
ax1.plot([p16_r21_wco10,p84_r21_wco10],[0.13,0.13],"-",markersize=7,alpha=0.5,lw=2,color="green")
ax1.plot([p16_r21_wco21,p84_r21_wco21],[0.12,0.12],"-",markersize=7,alpha=0.5,lw=2,color="red")

#
ax1.step(np.delete(hist_r21[1],-1),
	      hist_r21[0]/float(sum(hist_r21[0])),
	      alpha=0.4,
	      lw = 2,
	      color = "blue",
	      label = "unweighted")

#
ax1.step(np.delete(hist_r21_wco10[1],-1),
	      hist_r21_wco10[0]/float(sum(hist_r21_wco10[0])),
	      alpha=0.4,
	      lw = 2,
	      color = "green",
	      label = "CO(1-0)-weighted")

#
ax1.step(np.delete(hist_r21_wco21[1],-1),
	      hist_r21_wco21[0]/float(sum(hist_r21_wco21[0])),
	      alpha=0.4,
	      lw = 2,
	      color = "red",
	      label = "CO(2-1)-weighted")

ax1.set_xlim(historange)
ax1.set_ylim([0,0.15])

ax1.set_ylabel("Normlized Count")
ax1.set_xlabel("Brightness Temperature Ratio")

plt.legend()
plt.savefig(dir_product + "figure_histo_ratio.png",dpi=300)
