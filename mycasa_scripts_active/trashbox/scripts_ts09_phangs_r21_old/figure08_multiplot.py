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
i = 3
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
incs = [90-8.7,
        90-56.2,
        90-35.2,
        90-35.1]
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
            markeredgewidth=0,alpha=0.1,markersize=9)
    X,Y,Z=density_estimation(x,y,xlim,ylim)
    ax.contour(X,Y,Z,
               colors="black",
               levels=[0.05,0.5,2]*np.max(Z),
               linewidths=2,zorder=1000000)
    coef = str(np.round(np.corrcoef(x,y)[0][1],2))
    ax.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.08,
            title+r" ($\rho$ = "+str(coef)+")")

def setup_ax2(ax,x,bins,xlim,xlabel,j):
    ax.grid(axis="x")
    ax.tick_params(labelleft=False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(top=False,left=False,right=False)
    hist=ax.hist(x,bins=bins,range=xlim,
                 color=cm.rainbow(j/11.),
                 lw=0,alpha=0.4,align="mid")
    ax.plot(np.delete(hist[1],-1),hist[0],drawstyle="steps-post",
            color="black",lw=2)
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


#####################
### Main Procedure
#####################
name_title = gals[i].replace("ngc","NGC ")
beamfloat = float(beam[i])
suffix = str(beam[i]).replace(".","p")
d_fits = dir_data+gals[i]+"_wise/"

### import data
ra_tmp_ = import_data(d_fits,gals[i],"co10",suffix,"moment0","coords","ra")
dec_tmp_ = import_data(d_fits,gals[i],"co10",suffix,"moment0","coords","dec",1)
Ico10_tmp_ = import_data(d_fits,gals[i],"co10",suffix,"moment0","data","Ico10")
Ico21_tmp_ = import_data(d_fits,gals[i],"co21",suffix,"moment0","data","Ico21")
Tco21_tmp_ = import_data(d_fits,gals[i],"co21",suffix,"moment8","data","Tco21")
Sco21_tmp_ = import_data(d_fits,gals[i],"co21",suffix,"moment2","data","Sco21")
co10_jy2k = 1.222e6 / beam[i]**2 / 115.27120**2
co21_jy2k = 1.222e6 / beam[i]**2 / 230.53800**2
w1_tmp_ = import_data(d_fits,gals[i],"w1",suffix,"image","data","w1")
w2_tmp_ = import_data(d_fits,gals[i],"w2",suffix,"image","data","w2")
w3_tmp_ = import_data(d_fits,gals[i],"w3",suffix,"image","data","w3")

check_nchan(d_fits,gals[i],suffix)
nchan_tmp_ = import_data(d_fits,gals[i],"combine",suffix,
                         "nchan","data","nchan")

### plot data 1a
j = 0
# define cut
cut_pos = (ra_tmp_ > 0) & (dec_tmp_ > 0)
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_all = np.where((cut_pos) & (cut_co10) & (cut_co21))

# cut data
ra = ra_tmp_[cut_all] * 180/np.pi # deg
dec = dec_tmp_[cut_all] * 180/np.pi # deg
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = distance(ra,dec,pas[i],incs[i],cnt_ras[i],cnt_decs[i],scales[i])
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "a) Radial log $R_{21}$"
xlabel = "log Deprojected Distance (kpc)"
xlim = [-0.6,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,True,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot1a.png",dpi=200)

### plot data 1b
j += 1
# define cut
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_all = np.where((cut_co10) & (cut_co21))

# cut data
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = Ico21
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "b) log $R_{21}$ vs log $I_{CO(2-1)}$"
xlabel = "log $I_{CO(2-1)}$ (K km s$^{-1}$)"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,False,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot1b.png",dpi=200)

### plot data 1c
j += 1
# define cut
cut_Tco21 = (Tco21_tmp_ > Trms_co21[i]*snr)
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_all = np.where((cut_Tco21) & (cut_co10) & (cut_co21))

# cut data
Tco21 = Tco21_tmp_[cut_all] * co21_jy2k
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = Tco21
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "c) log $R_{21}$ vs log $T_{CO(2-1)}$"
xlabel = "log $T_{CO(2-1)}$ (K)"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,False,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot1c.png",dpi=200)

### plot data 1d
j += 1
# define cut
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_sigma = (Sco21_tmp_ > 5)
cut_all = np.where((cut_co10) & (cut_co21) & (cut_sigma))

# cut data
Sco21 = Sco21_tmp_[cut_all]
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = Sco21
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "d) log $R_{21}$ vs log $\sigma_{CO(2-1)}$"
xlabel = "log $\sigma_{CO(2-1)}$ (km s$^{-1}$)"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,False,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot1d.png",dpi=200)

### plot data 2a
j += 1
# define cut
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_all = np.where((cut_co10) & (cut_co21))

# cut data
w1 = w1_tmp_[cut_all]
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = w1
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "e) log $R_{21}$ vs log W1"
xlabel = "log W1 (Jy beam$^{-1}$)"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,True,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot2a.png",dpi=200)

### plot data 2b
j += 1
# define cut
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_all = np.where((cut_co10) & (cut_co21))

# cut data
w2 = w2_tmp_[cut_all]
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = w2
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "f) log $R_{21}$ vs log W2"
xlabel = "log W2 (Jy beam$^{-1}$)"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,False,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot2b.png",dpi=200)

### plot data 2c
j += 1
# define cut
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_all = np.where((cut_co10) & (cut_co21))

# cut data
w3 = w3_tmp_[cut_all]
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = w3
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "g) log $R_{21}$ vs log W3"
xlabel = "log W3 (Jy beam$^{-1}$)"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,False,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot2c.png",dpi=200)

### plot data 2d
j += 1
# define cut
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_all = np.where((cut_co10) & (cut_co21))

# cut data
w1 = w1_tmp_[cut_all]
w3 = w3_tmp_[cut_all]
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = w3/w1
y_tmp_ = r21
x_tmp_[np.where(np.isnan(x_tmp_) & np.isinf(x_tmp_))] = 0
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[np.where((x_tmp_>0)&(y_tmp_>0))])
y = np.log10(y_tmp_[np.where((x_tmp_>0)&(y_tmp_>0))])

# plot
title = "h) log $R_{21}$ vs log W3/W1"
xlabel = "log W3/W1"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,False,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot2d.png",dpi=200)

### plot data 3a
j += 1
# define cut
cut_Tco21 = (Tco21_tmp_ > Trms_co21[i]*snr)
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_all = np.where((cut_Tco21) & (cut_co10) & (cut_co21))

# cut data
w1 = w1_tmp_[cut_all]
Tco21 = Tco21_tmp_[cut_all]
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = w1/Tco21
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "i) log $R_{21}$ vs log W3/$T_{CO(2-1)}$"
xlabel = "log W3/$T_{CO(2-1)}$"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,True,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot3a.png",dpi=200)

### plot data 3b
j += 1
# define cut
cut_Tco21 = (Tco21_tmp_ > Trms_co21[i]*snr)
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_all = np.where((cut_Tco21) & (cut_co10) & (cut_co21))

# cut data
w2 = w2_tmp_[cut_all]
Tco21 = Tco21_tmp_[cut_all]
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = w2/Tco21
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "j) log $R_{21}$ vs log W2/$T_{CO(2-1)}$"
xlabel = "log W2/$T_{CO(2-1)}$"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,False,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot3b.png",dpi=200)

### plot data 3c
j += 1
# define cut
cut_Tco21 = (Tco21_tmp_ > Trms_co21[i]*snr)
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_all = np.where((cut_Tco21) & (cut_co10) & (cut_co21))

# cut data
w3 = w3_tmp_[cut_all]
Tco21 = Tco21_tmp_[cut_all]
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = w3/Tco21
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "k) log $R_{21}$ vs log W3/$T_{CO(2-1)}$"
xlabel = "log W3/$T_{CO(2-1)}$"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,False,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot3c.png",dpi=200)

### plot data 3d
j += 1
# define cut
cut_co10 = (Ico10_tmp_ > Trms_co10[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_co21 = (Ico21_tmp_ > Trms_co21[i] * snr * np.sqrt(nchan_tmp_) * np.sqrt(velres[i]))
cut_sigma = (Sco21_tmp_ > 5)
cut_all = np.where((cut_Tco21) & (cut_co10) & (cut_co21) & (cut_sigma))

# cut data
w3 = w3_tmp_[cut_all]
Sco21 = Sco21_tmp_[cut_all]
Ico21 = Ico21_tmp_[cut_all] * co21_jy2k
Ico10 = Ico10_tmp_[cut_all] * co10_jy2k
r21 = Ico21/Ico10

# make x and y
x_tmp_ = w3/Sco21
y_tmp_ = r21
y_tmp_[np.where(np.isnan(y_tmp_) & np.isinf(y_tmp_))] = 0
x = np.log10(x_tmp_[y_tmp_>0])
y = np.log10(y_tmp_[y_tmp_>0])

# plot
title = "l) log $R_{21}$ vs log W3/$\sigma_{CO(2-1)}$"
xlabel = "log W3/$\sigma_{CO(2-1)}$"
xlim = [x.min()-0.2,x.max()+0.2]

figure = plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 20
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:17,0:17])
ax2 = plt.subplot(gs[17:20,0:17])
setup_ax1(ax1,x,y,xlim,ylim,False,title,j)
setup_ax2(ax2,x,60,xlim,xlabel,j)
plt.subplots_adjust(bottom=0.15, wspace=0.05)
plt.savefig(dir_data+"eps/"+gals[i]+"_mplot3d.png",dpi=200)
