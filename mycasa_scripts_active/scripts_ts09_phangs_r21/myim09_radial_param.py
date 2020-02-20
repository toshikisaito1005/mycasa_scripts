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
snr = 5
dir_data = "/Users/saito/data/phangs/co_ratio/"
gals = ["ngc0628", "ngc3627", "ngc4254", "ngc4321"]
beam = [[13.6],[15.0],[8.0],[8.2]]

xlim = [-1.2,2.7] # [-1.9,1.9 or 2.9]
ylim = [-1.5,1.0] # [-1.9,1.9 or 2.9]
bins = 60
xlabel = "log $I_{CO(2-1)}$ (K km s$^{-1}$)"
ylabel = "log $R_{21}$"
if i==0:
    text1 = "a) log $I_{CO(2-1)}$ vs log $R_{21}$"
elif i==1:
    text1 = "b) log $I_{CO(2-1)}$ vs log $R_{21}$"
elif i==2:
    text1 = "c) log $I_{CO(2-1)}$ vs log $R_{21}$"
elif i==3:
    text1 = "b) log $I_{CO(2-1)}$ vs log $R_{21}$"

velres = [2.0,2.5,2.5,2.5]
Irms_co10 = [[0.050],[0.060],[0.020],[0.02]]
Irms_co21 = [[0.095],[0.040],[0.030],[0.03]]

scales = [44/1.0/1000, 52/1.3/1000, 130/1.6/1000, 103/1.4/1000]
cnt_ras = [24.174,
           170.063,
           184.707,
           185.729]
cnt_decs = [15.783,
            12.9914,
            14.4173,
            15.8223]
pas = [180-21.1,
       180-172.4,
       180-68.6,
       180-157.8]
incs = [90-8.7,
        90-56.2,
        90-35.2,
        90-35.1]


#####################
### functions
#####################
def distance(x, y, pa, inc, ra_cnt, dec_cnt, scale):
    tilt_cos = math.cos(math.radians(pa))
    tilt_sin = math.sin(math.radians(pa))
    
    x_tmp = x - ra_cnt
    y_tmp = y - dec_cnt
    
    x_new = (x_tmp*tilt_cos - y_tmp*tilt_sin)
    y_new = (x_tmp*tilt_sin + y_tmp*tilt_cos) * 1/math.sin(math.radians(inc))
    
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale
    
    return r

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
    image = dir_data+gal+"_"+line+"_"+suffix+"."+ext
    txtdata = dir_data+gal+"_"+suffix+"_f08_"+txtname+".txt"
    process_fits(image,txtdata,mode,index=index)
    data = np.loadtxt(txtdata)
    
    return data

def check_nchan(dir_data,gal,suffix):
    """
    """
    imagename = dir_data+gal+"_combine_"+suffix+".mask"
    outfile = imagename.replace(".mask",".nchan")
    os.system("rm -rf "+outfile)
    immoments(imagename=imagename,
              moments=[0],
              outfile=outfile)


#####################
### Main Procedure
#####################

#
#figure = plt.figure(figsize=(9,9))
#plt.rcParams["font.size"] = 14
#gs = gridspec.GridSpec(nrows=18, ncols=18)
for i in range(len(gals)):
    name_title = gals[i].replace("ngc","NGC ")
    for j in range(len(beam[i])):
        beamfloat = float(beam[i][j])
        suffix = str(beam[i][j]).replace(".","p")
        d_fits = dir_data+gals[i]+"_wise/"

        # import data
        Ico10_tmp_ = import_data(d_fits,gals[i],"co10",suffix,"moment0","data","Ico10")
        Ico21_tmp_ = import_data(d_fits,gals[i],"co21",suffix,"moment0","data","Ico21")
        ra_tmp_ = import_data(d_fits,gals[i],"co10",suffix,"moment0","coords","ra")
        dec_tmp_ = import_data(d_fits,gals[i],"co10",suffix,"moment0","coords","dec",1)
        co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
        co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2
        w1_tmp_ = import_data(d_fits,gals[i],"w1",suffix,"image","data","w1")
        w2_tmp_ = import_data(d_fits,gals[i],"w2",suffix,"image","data","w2")
        w3_tmp_ = import_data(d_fits,gals[i],"w3",suffix,"image","data","w3")
    
        # distance
        ra = ra_tmp_ * 180/np.pi # deg
        dec = dec_tmp_ * 180/np.pi # deg
        dist_tmp_ = distance(ra,dec,pas[i],incs[i],cnt_ras[i],cnt_decs[i],scales[i])

        # count nchan
        check_nchan(d_fits,gals[i],suffix)
        nchan_tmp_ = import_data(d_fits,gals[i],"combine",suffix,"nchan","data","nchan")

        # define cut
        Rco10 = Irms_co10[i][j]*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres[i]) # Jy/b
        Rco21 = Irms_co21[i][j]*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres[i]) # Jy/b
        cut_co10 = (Ico10_tmp_ > Rco10)
        cut_co21 = (Ico21_tmp_ > Rco21)
        cut_all = np.where((cut_co10) & (cut_co21))

        # cut data
        Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
        Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
        r21 = Ico21/Ico10
        dist = dist_tmp_[cut_all]

        # plot: co10
        figure = plt.figure(figsize=(9,12))
        plt.rcParams["font.size"] = 24
        gs = gridspec.GridSpec(nrows=20, ncols=20)
        plt.subplots_adjust(bottom=0.55, wspace=0.05)

        plt.scatter(dist,Ico10,lw=0,alpha=0.1,s=100,c="grey")

        n, _ = np.histogram(dist,bins=10)
        sy, _ = np.histogram(dist,bins=10,weights=Ico10)
        sy2, _ = np.histogram(dist,bins=10,weights=Ico10*Ico10)
        mean = sy / n
        std = np.sqrt(sy2/n - mean*mean)
        plt.errorbar((_[1:] + _[:-1])/2,mean,yerr=std,
                     color=cm.brg(i/3.5),ecolor=cm.brg(i/3.5),lw=7)

        plt.xlim([dist.max()*-0.1,dist.max()*1.1])
        xlength = dist.max()*1.1 + 0.5
        plt.ylim([Ico10.max()*-0.1,Ico10.max()*1.2])
        plt.grid()
        plt.ylabel("$I_{CO(1-0)}$")
        plt.text(dist.max()-xlength*0.3, Ico10.max()*1.02, name_title, fontsize=30)
        if gals[i]=="ngc0628":
            plt.text(0, Ico10.max()*1.02, "Radial $I_{CO(1-0)}$", fontsize=30)
        plt.savefig(dir_data+"eps/radial_co10_"+gals[i]+".png",dpi=200)
    
        # plot: co21
        figure = plt.figure(figsize=(9,12))
        plt.rcParams["font.size"] = 24
        gs = gridspec.GridSpec(nrows=20, ncols=20)
        plt.subplots_adjust(bottom=0.55, wspace=0.05)
    
        plt.scatter(dist,Ico21,lw=0,alpha=0.1,s=100,c="grey")

        n, _ = np.histogram(dist,bins=10)
        sy, _ = np.histogram(dist,bins=10,weights=Ico21)
        sy2, _ = np.histogram(dist,bins=10,weights=Ico21*Ico21)
        mean = sy / n
        std = np.sqrt(sy2/n - mean*mean)
        plt.errorbar((_[1:] + _[:-1])/2,mean,yerr=std,
                     color=cm.brg(i/3.5),ecolor=cm.brg(i/3.5),lw=7)
    
        plt.xlim([dist.max()*-0.1,dist.max()*1.1])
        xlength = dist.max()*1.1 + 0.5
        plt.ylim([Ico10.max()*-0.1,Ico10.max()*1.2])
        plt.grid()
        plt.ylabel("$I_{CO(2-1)}$")
        if gals[i]=="ngc0628":
            plt.text(0, Ico10.max()*1.02, "Radial $I_{CO(2-1)}$", fontsize=30)
        plt.savefig(dir_data+"eps/radial_co21_"+gals[i]+".png",dpi=200)
    
        # plot: r21
        figure = plt.figure(figsize=(9,12))
        plt.rcParams["font.size"] = 24
        gs = gridspec.GridSpec(nrows=20, ncols=20)
        plt.subplots_adjust(bottom=0.35, wspace=0.05)
    
        plt.scatter(dist,r21,lw=0,alpha=0.1,s=100,c="grey")

        n, _ = np.histogram(dist,bins=10)
        sy, _ = np.histogram(dist,bins=10,weights=r21)
        sy2, _ = np.histogram(dist,bins=10,weights=r21*r21)
        mean = sy / n
        std = np.sqrt(sy2/n - mean*mean)
        plt.errorbar((_[1:] + _[:-1])/2,mean,yerr=std,
                     color=cm.brg(i/3.5),ecolor=cm.brg(i/3.5),lw=7)
    
        print("### median of " + gals[i] + " = " + str(np.median(r21)))
    
        plt.xlim([-0.5,dist.max()*1.1])
        plt.ylim([0,2.0])
        plt.xlabel("Deprojected Distance (kpc)")
        if gals[i]=="ngc0628":
            plt.ylabel("$R_{21}$")
        plt.grid()
        if gals[i]=="ngc0628":
            plt.text(0, 1.7, "Radial $R_{21}$", fontsize=30)
        plt.savefig(dir_data+"eps/radial_r21_"+gals[i]+".png",dpi=200)

        combine_data = np.c_[(_[1:] + _[:-1])/2,mean,std]
        outputtxt = dir_data + gals[i] + "_wise/radial_r21.txt"
        np.savetxt(outputtxt,combine_data)

        outputtxt = dir_data + gals[i] + "_wise/radial_r21_rawdata.txt"
        np.savetxt(outputtxt,r21)
