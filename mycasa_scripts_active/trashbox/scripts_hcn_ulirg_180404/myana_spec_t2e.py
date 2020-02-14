import re
import os, glob
import os.path
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
#matplotlib.use('Agg')

dir_data = "../../hcn_ulirgs/"
targets = glob.glob(dir_data + "hcn_*/*.region")

### create eps
def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

plt.figure()
plt.rcParams["font.size"] = 10
plt.subplots_adjust(wspace = 0.2, hspace = 0.2)

### ESO_148-IG00 N
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
# LSB
plt.subplot(421)
ydata = np.r_[ydata_spw0, ydata_spw1]
xdata = np.r_[xdata_spw0, xdata_spw1]
#plt.yticks(np.arange(0., 10., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.text(min(xdata) * 1.0005, max(ydata) * 1.4 - (max(ydata)-min(ydata)) * 0.2, r"ESO 148-IG002 N")
plt.plot([328.242888912, 328.242888912], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="green")
plt.plot([329.504107214, 329.504107214], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="orange")
plt.text(328.34, 0.14, r"CS(7-6)", color="green")
plt.text(328.5, 0.06, r"HC$^{15}$N(4-3)", color="orange")
# USB
plt.subplot(422)
ydata = np.r_[ydata_spw2, ydata_spw3]
xdata = np.r_[xdata_spw2, xdata_spw3]
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([339.369267213, 339.369267213], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="blue")
plt.plot([341.5028542, 341.5028542], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="red")
plt.text(339.47, 0.22, r"HCN(4-3)", color="blue")
plt.text(340.5, 0.32, r"HCO$^{+}$(4-3)", color="red")

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
# LSB
plt.subplot(423)
ydata = np.r_[ydata_spw0, ydata_spw1]
xdata = np.r_[xdata_spw0, xdata_spw1]
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.text(min(xdata) * 1.0005, max(ydata) * 1.4 - (max(ydata)-min(ydata)) * 0.2, r"ESO 148-IG002 S")
plt.plot([328.242888912, 328.242888912], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="green")
plt.plot([329.504107214, 329.504107214], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="orange")
# USB
plt.subplot(424)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([min(xdata), max(xdata)], [0, 0], '-', lw=1, color="black")
plt.plot([339.369267213, 339.369267213], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="blue")
plt.plot([341.5028542, 341.5028542], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="red")

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
# LSB
plt.subplot(425)
ydata = np.r_[ydata_spw1, ydata_spw0]
xdata = np.r_[xdata_spw1, xdata_spw0]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.text(min(xdata) * 1.0005, max(ydata) * 1.4 - (max(ydata)-min(ydata)) * 0.2, r"ESO 286-IG019")
plt.plot([328.748000951, 328.748000951], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="green")
plt.plot([330.011160062, 330.011160062], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="orange")
# USB
plt.subplot(426)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([339.891500926, 339.891500926], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="blue")
plt.plot([342.028371154, 342.028371154], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="red")

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
# LSB
plt.subplot(427)
ydata = np.r_[ydata_spw1, ydata_spw0]
xdata = np.r_[xdata_spw1, xdata_spw0]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.text(min(xdata) * 1.0005, max(ydata) * 1.4 - (max(ydata)-min(ydata)) * 0.2, r"IRAS F05189-2524")
plt.plot([328.884537433, 328.884537433], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="green")
plt.plot([330.148221163, 330.148221163], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="orange")
plt.ylabel("Flux Density (mJy)")
plt.xlabel("Observed Frequency (GHz)")
# USB
plt.subplot(428)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([340.032665556, 340.032665556], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="blue")
plt.plot([342.170423274, 342.170423274], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="red")

plt.savefig(dir_data + "eps/spec1.eps", bbox_inches='tight')


plt.figure()
plt.rcParams["font.size"] = 10
plt.subplots_adjust(wspace = 0.2, hspace = 0.2)

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
# USB
plt.subplot(421)
ydata = np.r_[ydata_spw1, ydata_spw0]
xdata = np.r_[xdata_spw1, xdata_spw0]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.text(min(xdata) * 1.0005, max(ydata) * 1.4 - (max(ydata)-min(ydata)) * 0.2, r"IRAS 13120-5453")
plt.plot([332.650197281, 332.650197281], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="green")
plt.plot([333.928349928, 333.928349928], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="orange")
# LSB
plt.subplot(422)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([343.925969163, 343.925969163], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="blue")
plt.plot([346.088203764, 346.088203764], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="red")

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
# USB
plt.subplot(423)
ydata = np.r_[ydata_spw1, ydata_spw0]
xdata = np.r_[xdata_spw1, xdata_spw0]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.text(min(xdata) * 1.0005, max(ydata) * 1.4 - (max(ydata)-min(ydata)) * 0.2, r"IRAS F12112+0305 N")
plt.plot([319.460932791, 319.460932791], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="green")
plt.plot([320.688407898, 320.688407898], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="orange")
# LSB
plt.subplot(424)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([330.289631022, 330.289631022], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="blue")
plt.plot([332.366135075, 332.366135075], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="red")

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
# USB
plt.subplot(425)
ydata = np.r_[ydata_spw1, ydata_spw0]
xdata = np.r_[xdata_spw1, xdata_spw0]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.text(min(xdata) * 1.0005, max(ydata) * 1.4 - (max(ydata)-min(ydata)) * 0.2, r"IRAS F12112+0305 S")
plt.plot([319.460932791, 319.460932791], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="green")
plt.plot([320.688407898, 320.688407898], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="orange")
# LSB
plt.subplot(426)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([330.289631022, 330.289631022], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="blue")
plt.plot([332.366135075, 332.366135075], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="red")

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
# USB
plt.subplot(427)
ydata = np.r_[ydata_spw1, ydata_spw0]
xdata = np.r_[xdata_spw1, xdata_spw0]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.text(min(xdata) * 1.0005, max(ydata) * 1.4 - (max(ydata)-min(ydata)) * 0.2, r"IRAS F17207-0014")
plt.plot([328.806637834, 328.806637834], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="green")
plt.plot([330.070022248, 330.070022248], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="orange")
plt.ylabel("Flux Density (mJy)")
plt.xlabel("Observed Frequency (GHz)")
# LSB
plt.subplot(428)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.2, max(ydata) * 1.4)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([339.952125411, 339.952125411], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="blue")
plt.plot([342.08937678, 342.08937678], [min(ydata) * 1.2, max(ydata) * 1.4], '--', lw=2, color="red")




plt.savefig(dir_data + "eps/spec2.eps", bbox_inches='tight')

