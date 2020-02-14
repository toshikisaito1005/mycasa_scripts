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
    ap_size = int(txt_data.split("4p0_")[1].split(".txt")[0])
    data = np.loadtxt(txt_data, usecols=(2,3,6,7))
    x = data[:,1]/data[:,0]/4.
    y = data[:,3]/data[:,2]/4.
    for j in range(len(x)):
        if data[:,0][j] == 0:
            x[j] = 0
    for k in range(len(y)):
        if data[:,2][k] == 0:
            y[k] = 0

    return x, y, ap_size

#####################
### Main Procedure
#####################
### ngc4321
dir_data = "../../phangs/co_ratio/ngc4321/"
txtfiles = [dir_data + "ngc4321_flux_4p0_04.txt",
            dir_data + "ngc4321_flux_4p0_06.txt",
            dir_data + "ngc4321_flux_4p0_08.txt",
            dir_data + "ngc4321_flux_4p0_10.txt",
            dir_data + "ngc4321_flux_4p0_12.txt",
            dir_data + "ngc4321_flux_4p0_14.txt",
            dir_data + "ngc4321_flux_4p0_16.txt",
            dir_data + "ngc4321_flux_4p0_18.txt",
            dir_data + "ngc4321_flux_4p0_20.txt"]


### setup
bins = 50
limit = [0.1,1.2] #[0.1,0.87]
limit2 = [0.5,1.8]
limit3 = [0.1,0.9]
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

a00b.set_xlabel("$^{12}$CO Integrated Intensity Ratio")
a00.set_ylabel("$^{12}$CO Peak Temperature Ratio")


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

ax9b.set_ylabel("$^{12}$CO Peak Temperature Ratio")

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

ay9.set_xlabel("$^{12}$CO Integrated Intensity Ratio")


### a00
a00.plot([0.05,1.25],[0.05,1.25],"black")
a00.plot([0.05,1.25],[0.15,1.35],"black",linestyle="dashed")
a00.plot([0.05,1.25],[-0.05,1.15],"black",linestyle="dashed")
for i in range(len(txtfiles)):
    x, y, ap_size = load_data(txtfiles[i])

    a00.scatter(x, y, s=100, c=cm.rainbow(i/8.), alpha=0.4,
                linewidth=0, label = str(ap_size)+"\"")

a00.legend(bbox_to_anchor=(1.02, -0.2),
           loc="upper left", ncol=2,
           title="Aperture Size (Fixed Beam = 4\")")


### ax1
x_ax1, y_ax1, ap_size = load_data(txtfiles[0])
histo=ax1.hist(y_ax1,alpha=0.4,histtype="stepfilled",
         orientation="horizontal",
         color=cm.rainbow(0/8.), bins=bins, linewidth=0, range=[0,2])
ax1.set_xlim(0,max(histo[0][1:]))
ax1.spines["top"].set_visible(False)
ax1.spines["bottom"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
### ax2
x_ax2, y_ax2, ap_size = load_data(txtfiles[1])
ax2.hist(y_ax2,alpha=0.4,histtype="stepfilled",
         orientation="horizontal",
         color=cm.rainbow(1/8.), bins=bins, linewidth=0, range=[0,2])
ax2.spines["top"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
### ax3
x_ax3, y_ax3, ap_size = load_data(txtfiles[2])
ax3.hist(y_ax3,alpha=0.4,histtype="stepfilled",
         orientation="horizontal",
         color=cm.rainbow(2/8.),bins=bins, linewidth=0, range=[0,2])
ax3.spines["top"].set_visible(False)
ax3.spines["bottom"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["left"].set_visible(False)
### ax4
x_ax4, y_ax4, ap_size = load_data(txtfiles[3])
ax4.hist(y_ax4,alpha=0.4,histtype="stepfilled",
         orientation="horizontal",
         color=cm.rainbow(3/8.), bins=bins, linewidth=0, range=[0,2])
ax4.spines["top"].set_visible(False)
ax4.spines["bottom"].set_visible(False)
ax4.spines["right"].set_visible(False)
ax4.spines["left"].set_visible(False)
### ax5
x_ax5, y_ax5, ap_size = load_data(txtfiles[4])
ax5.hist(y_ax5,alpha=0.4,histtype="stepfilled",
         orientation="horizontal",
         color=cm.rainbow(4/8.), bins=bins, linewidth=0, range=[0,2])
ax5.spines["top"].set_visible(False)
ax5.spines["bottom"].set_visible(False)
ax5.spines["left"].set_visible(False)
ax5.spines["left"].set_visible(False)
ax5.spines["right"].set_visible(False)
### ax6
x_ax6, y_ax6, ap_size = load_data(txtfiles[5])
ax6.hist(y_ax6,alpha=0.4,histtype="stepfilled",
         orientation="horizontal",
         color=cm.rainbow(5/8.), bins=bins, linewidth=0, range=[0,2])
ax6.spines["top"].set_visible(False)
ax6.spines["bottom"].set_visible(False)
ax6.spines["left"].set_visible(False)
ax6.spines["right"].set_visible(False)
### ax7
x_ax7, y_ax7, ap_size = load_data(txtfiles[6])
ax7.hist(y_ax7,alpha=0.4,histtype="stepfilled",
         orientation="horizontal",
         color=cm.rainbow(6/8.), bins=bins, linewidth=0, range=[0,2])
ax7.spines["top"].set_visible(False)
ax7.spines["bottom"].set_visible(False)
ax7.spines["left"].set_visible(False)
ax7.spines["right"].set_visible(False)
### ax8
x_ax8, y_ax8, ap_size = load_data(txtfiles[7])
ax8.hist(y_ax8,alpha=0.4,histtype="stepfilled",
         orientation="horizontal",
         color=cm.rainbow(7/8.), bins=bins, linewidth=0, range=[0,2])
ax8.spines["top"].set_visible(False)
ax8.spines["bottom"].set_visible(False)
ax8.spines["left"].set_visible(False)
ax8.spines["right"].set_visible(False)
### ax9b
x_ax9, y_ax9, ap_size = load_data(txtfiles[8])
ax9b.hist(y_ax9,alpha=0.4,histtype="stepfilled",
          orientation="horizontal",
          color=cm.rainbow(8/8.), bins=bins, linewidth=0, range=[0,2])
ax9.spines["top"].set_visible(False)
ax9.spines["bottom"].set_visible(False)
ax9.spines["left"].set_visible(False)
ax9b.spines["top"].set_visible(False)
ax9b.spines["bottom"].set_visible(False)
ax9b.spines["left"].set_visible(False)

### ay1
x, y, ap_size = load_data(txtfiles[0])
histo=ay1.hist(x,alpha=0.4,histtype="stepfilled",
               color=cm.rainbow(0/8.), bins=bins, linewidth=0, range=[0,2])
ay1.set_ylim(0,max(histo[0][1:]))
ay1.invert_yaxis()
ay1.spines["top"].set_visible(False)
ay1.spines["bottom"].set_visible(False)
ay1.spines["left"].set_visible(False)
ay1.spines["right"].set_visible(False)
### ay2
x, y, ap_size = load_data(txtfiles[1])
histo=ay2.hist(x,alpha=0.4,histtype="stepfilled",
               color=cm.rainbow(1/8.), bins=bins, linewidth=0, range=[0,2])
ay2.set_ylim(0,max(histo[0][1:]))
ay2.invert_yaxis()
ay2.spines["top"].set_visible(False)
ay2.spines["bottom"].set_visible(False)
ay2.spines["left"].set_visible(False)
ay2.spines["right"].set_visible(False)
### ay3
x, y, ap_size = load_data(txtfiles[2])
histo=ay3.hist(x,alpha=0.4,histtype="stepfilled",
               color=cm.rainbow(2/8.), bins=bins, linewidth=0, range=[0,2])
ay3.set_ylim(0,max(histo[0][1:]))
ay3.invert_yaxis()
ay3.spines["top"].set_visible(False)
ay3.spines["bottom"].set_visible(False)
ay3.spines["left"].set_visible(False)
ay3.spines["right"].set_visible(False)
### ay4
x, y, ap_size = load_data(txtfiles[3])
histo=ay4.hist(x,alpha=0.4,histtype="stepfilled",
               color=cm.rainbow(3/8.), bins=bins, linewidth=0, range=[0,2])
ay4.set_ylim(0,max(histo[0][1:]))
ay4.invert_yaxis()
ay4.spines["top"].set_visible(False)
ay4.spines["bottom"].set_visible(False)
ay4.spines["left"].set_visible(False)
ay4.spines["right"].set_visible(False)
### ay5
x, y, ap_size = load_data(txtfiles[4])
histo=ay5.hist(x,alpha=0.4,histtype="stepfilled",
               color=cm.rainbow(4/8.), bins=bins, linewidth=0, range=[0,2])
ay5.set_ylim(0,max(histo[0][1:]))
ay5.invert_yaxis()
ay5.spines["top"].set_visible(False)
ay5.spines["bottom"].set_visible(False)
ay5.spines["left"].set_visible(False)
ay5.spines["right"].set_visible(False)
### ax6
x, y, ap_size = load_data(txtfiles[5])
histo=ay6.hist(x,alpha=0.4,histtype="stepfilled",
               color=cm.rainbow(5/8.), bins=bins, linewidth=0, range=[0,2])
ay6.set_ylim(0,max(histo[0][1:]))
ay6.invert_yaxis()
ay6.spines["top"].set_visible(False)
ay6.spines["bottom"].set_visible(False)
ay6.spines["left"].set_visible(False)
ay6.spines["right"].set_visible(False)
### ax7
x, y, ap_size = load_data(txtfiles[6])
histo=ay7.hist(x,alpha=0.4,histtype="stepfilled",
               color=cm.rainbow(6/8.), bins=bins, linewidth=0, range=[0,2])
ay7.set_ylim(0,max(histo[0][1:]))
ay7.invert_yaxis()
ay7.spines["top"].set_visible(False)
ay7.spines["bottom"].set_visible(False)
ay7.spines["left"].set_visible(False)
ay7.spines["right"].set_visible(False)
### ax8
x, y, ap_size = load_data(txtfiles[7])
histo=ay8.hist(x,alpha=0.4,histtype="stepfilled",
               color=cm.rainbow(7/8.), bins=bins, linewidth=0, range=[0,2])
ay8.set_ylim(0,max(histo[0][1:]))
ay8.invert_yaxis()
ay8.spines["top"].set_visible(False)
ay8.spines["bottom"].set_visible(False)
ay8.spines["left"].set_visible(False)
ay8.spines["right"].set_visible(False)
### ax9b
x, y, ap_size = load_data(txtfiles[8])
histo=ay9.hist(x,alpha=0.4,histtype="stepfilled",
               color=cm.rainbow(8/8.), bins=bins, linewidth=0, range=[0,2])
ay9.set_ylim(0,max(histo[0][1:]))
ay9.invert_yaxis()
ay9.spines["top"].set_visible(False)
ay9.spines["left"].set_visible(False)
ay9.spines["right"].set_visible(False)


plt.legend(loc="upper left", ncol=2)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/fig02_n4321.png",
            dpi=100)

