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
i = 0   # i != 2
snr = 3
resolutions = ["13.6","15.0","8.0","8.2"]
dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628", "ngc3627", "ngc4254", "ngc4321"]
beam = [[4.0,8.0,12.0,16.0,20.0],
        [8.0,12.0,16.0,20.0,24.0],
        [8.0,12.0,16.0,20.0,24.0],
        [4.0,8.0,12.0,16.0,20.0]]
scales = [44/1.0, 103/1.4, 52/1.3, 130/1.6]

Irms_co10_n0628 = [0.010,
                   0.025,
                   0.045,
                   0.055,
                   0.065]
Irms_co10_n3627 = [0.030,
                   0.045,
                   0.060,
                   0.090,
                   0.100]
Irms_co10_n4254 = [0.020,
                   0.035,
                   0.045,
                   0.055,
                   0.065]
Irms_co10_n4321 = [0.010,
                   0.020,
                   0.035,
                   0.040,
                   0.045]
Irms_co10 = [Irms_co10_n0628,Irms_co10_n3627,Irms_co10_n4254,Irms_co10_n4321]

Irms_co21_n0628 = [0.04,
                   0.08,
                   0.09,
                   0.10,
                   0.15]
Irms_co21_n3627 = [0.030,
                   0.035,
                   0.040,
                   0.045,
                   0.050]
Irms_co21_n4254 = [0.030,
                   0.035,
                   0.040,
                   0.045,
                   0.050]
Irms_co21_n4321 = [0.018,
                   0.030,
                   0.035,
                   0.037,
                   0.039]
Irms_co21 = [Irms_co21_n0628,Irms_co21_n3627,Irms_co21_n4254,Irms_co21_n4321]
velres = [2.0,2.5,2.5,2.5]

bins=80
xlim = [0.01,1.39]
ylim = [0.0,5.2]
step=(xlim[1]-xlim[0])/bins


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
    txtdata = dir_data+"f05_"+line+"_"+suffix+"."+txtname+".txt"
    process_fits(image,txtdata,mode,index=index)
    data = np.loadtxt(txtdata)

    return data

def violin_wt(ax,data,xval,bins,range,wt,step,color):
    """
    """
    # calculate weight
    if wt==None:
        weights=None
    else:
        weights=wt[data>0]

    # calculate histogram
    hist = np.histogram(data[data>0],bins,range=range,weights=weights,density=True)

    # import x and y data
    x=np.delete(hist[1],-1)
    y=hist[0]/(hist[0].max()*1.05)*2

    # plot violin
    ax.plot(y+xval,x,drawstyle="steps",color=color)
    ax.plot(y*-1+xval,x,drawstyle="steps",color=color)
    ax.barh(x,y,height=step,lw=0,color=color,alpha=0.4,left=xval)
    ax.barh(x,y*-1,height=step,lw=0,color=color,alpha=0.4,left=xval)

    # plot median
    num = hist_percent(y,0.5)
    #ax.plot([-2+xval,2+xval],[x[num],x[num]],"--",color=color,lw=2)
    value = x[num]
    num2 = hist_percent(y,0.843)
    value2 = x[num2]
    num3 = hist_percent(y,0.157)
    value3 = x[num3]

    return value, value2, value3

def check_nchan(dir_data,gal,suffix,line):
    """
    """
    imagename = dir_data+line+"_"+suffix+"_mask.image"
    outfile = imagename.replace("_mask.image",".nchan")
    os.system("rm -rf "+outfile)
    immoments(imagename=imagename,
              moments=[0],
              outfile=outfile)


#####################
### Main Procedure
#####################
fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(9, 4),sharey=True)
medians = []
yerr = []
yerr2 = []
for j in range(len(beam[i])):
    name_title = gals[i].replace("ngc","NGC ")
    beamfloat = float(beam[i][j])
    suffix = str(beam[i][j]).replace(".","p").zfill(4)
    d_fits_co10 = dir_data + gals[i] + "_co10/"
    d_fits_co21 = dir_data + gals[i] + "_co21/"
    Ico10_tmp_ = import_data(d_fits_co10,gals[i],"co10",suffix,"moment0","data","Ico10")
    Ico21_tmp_ = import_data(d_fits_co21,gals[i],"co21",suffix,"moment0","data","Ico21")
    co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
    co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2
    
    check_nchan(d_fits_co10,gals[i],suffix,"co10")
    nchan_tmp_ = import_data(d_fits_co10,gals[i],"co10",suffix,"nchan","data","nchan")

    # define cut
    Rco10 = Irms_co10[i][j]*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres[i]) # Jy/b.km/s
    Rco21 = Irms_co21[i][j]*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres[i]) # Jy/b.km/s
    cut_pos = (ra_tmp_ > 0) & (dec_tmp_ > 0)
    cut_co10 = (Ico10_tmp_ > Rco10)
    cut_co21 = (Ico21_tmp_ > Rco21)
    cut_all = np.where((cut_pos) & (cut_co10) & (cut_co21))

    # cut data
    Ico21_tmp2_ = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10_tmp2_ = Ico10_tmp_[cut_all] * co10_jy2k
    r21_tmp2_ = Ico21_tmp2_/Ico10_tmp2_
    r21_tmp2_[np.where(np.isnan(r21_tmp2_) & np.isinf(r21_tmp2_))] = 0

    Ico10 = Ico10_tmp2_[r21_tmp2_>0]
    Ico21 = Ico21_tmp2_[r21_tmp2_>0]
    r21 = r21_tmp2_[r21_tmp2_>0]

    num, num2, num3 = violin_wt(ax,r21,beamfloat,bins,xlim,None,step,
                          cm.brg(i/3.5))
    medians.append(num)
    yerr.append(num2)
    yerr2.append(num3)


plt.plot(beam[i],
         medians,"o-",
         color=cm.brg(i/3.5),
         markeredgewidth=0,
         markersize=10,
         lw=3)
plt.plot(beam[i],
         yerr,"--",
         color=cm.brg(i/3.5),
         markeredgewidth=0,
         markersize=10,
         lw=2)
plt.plot(beam[i],
         yerr2,"--",
         color=cm.brg(i/3.5),
         markeredgewidth=0,
         markersize=10,
         lw=2)
plt.xlim([beam[i][0]-2,beam[i][-1]+2])
if gals[i]=="ngc0628":
    plt.title("# of Sightlines") 
plt.ylabel("$R_{21}$")
plt.grid(axis="y")
plt.rcParams["font.size"] = 16
if gals[i]=="ngc4321":
    plt.xlabel("Beam Size (arcsec)")
plt.text((beam[i][0]-2)+((beam[i][-1]+2)-(beam[i][0]-2))*0.81,
         xlim[1]*0.9,
         name_title)
plt.plot([resolutions[i],resolutions[i]],[0.0,1.4],linestyle="-",lw=4,c="black",alpha=0.5)
plt.legend()
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_violin_num.png")

#
fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(9, 4),sharey=True)
medians = []
yerr = []
yerr2 = []
for j in range(len(beam[i])):
    name_title = gals[i].replace("ngc","NGC ")
    beamfloat = float(beam[i][j])
    suffix = str(beam[i][j]).replace(".","p")
    d_fits = dir_data+gals[i]+"_co/"
    
    Ico10_tmp_ = import_data(d_fits,gals[i],"co10",suffix,
                             "moment0","data","Ico10")
    Ico21_tmp_ = import_data(d_fits,gals[i],"co21",suffix,
                             "moment0","data","Ico21")
    co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
    co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2

    # define cut
    cut_co10 = (Ico10_tmp_ > Irms_co10[i][j]*snr)
    cut_co21 = (Ico21_tmp_ > Irms_co21[i][j]*snr)
    cut_all = np.where((cut_co10) & (cut_co21))

    # cut data
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
    r21 = Ico21/Ico10

    num, num2, num3 = violin_wt(ax,r21,beam[i][j],bins,xlim,Ico10,step,
                          cm.brg(i/3.5))
    medians.append(num)
    yerr.append(num2)
    yerr2.append(num3)


plt.plot(beam[i],
         medians,"o-",
         color=cm.brg(i/3.5),
         markeredgewidth=0,
         markersize=10,
         lw=3)
plt.plot(beam[i],
         yerr,"--",
         color=cm.brg(i/3.5),
         markeredgewidth=0,
         markersize=10,
         lw=2)
plt.plot(beam[i],
         yerr2,"--",
         color=cm.brg(i/3.5),
         markeredgewidth=0,
         markersize=10,
         lw=2)
plt.xlim([beam[i][0]-2,beam[i][-1]+2])
if gals[i]=="ngc0628":
    plt.title("CO(1-0) Flux")
plt.grid(axis="y")
plt.rcParams["font.size"] = 16
if gals[i]=="ngc4321":
    plt.xlabel("Beam Size (arcsec)")
    plt.tick_params(labelleft=False)
else:
    plt.tick_params(labelleft=False)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.plot([resolutions[i],resolutions[i]],[0.0,1.4],linestyle="-",lw=4,c="black",alpha=0.5)
plt.savefig(dir_data+"eps/"+gals[i]+"_violin_co10.png")

#
fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(9, 4),sharey=True)
medians = []
yerr = []
yerr2 = []
for j in range(len(beam[i])):
    name_title = gals[i].replace("ngc","NGC ")
    beamfloat = float(beam[i][j])
    suffix = str(beam[i][j]).replace(".","p")
    d_fits = dir_data+gals[i]+"_co/"
    
    Ico10_tmp_ = import_data(d_fits,gals[i],"co10",suffix,
                             "moment0","data","Ico10")
    Ico21_tmp_ = import_data(d_fits,gals[i],"co21",suffix,
                             "moment0","data","Ico21")
    co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
    co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2

    # define cut
    cut_co10 = (Ico10_tmp_ > Irms_co10[i][j]*snr)
    cut_co21 = (Ico21_tmp_ > Irms_co21[i][j]*snr)
    cut_all = np.where((cut_co10) & (cut_co21))

    # cut data
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
    r21 = Ico21/Ico10

    num, num2, num3 = violin_wt(ax,r21,beam[i][j],bins,xlim,Ico21,step,
                          cm.brg(i/3.5))
    medians.append(num)
    yerr.append(num2)
    yerr2.append(num3)

plt.plot(beam[i],
         medians,"o-",
         color=cm.brg(i/3.5),
         markeredgewidth=0,
         markersize=10,
         lw=3)
plt.plot(beam[i],
         yerr,"--",
         color=cm.brg(i/3.5),
         markeredgewidth=0,
         markersize=10,
         lw=2)
plt.plot(beam[i],
         yerr2,"--",
         color=cm.brg(i/3.5),
         markeredgewidth=0,
         markersize=10,
         lw=2)
plt.xlim([beam[i][0]-2,beam[i][-1]+2])
if gals[i]=="ngc0628":
    plt.title("CO(2-1) Flux")
plt.grid(axis="y")
plt.rcParams["font.size"] = 16
if gals[i]=="ngc4321":
    plt.xlabel("Beam Size (arcsec)")
    plt.tick_params(labelleft=False)
else:
    plt.tick_params(labelleft=False)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.plot([resolutions[i],resolutions[i]],[0.0,1.4],linestyle="-",lw=4,c="black",alpha=0.5)
plt.savefig(dir_data+"eps/"+gals[i]+"_violin_co21.png")

