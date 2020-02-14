import re
import os, glob
import os.path
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
#matplotlib.use('Agg')

dir_data = "../../hcn_ulirgs/"
targets = glob.glob(dir_data + "hcn_*/*.region")

### create eps
def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

plt.figure()
plt.rcParams["font.size"] = 12
plt.subplots_adjust(wspace = 0.2, hspace = 0.2)

### ESO_148-IG002 N
# setup
txtdata_spw0 = targets[0].replace(".region", "_spw0.txt")
txtdata_spw1 = targets[0].replace(".region", "_spw1.txt")
txtdata_spw2 = targets[0].replace(".region", "_spw2.txt")
txtdata_spw3 = targets[0].replace(".region", "_spw3.txt")
data0 = np.loadtxt(txtdata_spw0, delimiter = " ")
data1 = np.loadtxt(txtdata_spw1, delimiter = " ")
data2 = np.loadtxt(txtdata_spw2, delimiter = " ")
data3 = np.loadtxt(txtdata_spw3, delimiter = " ")
xdata_spw0, ydata_spw0 = data0[:,0] * 0.000000001, data0[:,1]
xdata_spw1, ydata_spw1 = data1[:,0] * 0.000000001, data1[:,1]
xdata_spw2, ydata_spw2 = data2[:,0] * 0.000000001, data2[:,1]
xdata_spw3, ydata_spw3 = data3[:,0] * 0.000000001, data3[:,1]
ydataa = np.r_[ydata_spw0, ydata_spw1, ydata_spw2, ydata_spw3]
plt.subplot(421)
plt.xlim(min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64)[1]) * 1.1)
plt.ylim(0., max(plt.hist(ydataa, bins=64)[0]) * 1.25)
sum2 = plt.hist(ydataa, bins=64)
a = sum2[0].shape[0]
index = np.where(sum2[0] == max(sum2[0]))
edge = 300
dat = np.c_[list(sum2[1])[0:a], list(sum2[0])]
popt, pcov = curve_fit(gauss_function, dat[:,0], dat[:,1], p0 = [58, 75., 20.1], maxfev = 1000000)
plt.plot(dat[:,0], gauss_function(dat[:,0], *popt), color = "blue", lw=2)
plt.axvline(500., color='black', linestyle = "dashed", linewidth = 3)
plt.text((max(plt.hist(ydataa, bins=64)[1])-min(plt.hist(ydataa, bins=64)[1])) * 1.5 * 0.02 + min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64, histtype='stepfilled', color = "lightcoral")[0]) * 1.05, r"ESO 148-IG002 N ($\mu$ = " + str(round(popt[1], 2)) + ")")

### ESO_148-IG00 S
# setup
txtdata_spw0 = targets[1].replace(".region", "_spw0.txt")
txtdata_spw1 = targets[1].replace(".region", "_spw1.txt")
txtdata_spw2 = targets[1].replace(".region", "_spw2.txt")
txtdata_spw3 = targets[1].replace(".region", "_spw3.txt")
data0 = np.loadtxt(txtdata_spw0, delimiter = " ")
data1 = np.loadtxt(txtdata_spw1, delimiter = " ")
data2 = np.loadtxt(txtdata_spw2, delimiter = " ")
data3 = np.loadtxt(txtdata_spw3, delimiter = " ")
xdata_spw0, ydata_spw0 = data0[:,0] * 0.000000001, data0[:,1]
xdata_spw1, ydata_spw1 = data1[:,0] * 0.000000001, data1[:,1]
xdata_spw2, ydata_spw2 = data2[:,0] * 0.000000001, data2[:,1]
xdata_spw3, ydata_spw3 = data3[:,0] * 0.000000001, data3[:,1]
ydataa = np.r_[ydata_spw0, ydata_spw1, ydata_spw2, ydata_spw3]
plt.subplot(422)
plt.xlim(min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64)[1]) * 1.1)
plt.ylim(0., max(plt.hist(ydataa, bins=64)[0]) * 1.25)
sum2 = plt.hist(ydataa, bins=64)
a = sum2[0].shape[0]
index = np.where(sum2[0] == max(sum2[0]))
edge = 300
dat = np.c_[list(sum2[1])[0:a], list(sum2[0])]
popt, pcov = curve_fit(gauss_function, dat[:,0], dat[:,1], p0 = [58, 75., 20.1], maxfev = 1000000)
plt.plot(dat[:,0], gauss_function(dat[:,0], *popt), color = "blue", lw=2)
plt.axvline(500., color='black', linestyle = "dashed", linewidth = 3)
plt.text((max(plt.hist(ydataa, bins=64)[1])-min(plt.hist(ydataa, bins=64)[1])) * 1.5 * 0.02 + min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64, histtype='stepfilled', color = "lightcoral")[0]) * 1.05, r"ESO 148-IG002 S ($\mu$ = " + str(round(popt[1], 2)) + ")")


### ESO_286-IG019
# setup
txtdata_spw0 = targets[2].replace(".region", "_spw0.txt")
txtdata_spw1 = targets[2].replace(".region", "_spw1.txt")
txtdata_spw2 = targets[2].replace(".region", "_spw2.txt")
txtdata_spw3 = targets[2].replace(".region", "_spw3.txt")
data0 = np.loadtxt(txtdata_spw0, delimiter = " ")
data1 = np.loadtxt(txtdata_spw1, delimiter = " ")
data2 = np.loadtxt(txtdata_spw2, delimiter = " ")
data3 = np.loadtxt(txtdata_spw3, delimiter = " ")
xdata_spw0, ydata_spw0 = data0[:,0] * 0.000000001, data0[:,1]
xdata_spw1, ydata_spw1 = data1[:,0] * 0.000000001, data1[:,1]
xdata_spw2, ydata_spw2 = data2[:,0] * 0.000000001, data2[:,1]
xdata_spw3, ydata_spw3 = data3[:,0] * 0.000000001, data3[:,1]
ydataa = np.r_[ydata_spw0, ydata_spw1, ydata_spw2, ydata_spw3]
plt.subplot(423)
plt.xlim(min(plt.hist(ydataa, bins=256)[1]) * 1.5, max(plt.hist(ydataa, bins=256)[1]) * 0.3)
plt.ylim(0., max(plt.hist(ydataa, bins=256)[0]) * 1.25)
sum2 = plt.hist(ydataa, bins=256)
a = sum2[0].shape[0]
index = np.where(sum2[0] == max(sum2[0]))
edge = 300
dat = np.c_[list(sum2[1])[0:a], list(sum2[0])]
popt, pcov = curve_fit(gauss_function, dat[:,0], dat[:,1], p0 = [58, 75., 20.1], maxfev = 1000000)
plt.plot(dat[:,0], gauss_function(dat[:,0], *popt), color = "blue", lw=2)
plt.axvline(500., color='black', linestyle = "dashed", linewidth = 3)
plt.text((max(plt.hist(ydataa, bins=256)[1]) * 0.3 -min(plt.hist(ydataa, bins=256)[1]) * 1.5) * 0.02 + min(plt.hist(ydataa, bins=256)[1]) * 1.5, max(plt.hist(ydataa, bins=256, histtype='stepfilled', color = "lightcoral")[0]) * 1.05, r"ESO 286-IG019 ($\mu$ = " + str(round(popt[1], 2)) + ")")

### IRAS_F05189-2524
# setup
txtdata_spw0 = targets[3].replace(".region", "_spw0.txt")
txtdata_spw1 = targets[3].replace(".region", "_spw1.txt")
txtdata_spw2 = targets[3].replace(".region", "_spw2.txt")
txtdata_spw3 = targets[3].replace(".region", "_spw3.txt")
data0 = np.loadtxt(txtdata_spw0, delimiter = " ")
data1 = np.loadtxt(txtdata_spw1, delimiter = " ")
data2 = np.loadtxt(txtdata_spw2, delimiter = " ")
data3 = np.loadtxt(txtdata_spw3, delimiter = " ")
xdata_spw0, ydata_spw0 = data0[:,0] * 0.000000001, data0[:,1]
xdata_spw1, ydata_spw1 = data1[:,0] * 0.000000001, data1[:,1]
xdata_spw2, ydata_spw2 = data2[:,0] * 0.000000001, data2[:,1]
xdata_spw3, ydata_spw3 = data3[:,0] * 0.000000001, data3[:,1]
ydataa = np.r_[ydata_spw0, ydata_spw1, ydata_spw2, ydata_spw3]
plt.subplot(424)
plt.xlim(min(plt.hist(ydataa, bins=256)[1]) * 1.5, max(plt.hist(ydataa, bins=256)[1]) * 0.3)
plt.ylim(0., max(plt.hist(ydataa, bins=256)[0]) * 1.25)
sum2 = plt.hist(ydataa, bins=256)
a = sum2[0].shape[0]
index = np.where(sum2[0] == max(sum2[0]))
edge = 300
dat = np.c_[list(sum2[1])[0:a], list(sum2[0])]
popt, pcov = curve_fit(gauss_function, dat[:,0], dat[:,1], p0 = [58, 75., 20.1], maxfev = 1000000)
plt.plot(dat[:,0], gauss_function(dat[:,0], *popt), color = "blue", lw=2)
plt.axvline(500., color='black', linestyle = "dashed", linewidth = 3)
plt.text((max(plt.hist(ydataa, bins=256)[1]) * 0.3 -min(plt.hist(ydataa, bins=256)[1]) * 1.5) * 0.02 + min(plt.hist(ydataa, bins=256)[1]) * 1.5, max(plt.hist(ydataa, bins=256, histtype='stepfilled', color = "lightcoral")[0]) * 1.05, r"IRAS F05189-2524 ($\mu$ = " + str(round(popt[1], 2)) + ")")

### IRAS_13120-5453
# setup
txtdata_spw0 = targets[4].replace(".region", "_spw0.txt")
txtdata_spw1 = targets[4].replace(".region", "_spw1.txt")
txtdata_spw2 = targets[4].replace(".region", "_spw2.txt")
txtdata_spw3 = targets[4].replace(".region", "_spw3.txt")
data0 = np.loadtxt(txtdata_spw0, delimiter = " ")
data1 = np.loadtxt(txtdata_spw1, delimiter = " ")
data2 = np.loadtxt(txtdata_spw2, delimiter = " ")
data3 = np.loadtxt(txtdata_spw3, delimiter = " ")
xdata_spw0, ydata_spw0 = data0[:,0] * 0.000000001, data0[:,1]
xdata_spw1, ydata_spw1 = data1[:,0] * 0.000000001, data1[:,1]
xdata_spw2, ydata_spw2 = data2[:,0] * 0.000000001, data2[:,1]
xdata_spw3, ydata_spw3 = data3[:,0] * 0.000000001, data3[:,1]
ydataa = np.r_[ydata_spw0, ydata_spw1, ydata_spw2, ydata_spw3]
plt.subplot(425)
plt.xlim(min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64)[1]) * 1.1)
plt.ylim(0., max(plt.hist(ydataa, bins=64)[0]) * 1.25)
sum2 = plt.hist(ydataa, bins=64)
a = sum2[0].shape[0]
index = np.where(sum2[0] == max(sum2[0]))
edge = 300
dat = np.c_[list(sum2[1])[0:a], list(sum2[0])]
popt, pcov = curve_fit(gauss_function, dat[:,0], dat[:,1], p0 = [58, 75., 20.1], maxfev = 1000000)
plt.plot(dat[:,0], gauss_function(dat[:,0], *popt), color = "blue", lw=2)
plt.axvline(500., color='black', linestyle = "dashed", linewidth = 3)
plt.text((max(plt.hist(ydataa, bins=64)[1])-min(plt.hist(ydataa, bins=64)[1])) * 1.5 * 0.02 + min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64, histtype='stepfilled', color = "lightcoral")[0]) * 1.05, r"IRAS 13120-5453 ($\mu$ = " + str(round(popt[1], 2)) + ")")

### IRAS_F12112+0305 N
# setup
txtdata_spw0 = targets[5].replace(".region", "_spw0.txt")
txtdata_spw1 = targets[5].replace(".region", "_spw1.txt")
txtdata_spw2 = targets[5].replace(".region", "_spw2.txt")
txtdata_spw3 = targets[5].replace(".region", "_spw3.txt")
data0 = np.loadtxt(txtdata_spw0, delimiter = " ")
data1 = np.loadtxt(txtdata_spw1, delimiter = " ")
data2 = np.loadtxt(txtdata_spw2, delimiter = " ")
data3 = np.loadtxt(txtdata_spw3, delimiter = " ")
xdata_spw0, ydata_spw0 = data0[:,0] * 0.000000001, data0[:,1]
xdata_spw1, ydata_spw1 = data1[:,0] * 0.000000001, data1[:,1]
xdata_spw2, ydata_spw2 = data2[:,0] * 0.000000001, data2[:,1]
xdata_spw3, ydata_spw3 = data3[:,0] * 0.000000001, data3[:,1]
ydataa = np.r_[ydata_spw0, ydata_spw1, ydata_spw2, ydata_spw3]
plt.subplot(426)
plt.xlim(min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64)[1]) * 1.1)
plt.ylim(0., max(plt.hist(ydataa, bins=64)[0]) * 1.25)
sum2 = plt.hist(ydataa, bins=64)
a = sum2[0].shape[0]
index = np.where(sum2[0] == max(sum2[0]))
edge = 300
dat = np.c_[list(sum2[1])[0:a], list(sum2[0])]
popt, pcov = curve_fit(gauss_function, dat[:,0], dat[:,1], p0 = [58, 75., 20.1], maxfev = 1000000)
plt.plot(dat[:,0], gauss_function(dat[:,0], *popt), color = "blue", lw=2)
plt.axvline(500., color='black', linestyle = "dashed", linewidth = 3)
plt.text((max(plt.hist(ydataa, bins=64)[1])-min(plt.hist(ydataa, bins=64)[1])) * 1.5 * 0.02 + min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64, histtype='stepfilled', color = "lightcoral")[0]) * 1.05, r"IRAS F12112+0305 N ($\mu$ = " + str(round(popt[1], 2)) + ")")

### IRAS_F12112+0305 S
# setup
txtdata_spw0 = targets[6].replace(".region", "_spw0.txt")
txtdata_spw1 = targets[6].replace(".region", "_spw1.txt")
txtdata_spw2 = targets[6].replace(".region", "_spw2.txt")
txtdata_spw3 = targets[6].replace(".region", "_spw3.txt")
data0 = np.loadtxt(txtdata_spw0, delimiter = " ")
data1 = np.loadtxt(txtdata_spw1, delimiter = " ")
data2 = np.loadtxt(txtdata_spw2, delimiter = " ")
data3 = np.loadtxt(txtdata_spw3, delimiter = " ")
xdata_spw0, ydata_spw0 = data0[:,0] * 0.000000001, data0[:,1]
xdata_spw1, ydata_spw1 = data1[:,0] * 0.000000001, data1[:,1]
xdata_spw2, ydata_spw2 = data2[:,0] * 0.000000001, data2[:,1]
xdata_spw3, ydata_spw3 = data3[:,0] * 0.000000001, data3[:,1]
ydataa = np.r_[ydata_spw0, ydata_spw1, ydata_spw2, ydata_spw3]
plt.subplot(427)
plt.xlim(min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64)[1]) * 1.1)
plt.ylim(0., max(plt.hist(ydataa, bins=64)[0]) * 1.25)
sum2 = plt.hist(ydataa, bins=64)
a = sum2[0].shape[0]
index = np.where(sum2[0] == max(sum2[0]))
edge = 300
dat = np.c_[list(sum2[1])[0:a], list(sum2[0])]
popt, pcov = curve_fit(gauss_function, dat[:,0], dat[:,1], p0 = [58, 75., 20.1], maxfev = 1000000)
plt.plot(dat[:,0], gauss_function(dat[:,0], *popt), color = "blue", lw=2)
plt.axvline(500., color='black', linestyle = "dashed", linewidth = 3)
plt.text((max(plt.hist(ydataa, bins=64)[1])-min(plt.hist(ydataa, bins=64)[1])) * 1.5 * 0.02 + min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64, histtype='stepfilled', color = "lightcoral")[0]) * 1.05, r"IRAS F12112+0305 S ($\mu$ = " + str(round(popt[1], 2)) + ")")
plt.xlabel("Flux density (mJy)")
plt.ylabel("Count")

### IRAS_F17207-0014
# setup
txtdata_spw0 = targets[7].replace(".region", "_spw0.txt")
txtdata_spw1 = targets[7].replace(".region", "_spw1.txt")
txtdata_spw2 = targets[7].replace(".region", "_spw2.txt")
txtdata_spw3 = targets[7].replace(".region", "_spw3.txt")
data0 = np.loadtxt(txtdata_spw0, delimiter = " ")
data1 = np.loadtxt(txtdata_spw1, delimiter = " ")
data2 = np.loadtxt(txtdata_spw2, delimiter = " ")
data3 = np.loadtxt(txtdata_spw3, delimiter = " ")
xdata_spw0, ydata_spw0 = data0[:,0] * 0.000000001, data0[:,1]
xdata_spw1, ydata_spw1 = data1[:,0] * 0.000000001, data1[:,1]
xdata_spw2, ydata_spw2 = data2[:,0] * 0.000000001, data2[:,1]
xdata_spw3, ydata_spw3 = data3[:,0] * 0.000000001, data3[:,1]
ydataa = np.r_[ydata_spw0, ydata_spw1, ydata_spw2, ydata_spw3]
plt.subplot(428)
plt.xlim(min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64)[1]) * 1.1)
plt.ylim(0., max(plt.hist(ydataa, bins=64)[0]) * 1.25)
sum2 = plt.hist(ydataa, bins=64)
a = sum2[0].shape[0]
index = np.where(sum2[0] == max(sum2[0]))
edge = 300
dat = np.c_[list(sum2[1])[0:a], list(sum2[0])]
popt, pcov = curve_fit(gauss_function, dat[:,0], dat[:,1], p0 = [58, 75., 20.1], maxfev = 1000000)
plt.plot(dat[:,0], gauss_function(dat[:,0], *popt), color = "blue", lw=2)
plt.axvline(500., color='black', linestyle = "dashed", linewidth = 3)
plt.text((max(plt.hist(ydataa, bins=64)[1])-min(plt.hist(ydataa, bins=64)[1])) * 1.5 * 0.02 + min(plt.hist(ydataa, bins=64)[1]) * 1.5, max(plt.hist(ydataa, bins=64, histtype='stepfilled', color = "lightcoral")[0]) * 1.05, r"IRAS F17207-0014 ($\mu$ = " + str(round(popt[1], 2)) + ")")

plt.savefig(dir_data + "eps/hist.eps", bbox_inches='tight')

