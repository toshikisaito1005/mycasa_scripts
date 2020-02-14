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
snr = 3.0
def_nucleus = [2200,2000,4063,3680] # pc [50".0,50".0,,]
dir_data = "/Users/saito/data/phangs/co_ratio/"
gals = ["ngc0628", "ngc3627", "ngc4254", "ngc4321"]
beam = ["13p6","15p0","8p0","8p2"]
scales = [44/1.0, 52/1.3, 130/1.6, 103/1.4]
Irms_co10 = [0.05*sqrt(2.0),
             0.026*sqrt(2.5),
             0.04*sqrt(2.5),
             0.02*sqrt(2.5)]
Irms_co21 = [0.1*sqrt(2.0),
             0.03*sqrt(2.5),
             0.04*sqrt(2.5),
             0.03*sqrt(2.5)]
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

bins=50
step=0.03
xlim = [0.05,1.35]
ylim = [0,0.16]#[10**-2.9,10**-0.5]


#####################
### functions
#####################
def func1(x, a, b, c):
    return a*np.exp(-(x-b)**2/(2*c**2))

def fit_func1(func1, data_x, data_y, guess):
    """
    fit data with func1
    """
    popt, pcov = curve_fit(func1,
                           data_x, data_y,
                           p0=guess)
    best_func = func1(data_x,popt[0],popt[1],popt[2])
    residual = data_y - best_func
                           
    return popt, residual

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

def distance(x, y, pa, inc, ra_cnt, dec_cnt, scale):
    tilt_cos = math.cos(math.radians(pa))
    tilt_sin = math.sin(math.radians(pa))
    
    x_tmp = x - ra_cnt
    y_tmp = y - dec_cnt
    
    x_new = (x_tmp*tilt_cos - y_tmp*tilt_sin)
    y_new = (x_tmp*tilt_sin + y_tmp*tilt_cos) * 1/math.sin(math.radians(inc))
    
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale # arcsec * pc/arcsec
    
    return r

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

#for i in range(len(gals)):
for i in [0,1,2,3]:
    name_title = gals[i].replace("ngc","NGC ")
    beamfloat = float(beam[i].replace("p","."))
    d_fits = dir_data+gals[i]+"_wise/"

    # import data
    ra_tmp_ = import_data(d_fits,gals[i],"co10",beam[i],
                          "moment0","coords","ra")
    dec_tmp_ = import_data(d_fits,gals[i],"co10",beam[i],
                           "moment0","coords","dec",1)
    Ico10_tmp_ = import_data(d_fits,gals[i],"co10",beam[i],
                             "moment0","data","Ico10")
    Ico21_tmp_ = import_data(d_fits,gals[i],"co21",beam[i],
                             "moment0","data","Ico21")
    w3_tmp_ = import_data(d_fits,gals[i],"w3",beam[i],
                          "image","data","w3")
    co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
    co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2

    check_nchan(d_fits,gals[i],beam[i])
    nchan_tmp_ = import_data(d_fits,gals[i],"combine",beam[i],
                             "nchan","data","nchan")

    # define cut
    cut_pos = (ra_tmp_ > 0) & (dec_tmp_ > 0)
    cut_co10 = (Ico10_tmp_>Irms_co10[i]*snr*np.sqrt(nchan_tmp_))
    cut_co21 = (Ico21_tmp_ > Irms_co21[i]*snr*np.sqrt(nchan_tmp_))
    cut_all = np.where((cut_pos) & (cut_co10) & (cut_co21))

    # cut data
    ra = ra_tmp_[cut_all] * 180/pi # deg
    dec = dec_tmp_[cut_all] * 180/pi # deg
    Ico21_tmp2_ = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10_tmp2_ = Ico10_tmp_[cut_all] * co10_jy2k
    r21_tmp2_ = Ico21_tmp2_/Ico10_tmp2_
    r21_tmp2_[np.where(np.isnan(r21_tmp2_) & np.isinf(r21_tmp2_))] = 0
    w3 = w3_tmp_[cut_all]

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
    plt4 = plt.subplot(gs[1:7,12:16])
    plt1.grid(axis="x")
    plt2.grid(axis="x")
    plt3.grid(axis="x")
    plt4.grid(axis="x")

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
    plt1.plot(histo1x,y12,c=cm.brg(i/3.5),ls="dotted",lw=2,alpha=1.0)
    plt1.plot(histo1x,y13,c=cm.brg(i/3.5),ls="-",lw=5,alpha=0.5)
    plt1.plot(med1, 0.15, ".", markersize=14,c="black")
    plt1.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/3.5))
    plt1.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/3.5))
    plt1.plot([histo1x[hist_percent(histo1y,0.157)],
               histo1x[hist_percent(histo1y,0.843)]],
              [0.15,0.15],c="black",lw=3,alpha=0.5)
    plt1.plot([histo2x[hist_percent(histo2y,0.157)],
               histo2x[hist_percent(histo2y,0.843)]],
              [0.14,0.14],c=cm.brg(i/3.5),lw=3,alpha=1.0,linestyle="dotted")
    plt1.plot([histo3x[hist_percent(histo3y,0.157)],
               histo3x[hist_percent(histo3y,0.843)]],
              [0.13,0.13],c=cm.brg(i/3.5),lw=3,alpha=0.5)
    
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
    plt2.plot(histo1x,y12,c=cm.brg(i/3.5),ls="dotted",lw=2,alpha=1.0)
    plt2.plot(histo1x,y13,c=cm.brg(i/3.5),ls="-",lw=5,alpha=0.5)
    plt2.plot(med1, 0.15, ".", markersize=14,c="black")
    plt2.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/3.5))
    plt2.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/3.5))
    plt2.plot([histo1x[hist_percent(histo1y,0.157)],
               histo1x[hist_percent(histo1y,0.843)]],
              [0.15,0.15],c="black",lw=3,alpha=0.5)
    plt2.plot([histo2x[hist_percent(histo2y,0.157)],
               histo2x[hist_percent(histo2y,0.843)]],
              [0.14,0.14],c=cm.brg(i/3.5),lw=3,alpha=1.0,linestyle="dotted")
    plt2.plot([histo3x[hist_percent(histo3y,0.157)],
               histo3x[hist_percent(histo3y,0.843)]],
              [0.13,0.13],c=cm.brg(i/3.5),lw=3,alpha=0.5)
    
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
    plt3.plot(histo1x,y12,c=cm.brg(i/3.5),ls="dotted",lw=2,alpha=1.0)
    plt3.plot(histo1x,y13,c=cm.brg(i/3.5),ls="-",lw=5,alpha=0.5)
    plt3.plot(med1, 0.15, ".", markersize=14,c="black")
    plt3.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/3.5))
    plt3.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/3.5))
    plt3.plot([histo1x[hist_percent(histo1y,0.157)],
               histo1x[hist_percent(histo1y,0.843)]],
              [0.15,0.15],c="black",lw=3,alpha=0.5)
    plt3.plot([histo2x[hist_percent(histo2y,0.157)],
               histo2x[hist_percent(histo2y,0.843)]],
              [0.14,0.14],c=cm.brg(i/3.5),lw=3,alpha=1.0,linestyle="dotted")
    plt3.plot([histo3x[hist_percent(histo3y,0.157)],
               histo3x[hist_percent(histo3y,0.843)]],
              [0.13,0.13],c=cm.brg(i/3.5),lw=3,alpha=0.5)

    #plt3.set_yscale("log")
    plt3.set_xlim(xlim)
    plt3.set_ylim(ylim)
    
    ## hist 4
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
    plt4.plot(histo1x,y12,c=cm.brg(i/3.5),ls="dotted",lw=2,alpha=1.0)
    plt4.plot(histo1x,y13,c=cm.brg(i/3.5),ls="-",lw=5,alpha=0.5)
    plt4.plot(med1, 0.15, ".", markersize=14,c="black")
    plt4.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/3.5))
    plt4.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/3.5))
    plt4.plot([histo1x[hist_percent(histo1y,0.157)],
               histo1x[hist_percent(histo1y,0.843)]],
              [0.15,0.15],c="black",lw=3,alpha=0.5)
    plt4.plot([histo2x[hist_percent(histo2y,0.157)],
               histo2x[hist_percent(histo2y,0.843)]],
              [0.14,0.14],c=cm.brg(i/3.5),lw=3,alpha=1.0,linestyle="dotted")
    plt4.plot([histo3x[hist_percent(histo3y,0.157)],
               histo3x[hist_percent(histo3y,0.843)]],
              [0.13,0.13],c=cm.brg(i/3.5),lw=3,alpha=0.5)

    #plt4.set_yscale("log")
    plt4.set_xlim(xlim)
    plt4.set_ylim(ylim)

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
        plt4.text(xlim[0]+(xlim[1]-xlim[0])*0.0,ylim[1]*1.04,"W3 Flux")

    if gals[i]=="ngc4321":
        plt1.set_xlabel("$R_{21}$")
        plt2.set_xlabel("$R_{21}$")
        plt3.set_xlabel("$R_{21}$")
        plt4.set_xlabel("$R_{21}$")
        plt1.tick_params(labelbottom=True)
        plt2.tick_params(labelleft=False,labelbottom=True)
        plt3.tick_params(labelleft=False,labelbottom=True)
        plt4.tick_params(labelleft=False,labelbottom=True)

    plt1.legend()
    plt2.legend()
    plt3.legend()
    plt4.legend()

    plt1.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))
    plt2.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))
    plt3.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))
    plt4.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))

    plt.savefig(dir_data+"eps/figure_hists_"+gals[i]+"_wise.png",dpi=100)

