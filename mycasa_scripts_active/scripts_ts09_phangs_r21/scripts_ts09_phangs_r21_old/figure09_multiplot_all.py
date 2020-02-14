import os
import sys
import glob
import math
import numpy as np
import scipy.stats as stats
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
snr = 3
ylim = [-1.2,0.8]
dir_data = "/Users/saito/data/phangs/co_ratio/"
gals = ["ngc0628", "ngc3627", "ngc4254", "ngc4321"]
beam = [13.6,8.2,15.0,7.51]
scales = [44/1.0/1000, 103/1.4/1000, 52/1.3/1000, 130/1.6/1000]
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
incs = [8.7,
        56.2,
        35.2,
        35.1]
Trms_co10 = [0.05,0.026,0.04,0.02]
Trms_co21 = [0.1,0.03,0.04,0.03]
velres = [2.0,2.5,2.5,2.5]


#####################
### functions
#####################
def density_estimation(m1,m2,xlim,ylim):
    X, Y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])
    kernel = stats.gaussian_kde(values, bw_method=0.4)
    Z = np.reshape(kernel(positions).T, X.shape)
    return X, Y, Z

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

def distance(x, y, pa, inc, ra_cnt, dec_cnt, scale):
    tilt_cos = math.cos(math.radians(pa))
    tilt_sin = math.sin(math.radians(pa))
    
    x_tmp = x - ra_cnt
    y_tmp = y - dec_cnt
    
    x_new = (x_tmp*tilt_cos - y_tmp*tilt_sin)
    y_new = (x_tmp*tilt_sin + y_tmp*tilt_cos) * 1/math.sin(math.radians(inc))
    
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale
    
    return r

def setup_ax1(ax,x,y,xlim,ylim,ylabel,title,j):
    ax.grid(axis="both")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    if ylabel==True:
        ax.tick_params(labelbottom=False)
        ax.set_ylabel("log $R_{21}$")
    else:
        ax.tick_params(labelleft=False,labelbottom=False)
    ax.plot(x,y,"o",
            color=cm.rainbow(j/11.),
            markeredgewidth=0,alpha=0.1,markersize=4)
    X,Y,Z=density_estimation(x,y,xlim,ylim)
    #ax.contour(X,Y,Z,colors="black",levels=[0.05,0.5,3]*np.max(Z),linewidths=2)
    #coef = str(np.round(np.corrcoef(x,y)[0][1],2))
    ax.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.08,
            title)

def setup_ax2(ax,x,bins,xlim,xlabel,j):
    ax.grid(axis="x")
    ax.tick_params(labelleft=False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(top=False,left=False,right=False)
    hist=ax.hist(x,bins=bins,range=xlim,
                 color=cm.rainbow(j/11.),
                 lw=0,alpha=0.0,align="mid")
    ax.plot(np.delete(hist[1],-1),hist[0],drawstyle="steps-post",
            color=cm.rainbow(j/11.),lw=2)
    ax.set_xlim(xlim)
    ax.set_ylim(hist[0].max()*1.1,0)
    ax.set_xlabel(xlabel)

def check_nchan(dir_data,gal,suffix):
    """
    """
    imagename = dir_data+gal+"_combine_"+suffix+".mask"
    outfile = imagename.replace(".mask",".nchan")
    os.system("rm -rf "+outfile)
    immoments(imagename=imagename,
              moments=[0],
              outfile=outfile)

def import_data_gal(dir_data,gal,beam):
    """
    """
    name_title = gal.replace("ngc","NGC ")
    beamfloat = float(beam)
    suffix = str(beam).replace(".","p")
    d_fits = dir_data+gal+"_wise/"
    ra_tmp_ = import_data(d_fits,gal,"co10",suffix,
                           "moment0","coords","ra")
    dec_tmp_ = import_data(d_fits,gal,"co10",suffix,
                            "moment0","coords","dec",1)
    Ico10_tmp_ = import_data(d_fits,gal,"co10",suffix,
                              "moment0","data","Ico10")
    Ico21_tmp_ = import_data(d_fits,gal,"co21",suffix,
                              "moment0","data","Ico21")
    Tco21_tmp_ = import_data(d_fits,gal,"co21",suffix,
                              "moment8","data","Tco21")
    Sco21_tmp_ = import_data(d_fits,gal,"co21",suffix,
                              "moment2","data","Sco21")
    co10_jy2k = 1.222e6 / beam**2 / 115.27120**2
    co21_jy2k = 1.222e6 / beam**2 / 230.53800**2
    w1_tmp_ = import_data(d_fits,gal,"w1",suffix,
                           "image","data","w1")
    w2_tmp_ = import_data(d_fits,gal,"w2",suffix,
                           "image","data","w2")
    w3_tmp_ = import_data(d_fits,gal,"w3",suffix,
                           "image","data","w3")
    check_nchan(d_fits,gal,suffix)
    nchan_tmp_ = import_data(d_fits,gal,"combine",suffix,
                              "nchan","data","nchan")

    return name_title, ra_tmp_, dec_tmp_, Ico10_tmp_, Ico21_tmp_, Tco21_tmp_, Sco21_tmp_, w1_tmp_, w2_tmp_, w3_tmp_, nchan_tmp_, co10_jy2k, co21_jy2k

def define_cut_1a(ra_tmp_,dec_tmp_,Ico10_tmp_,thres_co10,Ico21_tmp_,thres_co21):
    cut_pos = (ra_tmp_ > 0) & (dec_tmp_ > 0)
    cut_co10 = (Ico10_tmp_ > thres_co10)
    cut_co21 = (Ico21_tmp_ > thres_co21)
    cut_all = np.where((cut_pos) & (cut_co10) & (cut_co21))
    
    return cut_all

def setup_1a(Trms_co10,
             Trms_co21,
             snr,
             nchan_tmp_,
             velres,
             ra_tmp_,
             dec_tmp_,
             Ico10_tmp_,
             Ico21_tmp_,
             co10_jy2k,
             co21_jy2k,
             pa,
             inc,
             cnt_ra,
             cnt_dec,
             scale):
    """
    """
    thco10 = Trms_co10*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    thco21 = Trms_co21*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    cut_all=define_cut_1a(ra_tmp_,dec_tmp_,Ico10_tmp_,thco10,Ico21_tmp_,thco21)
    ra = ra_tmp_[cut_all] * 180/pi # deg
    dec = dec_tmp_[cut_all] * 180/pi # deg
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
    r21 = Ico21/Ico10
    x_tmp_ = distance(ra,dec,pa,inc,cnt_ra,cnt_dec,scale)
    y_tmp_ = r21
    y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
    x = np.log10(x_tmp_[y_tmp_>0])
    y = np.log10(y_tmp_[y_tmp_>0])

    return x, y

def define_cut_1b(Ico10_tmp_,thres_co10,Ico21_tmp_,thres_co21):
    cut_co10 = (Ico10_tmp_ > thres_co10)
    cut_co21 = (Ico21_tmp_ > thres_co21)
    cut_all = np.where((cut_co10) & (cut_co21))
    
    return cut_all

def setup_1b(Trms_co10,
             Trms_co21,
             snr,
             nchan_tmp_,
             velres,
             Ico10_tmp_,
             Ico21_tmp_,
             co10_jy2k,
             co21_jy2k):
    """
    """
    thco10 = Trms_co10*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    thco21 = Trms_co21*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    cut_all=define_cut_1b(Ico10_tmp_,thco10,Ico21_tmp_,thco21)
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
    r21 = Ico21/Ico10
    x_tmp_ = Ico21
    y_tmp_ = r21
    y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
    x = np.log10(x_tmp_[y_tmp_>0])
    y = np.log10(y_tmp_[y_tmp_>0])
    
    return x, y

def define_cut_1c(Tco21_tmp_,Trms_co21,
                  Ico10_tmp_,thres_co10,Ico21_tmp_,thres_co21):
    cut_Tco21 = (Tco21_tmp_ > Trms_co21)
    cut_co10 = (Ico10_tmp_ > thres_co10)
    cut_co21 = (Ico21_tmp_ > thres_co21)
    cut_all = np.where((cut_Tco21) & (cut_co10) & (cut_co21))
    
    return cut_all

def setup_1c(Trms_co10,
             Trms_co21,
             snr,
             nchan_tmp_,
             velres,
             Ico10_tmp_,
             Ico21_tmp_,
             co10_jy2k,
             co21_jy2k,
             Tco21_tmp_):
    """
    """
    thco10 = Trms_co10*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    thco21 = Trms_co21*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    Tthco21 = Trms_co21*snr #
    cut_all=define_cut_1c(Tco21_tmp_,Tthco21, #
                          Ico10_tmp_,thco10,Ico21_tmp_,thco21)
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
    r21 = Ico21/Ico10
    Tco21 = Tco21_tmp_[cut_all] * co21_jy2k #
    x_tmp_ = Tco21 #
    y_tmp_ = r21
    y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
    x = np.log10(x_tmp_[y_tmp_>0])
    y = np.log10(y_tmp_[y_tmp_>0])
    
    return x, y

def define_cut_1d(Sco21_tmp_,
                  Ico10_tmp_,thres_co10,Ico21_tmp_,thres_co21):
    cut_co10 = (Ico10_tmp_ > thres_co10)
    cut_co21 = (Ico21_tmp_ > thres_co21)
    cut_sigma = (Sco21_tmp_ > 5)
    cut_all = np.where((cut_sigma) & (cut_co10) & (cut_co21))
    
    return cut_all

def setup_1d(Trms_co10,
             Trms_co21,
             snr,
             nchan_tmp_,
             velres,
             Ico10_tmp_,
             Ico21_tmp_,
             co10_jy2k,
             co21_jy2k,
             Sco21_tmp_):
    """
    """
    thco10 = Trms_co10*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    thco21 = Trms_co21*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    cut_all=define_cut_1d(Sco21_tmp_, #
                          Ico10_tmp_,thco10,Ico21_tmp_,thco21)
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
    r21 = Ico21/Ico10
    Sco21_tmp_ = Sco21_tmp_[cut_all] #
    x_tmp_ = Sco21_tmp_ #
    y_tmp_ = r21
    y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
    x = np.log10(x_tmp_[y_tmp_>0])
    y = np.log10(y_tmp_[y_tmp_>0])
                          
    return x, y

def setup_2a(Trms_co10,
             Trms_co21,
             snr,
             nchan_tmp_,
             velres,
             Ico10_tmp_,
             Ico21_tmp_,
             co10_jy2k,
             co21_jy2k,
             w1_tmp_):
    """
    """
    thco10 = Trms_co10*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    thco21 = Trms_co21*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    cut_all=define_cut_1b(Ico10_tmp_,thco10,Ico21_tmp_,thco21)
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
    r21 = Ico21/Ico10
    w1 = w1_tmp_[cut_all] #
    x_tmp_ = w1 #
    y_tmp_ = r21
    y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
    x = np.log10(x_tmp_[y_tmp_>0])
    y = np.log10(y_tmp_[y_tmp_>0])
                          
    return x, y

def setup_2d(Trms_co10,
             Trms_co21,
             snr,
             nchan_tmp_,
             velres,
             Ico10_tmp_,
             Ico21_tmp_,
             co10_jy2k,
             co21_jy2k,
             w1_tmp_,
             w3_tmp_):
    """
    """
    thco10 = Trms_co10*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    thco21 = Trms_co21*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    cut_all=define_cut_1b(Ico10_tmp_,thco10,Ico21_tmp_,thco21)
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
    r21 = Ico21/Ico10
    w1 = w1_tmp_[cut_all] #
    w3 = w3_tmp_[cut_all] #
    x_tmp_ = w3/w1 #
    y_tmp_ = r21
    y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
    x = np.log10(x_tmp_[y_tmp_>0])
    y = np.log10(y_tmp_[y_tmp_>0])
    
    return x, y

def setup_3a(Trms_co10,
             Trms_co21,
             snr,
             nchan_tmp_,
             velres,
             Ico10_tmp_,
             Ico21_tmp_,
             co10_jy2k,
             co21_jy2k,
             Tco21_tmp_,
             w1_tmp_):
    """
    """
    thco10 = Trms_co10*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    thco21 = Trms_co21*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    Tthco21 = Trms_co21*snr
    cut_all=define_cut_1c(Tco21_tmp_,Tthco21, #
                          Ico10_tmp_,thco10,Ico21_tmp_,thco21)
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
    r21 = Ico21/Ico10
    w1 = w1_tmp_[cut_all] #
    Tco21 = Tco21_tmp_[cut_all] #
    x_tmp_ = w1/Tco21 #
    y_tmp_ = r21
    y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
    x = np.log10(x_tmp_[y_tmp_>0])
    y = np.log10(y_tmp_[y_tmp_>0])
    
    return x, y

def setup_3d(Trms_co10,
             Trms_co21,
             snr,
             nchan_tmp_,
             velres,
             Ico10_tmp_,
             Ico21_tmp_,
             co10_jy2k,
             co21_jy2k,
             Sco21_tmp_,
             w1_tmp_):
    """
    """
    thco10 = Trms_co10*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    thco21 = Trms_co21*snr*np.sqrt(nchan_tmp_)*np.sqrt(velres)
    cut_all=define_cut_1d(Sco21_tmp_,
                          Ico10_tmp_,thco10,Ico21_tmp_,thco21)
    Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
    Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
    r21 = Ico21/Ico10
    w1 = w1_tmp_[cut_all] #
    Sco21 = Sco21_tmp_[cut_all] #
    x_tmp_ = w1/Sco21 #
    y_tmp_ = r21
    y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
    x = np.log10(x_tmp_[y_tmp_>0])
    y = np.log10(y_tmp_[y_tmp_>0])
                          
    return x, y


#####################
### Main Procedure
#####################
### import data
name_title0, ra_tmp0_, dec_tmp0_, Ico10_tmp0_, Ico21_tmp0_, Tco21_tmp0_, Sco21_tmp0_, w1_tmp0_, w2_tmp0_, w3_tmp0_, nchan_tmp0_, co10_jy2k0, co21_jy2k0 = import_data_gal(dir_data,gals[0],beam[0])
name_title1, ra_tmp1_, dec_tmp1_, Ico10_tmp1_, Ico21_tmp1_, Tco21_tmp1_, Sco21_tmp1_, w1_tmp1_, w2_tmp1_, w3_tmp1_, nchan_tmp1_, co10_jy2k1, co21_jy2k1 = import_data_gal(dir_data,gals[1],beam[1])
name_title2, ra_tmp2_, dec_tmp2_, Ico10_tmp2_, Ico21_tmp2_, Tco21_tmp2_, Sco21_tmp2_, w1_tmp2_, w2_tmp2_, w3_tmp2_, nchan_tmp2_, co10_jy2k2, co21_jy2k2 = import_data_gal(dir_data,gals[2],beam[2])
name_title3, ra_tmp3_, dec_tmp3_, Ico10_tmp3_, Ico21_tmp3_, Tco21_tmp3_, Sco21_tmp3_, w1_tmp3_, w2_tmp3_, w3_tmp3_, nchan_tmp3_, co10_jy2k3, co21_jy2k3 = import_data_gal(dir_data,gals[3],beam[3])

### plot data 1a
x0, y0 = setup_1a(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  ra_tmp0_,dec_tmp0_,Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,
                  co21_jy2k0,pas[0],incs[0],cnt_ras[0],cnt_decs[0],scales[0])
x1, y1 = setup_1a(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  ra_tmp1_,dec_tmp1_,Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,
                  co21_jy2k1,pas[1],incs[1],cnt_ras[1],cnt_decs[1],scales[1])
x2, y2 = setup_1a(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  ra_tmp2_,dec_tmp2_,Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,
                  co21_jy2k2,pas[2],incs[2],cnt_ras[2],cnt_decs[2],scales[2])
x3, y3 = setup_1a(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  ra_tmp3_,dec_tmp3_,Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,
                  co21_jy2k3,pas[3],incs[3],cnt_ras[3],cnt_decs[3],scales[3])
title = "a) Radial log $R_{21}$"
xlabel = "log Deprojected Distance (kpc)"
xlim = [-1.0,x0.max()+0.2]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot1a.png",dpi=200)

### plot data 1b
x0, y0 = setup_1b(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0)
x1, y1 = setup_1b(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1)
x2, y2 = setup_1b(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2)
x3, y3 = setup_1b(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3)
title = "b) log $R_{21}$ vs log $I_{CO(2-1)}$"
xlabel = "log $I_{CO(2-1)}$ (K km s$^{-1}$)"
xlim = [-0.9,2.5]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot1b.png",dpi=200)

### plot data 1c
x0, y0 = setup_1c(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0,Tco21_tmp0_)
x1, y1 = setup_1c(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1,Tco21_tmp1_)
x2, y2 = setup_1c(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2,Tco21_tmp2_)
x3, y3 = setup_1c(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3,Tco21_tmp3_)
title = "c) log $R_{21}$ vs log $T_{CO(2-1)}$"
xlabel = "log $T_{CO(2-1)}$ (K)"
xlim = [-2.0,0.5]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot1c.png",dpi=200)

### plot data 1d
x0, y0 = setup_1d(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0,Sco21_tmp0_)
x1, y1 = setup_1d(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1,Sco21_tmp1_)
x2, y2 = setup_1d(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2,Sco21_tmp2_)
x3, y3 = setup_1d(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3,Sco21_tmp3_)
title = "d) log $R_{21}$ vs log $\sigma_{CO(2-1)}$"
xlabel = "log $\sigma_{CO(2-1)}$ (km s$^{-1}$)"
xlim = [0.6,1.8]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot1d.png",dpi=200)

### plot data 2a
x0, y0 = setup_2a(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0,w1_tmp0_)
x1, y1 = setup_2a(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1,w1_tmp1_)
x2, y2 = setup_2a(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2,w1_tmp2_)
x3, y3 = setup_2a(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3,w1_tmp3_)
title = "e) log $R_{21}$ vs log W1"
xlabel = "log W1 (Jy beam$^{-1}$)"
xlim = [-4.0,-1.0]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot2a.png",dpi=200)

### plot data 2b
x0, y0 = setup_2a(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0,w2_tmp0_)
x1, y1 = setup_2a(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1,w2_tmp1_)
x2, y2 = setup_2a(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2,w2_tmp2_)
x3, y3 = setup_2a(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3,w2_tmp3_)
title = "f) log $R_{21}$ vs log W2"
xlabel = "log W2 (Jy beam$^{-1}$)"
xlim = [-4.1,-1.1]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot2b.png",dpi=200)

### plot data 2c
x0, y0 = setup_2a(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0,w3_tmp0_)
x1, y1 = setup_2a(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1,w3_tmp1_)
x2, y2 = setup_2a(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2,w3_tmp2_)
x3, y3 = setup_2a(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3,w3_tmp3_)
title = "f) log $R_{21}$ vs log W3"
xlabel = "log W3 (Jy beam$^{-1}$)"
xlim = [-4.1,-0.6]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot2c.png",dpi=200)

### plot data 2d
x0, y0 = setup_2d(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0,
                  w1_tmp0_,w3_tmp0_)
x1, y1 = setup_2d(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1,
                  w1_tmp1_,w3_tmp1_)
x2, y2 = setup_2d(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2,
                  w1_tmp2_,w3_tmp2_)
x3, y3 = setup_2d(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3,
                  w1_tmp3_,w3_tmp3_)
title = "f) log $R_{21}$ vs log W3/W1"
xlabel = "log W3/W1"
xlim = [-0.5,1.2]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot2d.png",dpi=200)

### plot data 3a
x0, y0 = setup_3a(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0,
                  Tco21_tmp0_,w1_tmp0_)
x1, y1 = setup_3a(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1,
                  Tco21_tmp1_,w1_tmp1_)
x2, y2 = setup_3a(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2,
                  Tco21_tmp2_,w1_tmp2_)
x3, y3 = setup_3a(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3,
                  Tco21_tmp3_,w1_tmp3_)
title = "i) log $R_{21}$ vs log W1/$T_{CO(2-1)}$"
xlabel = "log W1/$T_{CO(2-1)}$"
xlim = [-3.6,-1.2]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot3a.png",dpi=200)

### plot data 3b
x0, y0 = setup_3a(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0,
                  Tco21_tmp0_,w2_tmp0_)
x1, y1 = setup_3a(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1,
                  Tco21_tmp1_,w2_tmp1_)
x2, y2 = setup_3a(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2,
                  Tco21_tmp2_,w2_tmp2_)
x3, y3 = setup_3a(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3,
                  Tco21_tmp3_,w2_tmp3_)
title = "i) log $R_{21}$ vs log W2/$T_{CO(2-1)}$"
xlabel = "log W2/$T_{CO(2-1)}$"
xlim = [-3.6,-1.2]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot3b.png",dpi=200)

### plot data 3c
x0, y0 = setup_3a(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0,
                  Tco21_tmp0_,w3_tmp0_)
x1, y1 = setup_3a(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1,
                  Tco21_tmp1_,w3_tmp1_)
x2, y2 = setup_3a(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2,
                  Tco21_tmp2_,w3_tmp2_)
x3, y3 = setup_3a(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3,
                  Tco21_tmp3_,w3_tmp3_)
title = "i) log $R_{21}$ vs log W3/$T_{CO(2-1)}$"
xlabel = "log W3/$T_{CO(2-1)}$"
xlim = [-3.6,-1.2]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/fig09_allmplot3c.png",dpi=200)

### plot data 3d
x0, y0 = setup_3d(Trms_co10[0],Trms_co21[0],snr,nchan_tmp0_,velres[0],
                  Ico10_tmp0_,Ico21_tmp0_,co10_jy2k0,co21_jy2k0,
                  Sco21_tmp0_,w3_tmp0_)
x1, y1 = setup_3d(Trms_co10[1],Trms_co21[1],snr,nchan_tmp1_,velres[1],
                  Ico10_tmp1_,Ico21_tmp1_,co10_jy2k1,co21_jy2k1,
                  Sco21_tmp1_,w3_tmp1_)
x2, y2 = setup_3d(Trms_co10[2],Trms_co21[2],snr,nchan_tmp2_,velres[2],
                  Ico10_tmp2_,Ico21_tmp2_,co10_jy2k2,co21_jy2k2,
                  Sco21_tmp2_,w3_tmp2_)
x3, y3 = setup_3d(Trms_co10[3],Trms_co21[3],snr,nchan_tmp3_,velres[3],
                  Ico10_tmp3_,Ico21_tmp3_,co10_jy2k3,co21_jy2k3,
                  Sco21_tmp3_,w3_tmp3_)
title = "l) log $R_{21}$ vs log W3/$\sigma_{CO(2-1)}$"
xlabel = "log W3/$\sigma_{CO(2-1)}$"
xlim = [-5.2,-2.2]
figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x3,y3,xlim,ylim,True,title,0)
setup_ax1(ax1,x2,y2,xlim,ylim,True,title,3)
setup_ax1(ax1,x1,y1,xlim,ylim,True,title,7)
setup_ax1(ax1,x0,y0,xlim,ylim,True,title,11)
setup_ax2(ax2,x0,60,xlim,xlabel,11)
setup_ax2(ax2,x1,60,xlim,xlabel,7)
setup_ax2(ax2,x2,60,xlim,xlabel,3)
setup_ax2(ax2,x3,60,xlim,xlabel,0)
plt.subplots_adjust(bottom=0.15, wspace=0.05)

plt.text(0, 0, "NGC 0628", color=cm.rainbow(0/11.))
plt.legend()
plt.savefig(dir_data+"eps/fig09_allmplot3d.png",dpi=200)


