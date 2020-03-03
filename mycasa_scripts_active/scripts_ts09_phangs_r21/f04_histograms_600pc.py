import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
from scipy.optimize import curve_fit
from scipy.stats import gaussian_kde
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
dir_data = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]
percents = [0.15,0.025,0.010]


#####################
### functions
#####################
def weighted_median(data, weights):
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


#####################
### Main Procedure
#####################
for i in range(len(gals)):
	galname = gals[i]
	data = np.loadtxt(dir_data + galname + "_parameter_matched_res.txt")



#for i in range(len(gals)):
for i in [0,1,2]:
    name_title = gals[i].replace("ngc","NGC ")
    beamfloat = float(beam[i].replace("p","."))
    d_fits_co10 = dir_data + gals[i] + "_co10/"
    d_fits_co21 = dir_data + gals[i] + "_co21/"

    # import data
    ra_tmp_ = import_data(d_fits_co10,gals[i],"co10",beam[i],"moment0","coords","ra")
    dec_tmp_ = import_data(d_fits_co10,gals[i],"co10",beam[i],"moment0","coords","dec",1)
    Ico10_tmp_ = import_data(d_fits_co10,gals[i],"co10",beam[i],"moment0","data","Ico10")
    Ico21_tmp_ = import_data(d_fits_co21,gals[i],"co21",beam[i],"moment0","data","Ico21")

    co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
    co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2

    check_nchan(d_fits_co10,gals[i],beam[i],"co10")
    nchan_tmp_ = import_data(d_fits_co10,gals[i],"co10",beam[i],"nchan","data","nchan")

    # define cut
    Rco10 = Irms_co10[i]*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres[i]) # Jy/b.km/s
    Rco21 = Irms_co21[i]*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres[i]) # Jy/b.km/s
    cut_pos = (ra_tmp_ > 0) & (dec_tmp_ > 0)
    cut_co10 = (Ico10_tmp_ > Rco10)
    cut_co21 = (Ico21_tmp_ > Rco21)
    cut_all = np.where((cut_pos) & (cut_co10) & (cut_co21))

    # cut data
    ra = ra_tmp_[cut_all] * 180/pi # deg
    dec = dec_tmp_[cut_all] * 180/pi # deg
    Ico21_tmp2_ = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10_tmp2_ = Ico10_tmp_[cut_all] * co10_jy2k
    r21_tmp2_ = Ico21_tmp2_/Ico10_tmp2_
    r21_tmp2_[np.where(np.isnan(r21_tmp2_) & np.isinf(r21_tmp2_))] = 0

    dist_tmp_ = distance(ra,dec,pas[i],incs[i],cnt_ras[i],cnt_decs[i],scales[i])
    dist = dist_tmp_[r21_tmp2_>0]
    Ico10 = Ico10_tmp2_[r21_tmp2_>0]
    Ico21 = Ico21_tmp2_[r21_tmp2_>0]
    r21 = r21_tmp2_[r21_tmp2_>0]
    num = float(len(r21))

    ### plot data
    plt.figure(figsize=(18,3))
    plt.rcParams["font.size"] = 14
    gs = gridspec.GridSpec(nrows=9, ncols=16)
    plt1 = plt.subplot(gs[1:7,0:4])
    plt2 = plt.subplot(gs[1:7,4:8])
    plt3 = plt.subplot(gs[1:7,8:12])
    #plt4 = plt.subplot(gs[1:7,12:16])
    plt1.grid(axis="x")
    plt2.grid(axis="x")
    plt3.grid(axis="x")
    #plt4.grid(axis="x")

    ## hist 1
    histo1 = np.histogram(r21,bins=bins,range=(xlim),weights=None)
    histo1x,histo1y = np.delete(histo1[1],-1),histo1[0]
    histo2 = np.histogram(r21[dist<def_nucleus[i]],bins=bins,range=(xlim),weights=None)
    histo2x,histo2y = np.delete(histo2[1],-1),histo2[0]
    histo3 = np.histogram(r21[dist>def_nucleus[i]],bins=bins,range=(xlim),weights=None)
    histo3x,histo3y = np.delete(histo3[1],-1),histo3[0]

    # kernel density estimation
    y11 = histo1y/float(sum(histo1y))
    y12 = histo2y/float(sum(histo1y))
    y13 = histo3y/float(sum(histo1y))
    med1 = np.median(r21)
    med2 = np.median(r21[dist<def_nucleus[i]])
    med3 = np.median(r21[dist>def_nucleus[i]])
    print(gals[i]+", median = "+str(med1))

    # plt1
    plt1.plot(histo1x,y11,"black",lw=5,alpha=0.5)
    plt1.plot(histo1x,y12,c=cm.brg(i/2.5),ls="dotted",lw=2,alpha=1.0)
    plt1.plot(histo1x,y13,c=cm.brg(i/2.5),ls="-",lw=5,alpha=0.5)
    plt1.plot(med1, 0.15, ".", markersize=14,c="black")
    plt1.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/2.5))
    plt1.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/2.5))
    plt1.plot([histo1x[hist_percent(histo1y,0.157)],
               histo1x[hist_percent(histo1y,0.843)]],
              [0.15,0.15],c="black",lw=3,alpha=0.5)
    plt1.plot([histo2x[hist_percent(histo2y,0.157)],
               histo2x[hist_percent(histo2y,0.843)]],
              [0.14,0.14],c=cm.brg(i/2.5),lw=3,alpha=1.0,linestyle="dotted")
    plt1.plot([histo3x[hist_percent(histo3y,0.157)],
               histo3x[hist_percent(histo3y,0.843)]],
              [0.13,0.13],c=cm.brg(i/2.5),lw=3,alpha=0.5)
    
    #plt1.set_yscale("log")
    plt1.set_xlim(xlim)
    plt1.set_ylim(ylim)

    ## hist 2
    histo1 = np.histogram(r21,bins=bins,range=(xlim),weights=Ico10)
    histo1x,histo1y = np.delete(histo1[1],-1),histo1[0]
    histo2 = np.histogram(r21[dist<def_nucleus[i]],bins=bins,range=(xlim),
                          weights=Ico10[dist<def_nucleus[i]])
    histo2x,histo2y = np.delete(histo2[1],-1),histo2[0]
    histo3 = np.histogram(r21[dist>def_nucleus[i]],bins=bins,range=(xlim),
                          weights=Ico10[dist>def_nucleus[i]])
    histo3x,histo3y = np.delete(histo3[1],-1),histo3[0]
    
    # kernel density estimation
    y11 = histo1y/float(sum(histo1y))
    y12 = histo2y/float(sum(histo1y))
    y13 = histo3y/float(sum(histo1y))
    med1 = weighted_median(r21,Ico10)
    med2 = weighted_median(r21[dist<def_nucleus[i]],Ico10[dist<def_nucleus[i]])
    med3 = weighted_median(r21[dist>def_nucleus[i]],Ico10[dist>def_nucleus[i]])
    
    # plt2
    plt2.plot(histo1x,y11,"black",lw=5,alpha=0.5)
    plt2.plot(histo1x,y12,c=cm.brg(i/2.5),ls="dotted",lw=2,alpha=1.0)
    plt2.plot(histo1x,y13,c=cm.brg(i/2.5),ls="-",lw=5,alpha=0.5)
    plt2.plot(med1, 0.15, ".", markersize=14,c="black")
    plt2.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/2.5))
    plt2.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/2.5))
    plt2.plot([histo1x[hist_percent(histo1y,0.157)],
               histo1x[hist_percent(histo1y,0.843)]],
              [0.15,0.15],c="black",lw=3,alpha=0.5)
    plt2.plot([histo2x[hist_percent(histo2y,0.157)],
               histo2x[hist_percent(histo2y,0.843)]],
              [0.14,0.14],c=cm.brg(i/2.5),lw=3,alpha=1.0,linestyle="dotted")
    plt2.plot([histo3x[hist_percent(histo3y,0.157)],
               histo3x[hist_percent(histo3y,0.843)]],
              [0.13,0.13],c=cm.brg(i/2.5),lw=3,alpha=0.5)
    
    #plt2.set_yscale("log")
    plt2.set_xlim(xlim)
    plt2.set_ylim(ylim)
    
    ## hist 3
    histo1 = np.histogram(r21,bins=bins,range=(xlim),weights=Ico21)
    histo1x,histo1y = np.delete(histo1[1],-1),histo1[0]
    histo2 = np.histogram(r21[dist<def_nucleus[i]],bins=bins,range=(xlim),
                          weights=Ico21[dist<def_nucleus[i]])
    histo2x,histo2y = np.delete(histo2[1],-1),histo2[0]
    histo3 = np.histogram(r21[dist>def_nucleus[i]],bins=bins,range=(xlim),
                          weights=Ico21[dist>def_nucleus[i]])
    histo3x,histo3y = np.delete(histo3[1],-1),histo3[0]

    # kernel density estimation
    y11 = histo1y/float(sum(histo1y))
    y12 = histo2y/float(sum(histo1y))
    y13 = histo3y/float(sum(histo1y))
    med1 = weighted_median(r21,Ico21)
    med2 = weighted_median(r21[dist<def_nucleus[i]],Ico21[dist<def_nucleus[i]])
    med3 = weighted_median(r21[dist>def_nucleus[i]],Ico21[dist>def_nucleus[i]])

    # plt3
    plt3.plot(histo1x,y11,"black",lw=5,alpha=0.5)
    plt3.plot(histo1x,y12,c=cm.brg(i/2.5),ls="dotted",lw=2,alpha=1.0)
    plt3.plot(histo1x,y13,c=cm.brg(i/2.5),ls="-",lw=5,alpha=0.5)
    plt3.plot(med1, 0.15, ".", markersize=14,c="black")
    plt3.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/2.5))
    plt3.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/2.5))
    plt3.plot([histo1x[hist_percent(histo1y,0.157)],
               histo1x[hist_percent(histo1y,0.843)]],
              [0.15,0.15],c="black",lw=3,alpha=0.5)
    plt3.plot([histo2x[hist_percent(histo2y,0.157)],
               histo2x[hist_percent(histo2y,0.843)]],
              [0.14,0.14],c=cm.brg(i/2.5),lw=3,alpha=1.0,linestyle="dotted")
    plt3.plot([histo3x[hist_percent(histo3y,0.157)],
               histo3x[hist_percent(histo3y,0.843)]],
              [0.13,0.13],c=cm.brg(i/2.5),lw=3,alpha=0.5)

    #plt3.set_yscale("log")
    plt3.set_xlim(xlim)
    plt3.set_ylim(ylim)
    
    ## hist 4
    """
    histo1 = np.histogram(r21,bins=bins,range=(xlim),weights=w3)
    histo1x,histo1y = np.delete(histo1[1],-1),histo1[0]
    histo2 = np.histogram(r21[dist<def_nucleus[i]],bins=bins,range=(xlim),
                          weights=w3[dist<def_nucleus[i]])
    histo2x,histo2y = np.delete(histo2[1],-1),histo2[0]
    histo3 = np.histogram(r21[dist>def_nucleus[i]],bins=bins,range=(xlim),
                          weights=w3[dist>def_nucleus[i]])
    histo3x,histo3y = np.delete(histo3[1],-1),histo3[0]

    # kernel density estimation
    y11 = histo1y/float(sum(histo1y))
    y12 = histo2y/float(sum(histo1y))
    y13 = histo3y/float(sum(histo1y))
    med1 = weighted_median(r21,Ico21)
    med2 = weighted_median(r21[dist<def_nucleus[i]],Ico21[dist<def_nucleus[i]])
    med3 = weighted_median(r21[dist>def_nucleus[i]],Ico21[dist>def_nucleus[i]])

    # plt4
    plt4.plot(histo1x,y11,"black",lw=5,alpha=0.5)
    plt4.plot(histo1x,y12,c=cm.brg(i/2.5),ls="dotted",lw=2,alpha=1.0)
    plt4.plot(histo1x,y13,c=cm.brg(i/2.5),ls="-",lw=5,alpha=0.5)
    plt4.plot(med1, 0.15, ".", markersize=14,c="black")
    plt4.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/2.5))
    plt4.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/2.5))
    plt4.plot([histo1x[hist_percent(histo1y,0.157)],
               histo1x[hist_percent(histo1y,0.843)]],
              [0.15,0.15],c="black",lw=3,alpha=0.5)
    plt4.plot([histo2x[hist_percent(histo2y,0.157)],
               histo2x[hist_percent(histo2y,0.843)]],
              [0.14,0.14],c=cm.brg(i/2.5),lw=3,alpha=1.0,linestyle="dotted")
    plt4.plot([histo3x[hist_percent(histo3y,0.157)],
               histo3x[hist_percent(histo3y,0.843)]],
              [0.13,0.13],c=cm.brg(i/2.5),lw=3,alpha=0.5)

    #plt4.set_yscale("log")
    plt4.set_xlim(xlim)
    plt4.set_ylim(ylim)
    """

    plt1.tick_params(labelbottom=False)
    plt2.tick_params(labelleft=False,labelbottom=False)
    plt3.tick_params(labelleft=False,labelbottom=False)
    plt4.tick_params(labelleft=False,labelbottom=False)
    #plt1.set_yticks(np.arange(0.9, ylim[1]+0.01, 0.9))
    #plt2.set_yticks(np.arange(0.9, ylim[1]+0.01, 0.9))
    #plt3.set_yticks(np.arange(0.9, ylim[1]+0.01, 0.9))

    txt_x = xlim[0]+(xlim[1]-xlim[0])*0.67
    bm = float(beam[i].replace("p","."))
    bm_arc = str(round(bm,1)).replace(".","\".")
    bm_kpc = str(int(round(bm*scales[i],-1)))+" pc"
    plt1.text(txt_x,ylim[1]*0.55,name_title+"\n"+bm_arc+"\n"+bm_kpc)

    if gals[i]=="ngc0628":
        plt1.text(xlim[0]+(xlim[1]-xlim[0])*0.0,ylim[1]*1.04,"# of Sightlines")
        plt2.text(xlim[0]+(xlim[1]-xlim[0])*0.0,ylim[1]*1.04,"CO(1-0) Flux")
        plt3.text(xlim[0]+(xlim[1]-xlim[0])*0.0,ylim[1]*1.04,"CO(2-1) Flux")

    if gals[i]=="ngc4321":
        plt1.set_xlabel("$R_{21}$")
        plt2.set_xlabel("$R_{21}$")
        plt3.set_xlabel("$R_{21}$")
        plt1.tick_params(labelbottom=True)
        plt2.tick_params(labelleft=False,labelbottom=True)
        plt3.tick_params(labelleft=False,labelbottom=True)

    plt1.legend()
    plt2.legend()
    plt3.legend()

    plt1.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))
    plt2.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))
    plt3.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))

    plt.savefig(dir_data+"eps/figure_hists_"+gals[i]+".png",dpi=100)

os.system("rm -rf *.last")
