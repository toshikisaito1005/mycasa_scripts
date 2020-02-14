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
### ngc4321
scale = 103/1.4/1000. #kpc/arcsec
# data stats
dir_data = "../../phangs/co_ratio/ngc4321_co/"
output = "bm_vs_ap_r21_median.txt"
txt_files = glob.glob(dir_data + "ngc4321*.txt")

os.system("rm -rf " + dir_data + output)
f = open(dir_data + output, "a")
f.write("#ap bm median_int median_peak std_int std_peak\n")
for i in range(len(txt_files)):
    size_ap = str(int(txt_files[i].split("_")[-1].split(".")[0]))
    size_bm = str(int(txt_files[i].split("_")[-2].split("p")[0]))
    data = np.loadtxt(txt_files[i], usecols=(2,3,6,7))
    r_int = data[:,1]/data[:,0]/4.
    r_pea = data[:,3]/data[:,2]/4.
    for j in range(len(r_int)):
        if data[:,0][j] == 0:
            r_int[j] = 0
    for k in range(len(r_pea)):
        if data[:,2][k] == 0:
            r_pea[k] = 0
    
    f.write(size_ap + " " + size_bm + " " \
            + str(np.median(r_int[r_int>0])) + " " \
            + str(np.median(r_pea[r_pea>0])) + " " \
            + str(np.std(r_int[r_int>0])) + " " \
            + str(np.std(r_pea[r_pea>0])) + " \n")

f.close()

txt_data = glob.glob(dir_data + output)
data = np.loadtxt(txt_data[0], usecols=(0,1,2,3,4,5))

# heat map: Rinteg
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 18

plt.scatter(data[:,0]*scale,
            data[:,1]*scale,
            s=750,
            linewidth=0,
            c=data[:,2],
            marker="s")

plt.xlim([1*scale,35*scale])
plt.ylim([1*scale,35*scale])
plt.clim([0.4,0.65])
plt.xlabel("Aperture Size (kpc)")
plt.ylabel("Beam Size (kpc)")
plt.text(1*scale + (35*scale-1*scale)*0.05,
         35*scale - (35*scale-1*scale)*0.08,
         "(a) median $R_{21}$, $Me$($R_{21}$)")
cbar=plt.colorbar()
cbar.set_label("$Me$($R_{21}$)", size=18)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/f05a_bm_vs_ap_R21_median_n4321.png",
            dpi=100)
