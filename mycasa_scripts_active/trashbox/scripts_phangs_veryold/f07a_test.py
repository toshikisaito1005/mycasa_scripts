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
### Define Functions
#####################
def load_data(txt_data):
    ap_size = int(txt_data.split("p0_")[1].split(".txt")[0])
    bm_size = int(txt_data.split("p")[-2].split("_")[-1])
    data = np.loadtxt(txt_data, usecols=(2,3,6,7))
    beta10 = 1.222 * 10**6 / bm_size**2 / 115.27120**2
    beta21 = 1.222 * 10**6 / bm_size**2 / 230.53800**2
    
    x = np.log10(data[:,0] * beta10) # co10_m0
    y = np.log10(data[:,1] * beta21) # co21_m0
    return x, y, ap_size, bm_size

def w_median(data, weights):
    """
        Args:
        data (list or numpy.array): data
        weights (list or numpy.array): weights
        """
    data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
    s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
    midpoint = 0.5 * sum(s_weights)
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

def w_avg_and_std(values, weights):
    """
        Return the weighted average and standard deviation.
        
        values, weights -- Numpy ndarrays with the same shape.
        """
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)  # Fast and numerically precise
    return (average, math.sqrt(variance))

#####################
### Main Procedure
#####################
### ngc4321
dir_data = "../../phangs/co_ratio/ngc4321/"
txtfiles = glob.glob(dir_data+"ngc4321_flux_*.txt")
output = "w2uw_co21_r21.txt"

os.system("rm -rf " + dir_data + output)
f = open(dir_data + output, "a")
f.write("#r21 uw_10 w_10 w2_10 iw_10 iw2_10 uw_21 w_21 w2_21 iw_21 iw2_21\n")
### setup
for i in range(len(txtfiles)):
    co10_tmp, co21_tmp, ap_size, bm_size = load_data(txtfiles[i])
    
    co10, co21, r21 = [], [], []
    for j in range(len(co10_tmp)):
        if co10_tmp[j] > 0:
            if co21_tmp[j] > 0:
                co10.append(co10_tmp[j])
                co21.append(co21_tmp[j])
                r21.append(co21_tmp[j]/co10_tmp[j])


    data_10 = np.array(co10)
    data_21 = np.array(co21)
    data_r21 = np.array(r21)


    # stats r21
    median_r21_uw = str(round(np.median(data_r21), 3))
    std_r21_uw = str(round(np.std(data_r21), 3))


    # stats co10
    med10_uw = str(round(np.median(data_10), 3))
    std10_uw = str(round(np.std(data_10), 3))

    med10_w = str(round(w_median(data_10, data_10), 3))
    std10_w = str(round(w_avg_and_std(data_10, data_10)[1], 3))

    med10_w2 = str(round(w_median(data_10, data_10**2), 3))
    std10_w2 = str(round(w_avg_and_std(data_10, data_10**2)[1], 3))

    med10_iw = str(round(w_median(data_10, 1/data_10), 3))
    std10_iw = str(round(w_avg_and_std(data_10, 1/data_10)[1], 3))

    med10_iw2 = str(round(w_median(data_10, 1/data_10**2), 3))
    std10_iw2 = str(round(w_avg_and_std(data_10, 1/data_10**2)[1], 3))


    # stats co21
    med21_uw = str(round(np.median(data_21), 3))
    std21_uw = str(round(np.std(data_21), 3))

    med21_w = str(round(w_median(data_21, data_21), 3))
    std21_w = str(round(w_avg_and_std(data_21, data_21)[1], 3))

    med21_w2 = str(round(w_median(data_21, data_21**2), 3))
    std21_w2 = str(round(w_avg_and_std(data_21, data_21**2)[1], 3))

    med21_iw = str(round(w_median(data_21, 1/data_21), 3))
    std21_iw = str(round(w_avg_and_std(data_21, 1/data_21)[1], 3))

    med21_iw2 = str(round(w_median(data_21, 1/data_21**2), 3))
    std21_iw2 = str(round(w_avg_and_std(data_21, 1/data_21**2)[1], 3))

    f.write(median_r21_uw\
            +" "+med10_uw+" "+med10_w+" "+med10_w2+" "+med10_iw+" "+med10_iw2\
            +" "+med21_uw+" "+med21_w+" "+med21_w2+" "+med21_iw+" "+med21_iw2+"\n")

f.close()

