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
### ngc4321-only
dir_data = "../../phangs/co_ratio/ngc4321/"
txtfiles = glob.glob(dir_data + "ngc4321_flux_4p0_*.txt")

plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 14
plt.xscale("log")
plt.xlim([0.5,1000])
plt.ylim([0.1,0.87])
plt.xlabel("$^{12}$CO(2-1) flux")
plt.ylabel("$R_{21}$")

for i in range(len(txtfiles)):
    ap_size = int(txtfiles[i].split("4p0_")[1].split(".txt")[0])
    data = np.loadtxt(txtfiles[i], usecols=(2,3,6,7))

    y = data[:,3]/data[:,2]/4.
    for k in range(len(y)):
        if data[:,2][k] == 0:
            y[k] = 0

    plt.scatter(data[:,0], y,
                s=50, c=cm.hsv(i/10.), alpha=0.4, linewidth=0,
                label = str(ap_size)+"\"")

plt.legend(loc="lower right", ncol=2)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig05_n4321.png",
            dpi=300)

