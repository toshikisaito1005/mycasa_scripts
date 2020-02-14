import glob
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import scipy.optimize
from scipy.optimize import curve_fit
plt.ioff()



#####################
### Main Procedure
#####################
### ngc0628
dir_data = "/Users/saito/data/phangs/co_ratio/data_txt/"
txtfiles = glob.glob(dir_data + "flux_ngc0628.txt")
data = np.loadtxt(txtfiles[0], usecols=(0,1,2))
beta10 = 1.222 * 10**6 / 115.27120**2
beta21 = 1.222 * 10**6 / 230.53800**2


fig=plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 18

ax1 = fig.add_subplot(111)
ln1 = ax1.plot(data[:,0], data[:,1] / data[:,0]**2 * beta10,
               c="blue", alpha=0.4, linewidth=5,
               label = "CO(1-0)")
ln2 = ax1.plot(data[:,0], data[:,2] / data[:,0]**2 * beta21,
               c="red", alpha=0.4, linewidth=5,
               label = "CO(2-1)")

ax2 = ax1.twinx()
ln3 = ax2.plot(data[:,0], data[:,2] / data[:,1] / 4.0,
               c="green", alpha=0.4, linewidth=5,
               label = "$R_{21}$")


h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1, loc="lower left")


ax1.set_xlabel("Beam Size (arcsec)")
ax1.set_ylabel("Total Flux (K km s$^{-1}$)")
ax2.set_ylabel("$R_{21}$")
ax1.set_ylim([0,5])
ax2.set_ylim([0,1])

plt.title("NGC 0628")
plt.legend(loc="lower right", ncol=2)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig97_n0628.png",
            dpi=300)



### ngc4321
dir_data = "/Users/saito/data/phangs/co_ratio/data_txt/"
txtfiles = glob.glob(dir_data + "flux_ngc4321.txt")
data = np.loadtxt(txtfiles[0], usecols=(0,1,2))
beta10 = 1.222 * 10**6 / 115.27120**2
beta21 = 1.222 * 10**6 / 230.53800**2


fig=plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 18

ax1 = fig.add_subplot(111)
ln1 = ax1.plot(data[:,0], data[:,1] / data[:,0]**2 * beta10,
               c="blue", alpha=0.4, linewidth=5,
               label = "CO(1-0)")
ln2 = ax1.plot(data[:,0], data[:,2] / data[:,0]**2 * beta21,
               c="red", alpha=0.4, linewidth=5,
               label = "CO(2-1)")

ax2 = ax1.twinx()
ln3 = ax2.plot(data[:,0], data[:,2] / data[:,1] / 4.0,
               c="green", alpha=0.4, linewidth=5,
               label = "$R_{21}$")


h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1, loc="lower left")


ax1.set_xlabel("Beam Size (arcsec)")
ax1.set_ylabel("Total Flux (K km s$^{-1}$)")
ax2.set_ylabel("$R_{21}$")
ax1.set_ylim([2,10.5])
ax2.set_ylim([0,1])

plt.title("NGC 4321")
plt.legend(loc="lower right", ncol=2)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig97_n4321.png",
            dpi=300)



### ngc3627
dir_data = "/Users/saito/data/phangs/co_ratio/data_txt/"
txtfiles = glob.glob(dir_data + "flux_ngc3627.txt")
data = np.loadtxt(txtfiles[0], usecols=(0,1,2))
beta10 = 1.222 * 10**6 / 115.27120**2
beta21 = 1.222 * 10**6 / 230.53800**2


fig=plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 18

ax1 = fig.add_subplot(111)
ln1 = ax1.plot(data[:,0], data[:,1] / data[:,0]**2 * beta10,
               c="blue", alpha=0.4, linewidth=5,
               label = "CO(1-0)")
ln2 = ax1.plot(data[:,0], data[:,2] / data[:,0]**2 * beta21,
               c="red", alpha=0.4, linewidth=5,
               label = "CO(2-1)")

ax2 = ax1.twinx()
ln3 = ax2.plot(data[:,0], data[:,2] / data[:,1] / 4.0,
               c="green", alpha=0.4, linewidth=5,
               label = "$R_{21}$")


h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1, loc="lower left")


ax1.set_xlabel("Beam Size (arcsec)")
ax1.set_ylabel("Total Flux (K km s$^{-1}$)")
ax2.set_ylabel("$R_{21}$")
ax1.set_ylim([6,16])
ax2.set_ylim([0,1])

plt.title("NGC 3627")
plt.legend(loc="lower right", ncol=2)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig97_n3627.png",
            dpi=300)



### ngc4254
dir_data = "/Users/saito/data/phangs/co_ratio/data_txt/"
txtfiles = glob.glob(dir_data + "flux_ngc4254.txt")
data = np.loadtxt(txtfiles[0], usecols=(0,1,2))
beta10 = 1.222 * 10**6 / 115.27120**2
beta21 = 1.222 * 10**6 / 230.53800**2


fig=plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 18

ax1 = fig.add_subplot(111)
ln1 = ax1.plot(data[:,0], data[:,1] / data[:,0]**2 * beta10,
               c="blue", alpha=0.4, linewidth=5,
               label = "CO(1-0)")
ln2 = ax1.plot(data[:,0], data[:,2] / data[:,0]**2 * beta21,
               c="red", alpha=0.4, linewidth=5,
               label = "CO(2-1)")

ax2 = ax1.twinx()
ln3 = ax2.plot(data[:,0], data[:,2] / data[:,1] / 4.0,
               c="green", alpha=0.4, linewidth=5,
               label = "$R_{21}$")


h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1, loc="lower left")


ax1.set_xlabel("Beam Size (arcsec)")
ax1.set_ylabel("Total Flux (K km s$^{-1}$)")
ax2.set_ylabel("$R_{21}$")
ax1.set_ylim([5,12.5])
ax2.set_ylim([0,1])

plt.title("NGC 4254")
plt.legend(loc="lower right", ncol=2)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig97_n4254.png",
            dpi=300)
