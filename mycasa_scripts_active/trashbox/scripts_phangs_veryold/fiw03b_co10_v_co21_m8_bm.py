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


def load_data(txt_data):
    ap_size = int(txt_data.split("p0_")[1].split(".txt")[0])
    bm_size = int(txt_data.split("p")[-2].split("_")[-1])
    data = np.loadtxt(txt_data, usecols=(14,15,18,19))
    beta10 = 1.222 * 10**6 / bm_size**2 / 115.27120**2
    beta21 = 1.222 * 10**6 / bm_size**2 / 230.53800**2

    x = np.log10(data[:,2] * beta10) # co10_m0
    y = np.log10(data[:,3] * beta21) # co21_m0
    return x, y, ap_size, bm_size

#####################
### Main Procedure
#####################
### ngc4321
dir_data = "../../phangs/co_ratio/ngc4321/"
txtfiles = [dir_data + "ngc4321_flux_4p0_20.txt",
            dir_data + "ngc4321_flux_6p0_20.txt",
            dir_data + "ngc4321_flux_8p0_20.txt",
            dir_data + "ngc4321_flux_10p0_20.txt",
            dir_data + "ngc4321_flux_12p0_20.txt",
            dir_data + "ngc4321_flux_14p0_20.txt",
            dir_data + "ngc4321_flux_16p0_20.txt",
            dir_data + "ngc4321_flux_18p0_20.txt",
            dir_data + "ngc4321_flux_20p0_20.txt"]


### setup
bins = 20
limit = [-3.3,0.5]
limit2 = [-3.3,0.5]
limit3 = [-3.3,0.5]
figure = plt.figure(figsize=(16, 16))
plt.rcParams["font.size"] = 24
gs = gridspec.GridSpec(nrows=18, ncols=18)

# a00 scatter
a00 = plt.subplot(gs[0:9,0:9])
a00.set_xticks([])
a00b = a00.twiny()

a00.set_xlim(limit)
a00.set_ylim(limit)
a00b.set_xlim(limit)

a00b.set_xlabel("log $T_{CO(1-0),1/w}$ (K)")
a00.set_ylabel("log $T_{CO(2-1),1/w}$ (K)")


# x-axis histograms
ax1 = plt.subplot(gs[0:9,9])
ax2 = plt.subplot(gs[0:9,10])
ax3 = plt.subplot(gs[0:9,11])
ax4 = plt.subplot(gs[0:9,12])
ax5 = plt.subplot(gs[0:9,13])
ax6 = plt.subplot(gs[0:9,14])
ax7 = plt.subplot(gs[0:9,15])
ax8 = plt.subplot(gs[0:9,16])
ax9 = plt.subplot(gs[0:9,17])

ax1.set_xticks([])
ax2.set_xticks([])
ax3.set_xticks([])
ax4.set_xticks([])
ax5.set_xticks([])
ax6.set_xticks([])
ax7.set_xticks([])
ax8.set_xticks([])
ax9.set_xticks([])
ax1.set_yticks([])
ax2.set_yticks([])
ax3.set_yticks([])
ax4.set_yticks([])
ax5.set_yticks([])
ax6.set_yticks([])
ax7.set_yticks([])
ax8.set_yticks([])
ax9.set_yticks([])
ax9b = ax9.twinx()
ax9b.set_xticks([])

ax1.set_ylim(limit)
ax2.set_ylim(limit)
ax3.set_ylim(limit)
ax4.set_ylim(limit)
ax5.set_ylim(limit)
ax6.set_ylim(limit)
ax7.set_ylim(limit)
ax8.set_ylim(limit)
ax9b.set_ylim(limit)

ax9b.set_ylabel("log $T_{CO(2-1),1/w}$ (K)")

# y-axis histograms
ay1 = plt.subplot(gs[9,0:9])
ay2 = plt.subplot(gs[10,0:9])
ay3 = plt.subplot(gs[11,0:9])
ay4 = plt.subplot(gs[12,0:9])
ay5 = plt.subplot(gs[13,0:9])
ay6 = plt.subplot(gs[14,0:9])
ay7 = plt.subplot(gs[15,0:9])
ay8 = plt.subplot(gs[16,0:9])
ay9 = plt.subplot(gs[17,0:9])

ay1.set_xticks([])
ay2.set_xticks([])
ay3.set_xticks([])
ay4.set_xticks([])
ay5.set_xticks([])
ay6.set_xticks([])
ay7.set_xticks([])
ay8.set_xticks([])
#ay9.set_xticks([])
ay1.set_yticks([])
ay2.set_yticks([])
ay3.set_yticks([])
ay4.set_yticks([])
ay5.set_yticks([])
ay6.set_yticks([])
ay7.set_yticks([])
ay8.set_yticks([])
ay9.set_yticks([])

ay1.set_xlim(limit)
ay2.set_xlim(limit)
ay3.set_xlim(limit)
ay4.set_xlim(limit)
ay5.set_xlim(limit)
ay6.set_xlim(limit)
ay7.set_xlim(limit)
ay8.set_xlim(limit)
ay9.set_xlim(limit)

ay9.set_xlabel("log $T_{CO(1-0),1/w}$ (K)")


### a00
a00.plot([limit[0],limit[1]],
         [limit[0],limit[1]],
         "black",
         linewidth = 2)
a00.plot([limit[0],limit[1]],
         [limit[0]+log10(0.8),limit[1]+log10(0.8)],
         "black",
         linestyle="dashed",
         linewidth = 2)
a00.plot([limit[0],limit[1]],
         [limit[0]+log10(0.5),limit[1]+log10(0.5)],
         "black",
         linestyle="dashed",
         linewidth = 2)
a00.plot([limit[0],limit[1]],
         [limit[0]+log10(0.2),limit[1]+log10(0.2)],
         "black",
         linestyle="dashed",
         linewidth = 2)
for i in range(len(txtfiles)):
    x, y, ap_size, bm_size = load_data(txtfiles[i])

    a00.scatter(x, y, s=70, c=cm.gnuplot(i/8.), alpha=0.4,
                linewidth=0, label = str(bm_size)+"\"")

length = limit[1] - limit[0]
a00.text(limit[0] + length*0.05, limit[1] - length*0.15,
         "b) $T_{CO(1-0),1/w}$ vs $T_{CO(2-1),1/w}$ with \n    varying beam size")

a00.legend(bbox_to_anchor=(1.02, -0.2),
           loc="upper left", ncol=2,
           title="Beam Size (Fixed Aperture = 20\")")


### ax1
# histogram
x_ax1, y_ax1, ap_size, bm_size = load_data(txtfiles[0])
histo=ax1.hist(y_ax1,
               alpha=0.4,
               histtype="stepfilled",
               orientation="horizontal",
               color=cm.gnuplot(0/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ax1.set_xlim(0,max(histo[0][1:]))
ax1.spines["top"].set_visible(False)
ax1.spines["bottom"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
# mean and median
stats = []
for i in range(len(y_ax1)):
    if y_ax1[i] > -10000:
        stats.append(y_ax1[i])

mean = np.mean(stats)
medi = np.median(stats)
ax1.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
ax1.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)

### ax2
# histogram
x_ax2, y_ax2, ap_size, bm_size = load_data(txtfiles[1])
histo=ax2.hist(y_ax2,
               alpha=0.4,
               histtype="stepfilled",
               orientation="horizontal",
               color=cm.gnuplot(1/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ax2.set_xlim(0,max(histo[0][1:]))
ax2.spines["top"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
# mean and median
stats = []
for i in range(len(y_ax2)):
    if y_ax2[i] > -10000:
        stats.append(y_ax2[i])

mean = np.mean(stats)
medi = np.median(stats)
ax2.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
ax2.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)

### ax3
# histogram
x_ax3, y_ax3, ap_size, bm_size = load_data(txtfiles[2])
histo=ax3.hist(y_ax3,
               alpha=0.4,
               histtype="stepfilled",
               orientation="horizontal",
               color=cm.gnuplot(2/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ax3.spines["top"].set_visible(False)
ax3.spines["bottom"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["left"].set_visible(False)
# mean and median
stats = []
for i in range(len(y_ax3)):
    if y_ax3[i] > -10000:
        stats.append(y_ax3[i])

mean = np.mean(stats)
medi = np.median(stats)
ax3.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
ax3.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)

### ax4
# histogram
x_ax4, y_ax4, ap_size, bm_size = load_data(txtfiles[3])
histo=ax4.hist(y_ax4,
               alpha=0.4,
               histtype="stepfilled",
               orientation="horizontal",
               color=cm.gnuplot(3/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ax4.spines["top"].set_visible(False)
ax4.spines["bottom"].set_visible(False)
ax4.spines["right"].set_visible(False)
ax4.spines["left"].set_visible(False)
# mean and median
stats = []
for i in range(len(y_ax4)):
    if y_ax4[i] > -10000:
        stats.append(y_ax4[i])

mean = np.mean(stats)
medi = np.median(stats)
ax4.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
ax4.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)

### ax5
# histogram
x_ax5, y_ax5, ap_size, bm_size = load_data(txtfiles[4])
histo=ax5.hist(y_ax5,
               alpha=0.4,
               histtype="stepfilled",
               orientation="horizontal",
               color=cm.gnuplot(4/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ax5.spines["top"].set_visible(False)
ax5.spines["bottom"].set_visible(False)
ax5.spines["left"].set_visible(False)
ax5.spines["left"].set_visible(False)
ax5.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(y_ax5)):
    if y_ax5[i] > -10000:
        stats.append(y_ax5[i])

mean = np.mean(stats)
medi = np.median(stats)
ax5.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
ax5.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)

### ax6
# histogram
x_ax6, y_ax6, ap_size, bm_size = load_data(txtfiles[5])
histo=ax6.hist(y_ax6,
               alpha=0.4,
               histtype="stepfilled",
               orientation="horizontal",
               color=cm.gnuplot(5/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ax6.spines["top"].set_visible(False)
ax6.spines["bottom"].set_visible(False)
ax6.spines["left"].set_visible(False)
ax6.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(y_ax6)):
    if y_ax6[i] > -10000:
        stats.append(y_ax6[i])

mean = np.mean(stats)
medi = np.median(stats)
ax6.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
ax6.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)

### ax7
# histogram
x_ax7, y_ax7, ap_size, bm_size = load_data(txtfiles[6])
histo=ax7.hist(y_ax7,
               alpha=0.4,
               histtype="stepfilled",
               orientation="horizontal",
               color=cm.gnuplot(6/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ax7.spines["top"].set_visible(False)
ax7.spines["bottom"].set_visible(False)
ax7.spines["left"].set_visible(False)
ax7.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(y_ax7)):
    if y_ax7[i] > -10000:
        stats.append(y_ax7[i])

mean = np.mean(stats)
medi = np.median(stats)
ax7.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
ax7.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)

### ax8
# histogram
x_ax8, y_ax8, ap_size, bm_size = load_data(txtfiles[7])
histo=ax8.hist(y_ax8,
               alpha=0.4,
               histtype="stepfilled",
               orientation="horizontal",
               color=cm.gnuplot(7/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ax8.spines["top"].set_visible(False)
ax8.spines["bottom"].set_visible(False)
ax8.spines["left"].set_visible(False)
ax8.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(y_ax8)):
    if y_ax8[i] > -10000:
        stats.append(y_ax8[i])

mean = np.mean(stats)
medi = np.median(stats)
ax8.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
ax8.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)

### ax9b
# histogram
x_ax9, y_ax9, ap_size, bm_size = load_data(txtfiles[8])
histo=ax9b.hist(y_ax9,
                alpha=0.4,
                histtype="stepfilled",
                orientation="horizontal",
                color=cm.gnuplot(8/8.),
                bins=bins,
                linewidth=0,
                range=limit)
ax9.spines["top"].set_visible(False)
ax9.spines["bottom"].set_visible(False)
ax9.spines["left"].set_visible(False)
ax9b.spines["top"].set_visible(False)
ax9b.spines["bottom"].set_visible(False)
ax9b.spines["left"].set_visible(False)
# mean and median
stats = []
for i in range(len(y_ax9)):
    if y_ax9[i] > -10000:
        stats.append(y_ax9[i])

mean = np.mean(stats)
medi = np.median(stats)
ax9b.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
ax9b.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)


### ay1
# histogram
x, y, ap_size, bm_size = load_data(txtfiles[0])
histo=ay1.hist(x,
               alpha=0.4,
               histtype="stepfilled",
               color=cm.gnuplot(0/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ay1.set_ylim(0,max(histo[0][1:]))
ay1.invert_yaxis()
ay1.spines["top"].set_visible(False)
ay1.spines["bottom"].set_visible(False)
ay1.spines["left"].set_visible(False)
ay1.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(x)):
    if x[i] > -10000:
        stats.append(x[i])

mean = np.mean(stats)
medi = np.median(stats)
ay1.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
ay1.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)

### ay2
# histogram
x, y, ap_size, bm_size = load_data(txtfiles[1])
histo=ay2.hist(x,
               alpha=0.4,
               histtype="stepfilled",
               color=cm.gnuplot(1/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ay2.set_ylim(0,max(histo[0][1:]))
ay2.invert_yaxis()
ay2.spines["top"].set_visible(False)
ay2.spines["bottom"].set_visible(False)
ay2.spines["left"].set_visible(False)
ay2.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(x)):
    if x[i] > -10000:
        stats.append(x[i])

mean = np.mean(stats)
medi = np.median(stats)
ay2.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
ay2.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)

### ay3
# histogram
x, y, ap_size, bm_size = load_data(txtfiles[2])
histo=ay3.hist(x,
               alpha=0.4,
               histtype="stepfilled",
               color=cm.gnuplot(2/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ay3.set_ylim(0,max(histo[0][1:]))
ay3.invert_yaxis()
ay3.spines["top"].set_visible(False)
ay3.spines["bottom"].set_visible(False)
ay3.spines["left"].set_visible(False)
ay3.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(x)):
    if x[i] > -10000:
        stats.append(x[i])

mean = np.mean(stats)
medi = np.median(stats)
ay3.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
ay3.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)

### ay4
# histogram
x, y, ap_size, bm_size = load_data(txtfiles[3])
histo=ay4.hist(x,
               alpha=0.4,
               histtype="stepfilled",
               color=cm.gnuplot(3/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ay4.set_ylim(0,max(histo[0][1:]))
ay4.invert_yaxis()
ay4.spines["top"].set_visible(False)
ay4.spines["bottom"].set_visible(False)
ay4.spines["left"].set_visible(False)
ay4.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(x)):
    if x[i] > -10000:
        stats.append(x[i])

mean = np.mean(stats)
medi = np.median(stats)
ay4.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
ay4.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)

### ay5
# histogram
x, y, ap_size, bm_size = load_data(txtfiles[4])
histo=ay5.hist(x,
               alpha=0.4,
               histtype="stepfilled",
               color=cm.gnuplot(4/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ay5.set_ylim(0,max(histo[0][1:]))
ay5.invert_yaxis()
ay5.spines["top"].set_visible(False)
ay5.spines["bottom"].set_visible(False)
ay5.spines["left"].set_visible(False)
ay5.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(x)):
    if x[i] > -10000:
        stats.append(x[i])

mean = np.mean(stats)
medi = np.median(stats)
ay5.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
ay5.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)

### ax6
# histogram
x, y, ap_size, bm_size = load_data(txtfiles[5])
histo=ay6.hist(x,
               alpha=0.4,
               histtype="stepfilled",
               color=cm.gnuplot(5/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ay6.set_ylim(0,max(histo[0][1:]))
ay6.invert_yaxis()
ay6.spines["top"].set_visible(False)
ay6.spines["bottom"].set_visible(False)
ay6.spines["left"].set_visible(False)
ay6.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(x)):
    if x[i] > -10000:
        stats.append(x[i])

mean = np.mean(stats)
medi = np.median(stats)
ay6.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
ay6.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)

### ax7
# histogram
x, y, ap_size, bm_size = load_data(txtfiles[6])
histo=ay7.hist(x,
               alpha=0.4,
               histtype="stepfilled",
               color=cm.gnuplot(6/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ay7.set_ylim(0,max(histo[0][1:]))
ay7.invert_yaxis()
ay7.spines["top"].set_visible(False)
ay7.spines["bottom"].set_visible(False)
ay7.spines["left"].set_visible(False)
ay7.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(x)):
    if x[i] > -10000:
        stats.append(x[i])

mean = np.mean(stats)
medi = np.median(stats)
ay7.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
ay7.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)

### ax8
# histogram
x, y, ap_size, bm_size = load_data(txtfiles[7])
histo=ay8.hist(x,
               alpha=0.4,
               histtype="stepfilled",
               color=cm.gnuplot(7/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ay8.set_ylim(0,max(histo[0][1:]))
ay8.invert_yaxis()
ay8.spines["top"].set_visible(False)
ay8.spines["bottom"].set_visible(False)
ay8.spines["left"].set_visible(False)
ay8.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(x)):
    if x[i] > -10000:
        stats.append(x[i])

mean = np.mean(stats)
medi = np.median(stats)
ay8.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
ay8.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)

### ax9b
# histogram
x, y, ap_size, bm_size = load_data(txtfiles[8])
histo=ay9.hist(x,
               alpha=0.4,
               histtype="stepfilled",
               color=cm.gnuplot(8/8.),
               bins=bins,
               linewidth=0,
               range=limit)
ay9.set_ylim(0,max(histo[0][1:]))
ay9.invert_yaxis()
ay9.spines["top"].set_visible(False)
ay9.spines["left"].set_visible(False)
ay9.spines["right"].set_visible(False)
# mean and median
stats = []
for i in range(len(x)):
    if x[i] > -10000:
        stats.append(x[i])

mean = np.mean(stats)
medi = np.median(stats)
ay9.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
ay9.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)


plt.legend(loc="upper left", ncol=2)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/figiw03b_n4321_m8_bm.png",
            dpi=100)

