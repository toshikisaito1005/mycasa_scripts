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
plot_ymax = 0.4
plot_ytitle = 0.06
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
# USB
plt.subplot(421)
ydata = np.r_[ydata_spw2, ydata_spw3]
xdata = np.r_[xdata_spw2, xdata_spw3]
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.1, max(ydata) * plot_ymax)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([339.369267213, 339.369267213], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.plot([341.5028542, 341.5028542], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.text(min(xdata) * 1.0005, max(ydata) * plot_ymax - (max(ydata)-min(ydata)) * plot_ytitle, r"ESO 148-IG002 N")
plt.plot([339.553054228, 339.553054228], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="red")
plt.plot([340.384749775, 340.384749775], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="yellow")
plt.plot([340.869336713, 340.869336713], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="green")
plt.plot([341.044638096, 341.044638096], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="blue")


### ESO_148-IG00 S
# setup
plot_ymax = 0.3
plot_ytitle = 0.06
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
# USB
plt.subplot(422)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.1, max(ydata) * plot_ymax)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([min(xdata), max(xdata)], [0 , 0], '-', lw=1, color="black")
plt.plot([339.369267213, 339.369267213], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.plot([341.5028542, 341.5028542], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.text(min(xdata) * 1.0005, max(ydata) * plot_ymax - (max(ydata)-min(ydata)) * plot_ytitle, r"ESO 148-IG002 S")
plt.plot([339.553054228, 339.553054228], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="red")
plt.plot([340.384749775, 340.384749775], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="yellow")
plt.plot([340.869336713, 340.869336713], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="green")
plt.plot([341.044638096, 341.044638096], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="blue")

### ESO_286-IG019
# setup
plot_ymax = 0.2
plot_ytitle = 0.06
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
# USB
plt.subplot(423)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.1, max(ydata) * plot_ymax)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([339.891500926, 339.891500926], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.plot([342.028371154, 342.028371154], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.text(min(xdata) * 1.0005, max(ydata) * plot_ymax - (max(ydata)-min(ydata)) * plot_ytitle, r"ESO 286-IG019")
plt.plot([340.07557076, 340.07557076], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="red")
plt.plot([340.90854615, 340.90854615], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="yellow")
plt.plot([341.393878788, 341.393878788], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="green")
plt.plot([341.569449931, 341.569449931], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="blue")

### IRAS_F05189-2524
# setup
plot_ymax = 0.2
plot_ytitle = 0.06
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
# USB
plt.subplot(424)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.1, max(ydata) * plot_ymax)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([340.032665556, 340.032665556], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.plot([342.170423274, 342.170423274], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.text(min(xdata) * 1.0005, max(ydata) * plot_ymax - (max(ydata)-min(ydata)) * plot_ytitle, r"IRAS F05189-2524")
plt.plot([340.216811838, 340.216811838], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="red")
plt.plot([341.050133181, 341.050133181], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="yellow")
plt.plot([341.535667389, 341.535667389], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="green")
plt.plot([341.711311451, 341.711311451], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="blue")

### IRAS_13120-5453
# setup
plot_ymax = 0.6
plot_ytitle = 0.06
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
# LSB
plt.subplot(425)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.1, max(ydata) * plot_ymax)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([343.925969163, 343.925969163], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.plot([346.088203764, 346.088203764], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.text(min(xdata) * 1.0005, max(ydata) * plot_ymax - (max(ydata)-min(ydata)) * plot_ytitle, r"IRAS 13120-5453")
plt.plot([344.112223881, 344.112223881], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="red")
plt.plot([344.955086582, 344.955086582], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="yellow")
plt.plot([345.446180055, 345.446180055], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="green")
plt.plot([345.623835205, 345.623835205], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="blue")

### IRAS_F12112+0305 N
# setup
plot_ymax = 0.4
plot_ytitle = 0.06
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
# LSB
plt.subplot(426)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.1, max(ydata) * plot_ymax)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([330.289631022, 330.289631022], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.plot([332.366135075, 332.366135075], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.text(min(xdata) * 1.0005, max(ydata) * plot_ymax - (max(ydata)-min(ydata)) * plot_ytitle, r"IRAS F12112+0305 N")
plt.plot([330.468500918, 330.468500918], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="red")
plt.plot([331.277944913, 331.277944913], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="yellow")
plt.plot([331.749566997, 331.749566997], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="green")
plt.plot([331.920178288, 331.920178288], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="blue")

### IRAS_F12112+0305 S
# setup
plot_ymax = 0.6
plot_ytitle = 0.06
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
# LSB
plt.subplot(427)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.1, max(ydata) * plot_ymax)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([330.289631022, 330.289631022], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.plot([332.366135075, 332.366135075], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.text(min(xdata) * 1.0005, max(ydata) * plot_ymax - (max(ydata)-min(ydata)) * plot_ytitle, r"IRAS F12112+0305 S")
plt.plot([330.468500918, 330.468500918], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="red")
plt.plot([331.277944913, 331.277944913], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="yellow")
plt.plot([331.749566997, 331.749566997], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="green")
plt.plot([331.920178288, 331.920178288], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="blue")

### IRAS_F17207-0014
# setup
plot_ymax = 0.4
plot_ytitle = 0.06
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
plt.ylabel("Flux Density (mJy)")
plt.xlabel("Observed Frequency (GHz)")
# LSB
plt.subplot(428)
ydata = np.r_[ydata_spw3, ydata_spw2]
xdata = np.r_[xdata_spw3, xdata_spw2]
plt.plot([min(xdata) - 1., max(xdata) + 1.], [0, 0], 'k-', lw=1.0)
#plt.yticks(np.arange(0., 30., 10.))
#plt.grid(linestyle="--", lw=1.0)
plt.ylim(min(ydata) * 1.1, max(ydata) * plot_ymax)
plt.xlim(min(xdata), max(xdata))
plt.plot(xdata, ydata, lw=1.0, color="black")
plt.plot([339.952125411, 339.952125411], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.plot([342.08937678, 342.08937678], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="grey")
plt.text(min(xdata) * 1.0005, max(ydata) * plot_ymax - (max(ydata)-min(ydata)) * plot_ytitle, r"IRAS F17207-0014")
plt.plot([340.136228076, 340.136228076], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="red")
plt.plot([340.969352039, 340.969352039], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="yellow")
plt.plot([341.454771243, 341.454771243], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="green")
plt.plot([341.630373702, 341.630373702], [min(ydata) * 1.1, max(ydata) * plot_ymax], '--', lw=2, color="blue")




plt.savefig(dir_data + "eps/spec3.eps", bbox_inches='tight')

