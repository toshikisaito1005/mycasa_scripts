import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
from scipy.optimize import curve_fit
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
i = 1
snr = 2.5
dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628", "ngc3627", "ngc4254", "ngc4321"]
beam = [[4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0],
        [8.0,10.0,12.0,14.0,16.0,18.0,20.0,22.0,24.0],
        [8.0,10.0,12.0,14.0,16.0,18.0,20.0,22.0,24.0],
        [4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0]]

xlim = [-1.2,2.7] # [-1.9,1.9 or 2.9]
ylim = [-1.2,2.7] # [-1.9,1.9 or 2.9]
bins = 60
xlabel = "log $I_{CO(1-0)}$ (K km s$^{-1}$)"
ylabel = "log $I_{CO(2-1)}$ (K km s$^{-1}$)"
if i==0:
    text1 = "a) log $I_{CO(1-0)}$ vs log $I_{CO(2-1)}$"
elif i==1:
    text1 = "b) log $I_{CO(1-0)}$ vs log $I_{CO(2-1)}$"
elif i==2:
    text1 = "c) log $I_{CO(1-0)}$ vs log $I_{CO(2-1)}$"
elif i==3:
    text1 = "a) log $I_{CO(1-0)}$ vs log $I_{CO(2-1)}$"

velres = [6.0,10.0,10.0,5.0]
Irms_co10_n0628 = [0.010,0.020,0.030,0.040,0.050,0.060,0.070,0.080,0.090] # Jy/beam
Irms_co10_n3627 = [0.030,0.038,0.045,0.055,0.065,0.080,0.090,0.100,0.110] # Jy/beam
Irms_co10_n4254 = [0.025,0.030,0.036,0.040,0.045,0.050,0.050,0.055,0.060] # Jy/beam
Irms_co10_n4321 = [0.012,0.020,0.028,0.035,0.040,0.045,0.050,0.055,0.060] # Jy/beam
Irms_co10 = [Irms_co10_n0628,Irms_co10_n3627,Irms_co10_n4254,Irms_co10_n4321]
Irms_co10 = (np.array(Irms_co10)/1.2).tolist()

Irms_co21_n0628 = [0.025,0.030,0.035,0.037,0.038,0.039,0.040,0.042,0.043] # Jy/beam
Irms_co21_n3627 = [0.023,0.025,0.027,0.027,0.028,0.029,0.030,0.031,0.033] # Jy/beam
Irms_co21_n4254 = [0.028,0.030,0.032,0.033,0.033,0.035,0.037,0.038,0.040] # Jy/beam
Irms_co21_n4321 = [0.023,0.025,0.027,0.027,0.028,0.029,0.030,0.031,0.033] # Jy/beam
Irms_co21 = [Irms_co21_n0628,Irms_co21_n3627,Irms_co21_n4254,Irms_co21_n4321]
Irms_co21 = (np.array(Irms_co21)/1.2).tolist()

#####################
### functions
#####################
def hist_percent(histo,percent):
    dat_sum = np.sum(histo)
    dat_sum_from_zero,i = 0,0
    while dat_sum_from_zero < dat_sum * percent:
        dat_sum_from_zero += histo[i]
        i += 1
    
    return i

def process_fits(image,txtdata,mode,index=0):
    """
    """
    done = glob.glob(txtdata)
    if not done:
        ### import data
        image_r = imhead(image,mode="list")["shape"][0] - 1
        image_t = imhead(image,mode="list")["shape"][1] - 1
        
        value = imval(image,box="0,0,"+str(image_r)+","+str(image_t))
        
        if mode=="coords":
            value_masked = value[mode][:,:,index]
        else:
            value_masked = value[mode]
        
        value_masked_1d = value_masked.flatten()
        
        np.savetxt(txtdata, value_masked_1d)

def import_data(dir_data,
                gal,
                line,
                suffix,
                ext,
                mode,
                txtname,
                index=0):
    """
    """
    image = dir_data+line+"_"+suffix+"."+ext
    print(image)
    txtdata = dir_data+gal+"_"+suffix+"_f03_"+txtname+".txt"
    process_fits(image,txtdata,mode,index=index)
    data = np.loadtxt(txtdata)
    
    return data

def check_nchan(dir_data,gal,suffix,line):
    """
    """
    imagename = dir_data+line+"_"+suffix+"_mask.image"
    print(imagename)
    outfile = imagename.replace("_mask.image",".nchan")
    os.system("rm -rf "+outfile)
    immoments(imagename=imagename,
              moments=[0],
              outfile=outfile)

#####################
### Main Procedure
#####################
name_title = gals[i].replace("ngc","    for NGC ")

#
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 14
gs = gridspec.GridSpec(nrows=18, ncols=18)
ax1 = plt.subplot(gs[0:9,0:9])
ax2 = plt.subplot(gs[0:9,9:18])
ax3 = plt.subplot(gs[9:18,0:9])
ax1b = ax1.twiny()
ax2b = ax2.twinx()

ax1.tick_params(labelbottom=False)
ax1b.tick_params(labelbottom=False,labelleft=False)
ax2.tick_params(labelbottom=False,labelleft=False)
ax2b.tick_params(labelbottom=False)
ax3.tick_params(labelleft=False)

ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2b.spines["top"].set_visible(False)
ax2b.spines["left"].set_visible(False)
ax2b.spines["bottom"].set_visible(False)
ax3.spines["top"].set_visible(False)
ax3.spines["left"].set_visible(False)
ax3.spines["right"].set_visible(False)

ax2.tick_params(top=False,left=False,bottom=False)
ax2b.tick_params(top=False,left=False,bottom=False)
ax3.tick_params(top=False,left=False,right=False)

ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
ax1b.set_xlim(xlim)
ax2.set_ylim(ylim)
ax2b.set_ylim(ylim)
ax3.set_xlim(xlim)
ax3.set_ylim([9,0])

ax1.grid(axis="both")
ax2.grid(axis="y")
ax3.grid(axis="x")

ax1.set_ylabel(ylabel)
ax1b.set_xlabel(xlabel)
ax2b.set_ylabel(ylabel)
ax3.set_xlabel(xlabel)

meds_axis = []
meds_co10 = []
meds_co21 = []
meds_co10_err = []
meds_co21_err = []
for j in range(len(beam[i])):
    beamfloat = float(beam[i][j])
    suffix = str(beam[i][j]).zfill(4).replace(".","p")
    co10_fits = dir_data+gals[i]+"_co10/"
    co21_fits = dir_data+gals[i]+"_co21/"

    # import data
    Ico10_tmp_ = import_data(co10_fits,gals[i],"co10",suffix,
                             "moment0","data","Ico10")
    Ico21_tmp_ = import_data(co21_fits,gals[i],"co21",suffix,
                             "moment0","data","Ico21")
    co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
    co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2
    
    # count nchan
    check_nchan(co21_fits,gals[i],suffix,"co21")
    nchan_tmp_ = import_data(co21_fits,gals[i],"co21",suffix,
                             "nchan","data","nchan")

    # define cut
    Rco10 = Irms_co10[i][j]*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres[i]) # Jy/b.km/s
    Rco21 = Irms_co21[i][j]*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres[i]) # Jy/b.km/s
    cut_co10 = (Ico10_tmp_ > Rco10)
    cut_co21 = (Ico21_tmp_ > Rco21)
    cut_all = np.where((cut_co10) & (cut_co21))

    # cut data
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k # K
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k # K
    r21 = Ico21/Ico10
    
    meds_axis.append(j+0.5)
    meds_co10.append(np.median(np.log10(Ico10)))
    meds_co10_err.append(np.std(np.log10(Ico10))**2)
    meds_co21.append(np.median(np.log10(Ico21)))
    meds_co21_err.append(np.std(np.log10(Ico21))**2)

    # ax1
    ax1.scatter(np.log10(Ico10),
                np.log10(Ico21),
                color=cm.gnuplot(j/8.),
                alpha=0.1,
                s=20,
                lw=0)

    x1 = np.log10(np.median(Rco10[Rco10>0])*co10_jy2k)
    y1 = np.log10(np.median(Rco21[Rco21>0])*co21_jy2k)
    ax1.plot([x1,x1],ylim,"-",c=cm.gnuplot(j/8.),alpha=0.4)
    ax1.plot(xlim,[y1,y1],"-",c=cm.gnuplot(j/8.),alpha=0.4)
    
    if j==0:# or j==7:
        n, _ = np.histogram(np.log10(Ico10),bins=10,range=[0.0,2.5])
        sy, _ = np.histogram(np.log10(Ico10),bins=10,range=[0.0,2.5],
                             weights=np.log10(Ico21))
        sy2, _ = np.histogram(np.log10(Ico10),bins=10,range=[0.0,2.5],
                              weights=np.log10(Ico21)*np.log10(Ico21))
        mean = sy / n
        std = np.sqrt(sy2/n - mean*mean)
        ax1.errorbar((_[1:] + _[:-1])/2,mean,yerr=std,
                     color=cm.gnuplot(j/8.),
                     ecolor=cm.gnuplot(j/8.))

    # ax2
    hist_ax2 = np.histogram(np.log10(Ico21),
                           bins=bins,
                           range=ylim)

    x=np.delete(hist_ax2[1],-1)
    y=hist_ax2[0]/(hist_ax2[0].max()*1.05)

    ax2.plot(y+j,x,
             drawstyle="steps",
             color="grey",
             lw=0.5)
    ax2.barh(x,y,
             height=(ylim[1]-ylim[0])/bins,
             lw=0,
             color=cm.gnuplot(j/8.),
             alpha=0.4,
             left=j)

    # ax3
    hist_ax3 = np.histogram(np.log10(Ico10),
                            bins=bins,
                            range=ylim)

    y=np.delete(hist_ax3[1],-1)
    x=hist_ax3[0]/(hist_ax3[0].max()*1.05)

    ax3.plot(y,x+j,
             drawstyle="steps-mid",
             color="grey",#cm.gnuplot(j/8.),
             lw=0.5)
    ax3.bar(y,x,
            width=(ylim[1]-ylim[0])/bins,
            lw=0,
            color=cm.gnuplot(j/8.),
            alpha=0.4,
            bottom=j,
            align="center")


ax1.plot(xlim,ylim,"--",color="black",lw=3,alpha=0.7)
ax1.plot([np.log10(1/0.7*10**xlim[0]),xlim[1]],
         [ylim[0],np.log10(0.7*10**ylim[1])],"--",color="grey",lw=1,alpha=0.7)
ax1.plot([np.log10(1/0.4*10**xlim[0]),xlim[1]],
         [ylim[0],np.log10(0.4*10**ylim[1])],"--",color="grey",lw=1,alpha=0.7)

ax2.plot(meds_axis,
         meds_co21,
         "o-",
         color="grey",
         markeredgewidth=0,
         markersize=7,
         lw=2)

ax3.plot(meds_co10,
         meds_axis,
         "o-",
         color="grey",
         markeredgewidth=0,
         markersize=7,
         lw=2)

ax1.text(xlim[0]+(xlim[1]-xlim[0])*0.1,
         ylim[1]-(ylim[1]-ylim[0])*0.08,
         text1)
ax1.text(xlim[0]+(xlim[1]-xlim[0])*0.1,
         ylim[1]-(ylim[1]-ylim[0])*0.16,
         name_title)
plt.legend()
#plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_scatter_co10_co21.png",dpi=200)

os.system("rm -rf *.last")

