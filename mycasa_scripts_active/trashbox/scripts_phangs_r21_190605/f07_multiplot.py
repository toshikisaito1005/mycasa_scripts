import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
import scipy.stats as stats
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

gal = "ngc0628"
scale = 44/1.0/1000. #kpc/arcsec 0628
ra_cnt = 24.174
dec_cnt = 15.783
pa = 180-21.1
inc = 8.7
txtfile="../../phangs/co_ratio/"+gal+"/"+gal+"_flux_14p0_14p0_no.txt"
"""
gal = "ngc4321"
scale = 103/1.4/1000. #kpc/arcsec 4321
ra_cnt = 185.729
dec_cnt = 15.8223
pa = 180-157.8
inc = 90-35.1
txtfile="../../phangs/co_ratio/"+gal+"_wise/"+gal+"_flux_8p0_8p0_no.txt"
"""

dir_eps="/Users/saito/data/phangs/co_ratio/eps/"
beam = 8.0


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

def density_estimation(m1,m2,xlim,ylim):
    X, Y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)
    return X, Y, Z

def scatbins(x,y,nbins,range):
    n, _ = np.histogram(x,bins=nbins,range=range)
    sy, _ = np.histogram(x,bins=nbins,weights=y,range=range)
    sy2, _ = np.histogram(x,bins=nbins,weights=y*y,range=range)
    mean = sy / n
    std = np.sqrt(sy2/n - mean*mean)

    return _, mean, std

def func(x, a, b):
    f = a * x + b
    return f

#####################
### Main Procedure
#####################

##################### data 1
data = np.loadtxt(txtfile)
y=data[:,3]/data[:,2]/4.
for i in range(len(y)):
    if data[:,2][i]==0:
        y[i]=-1

r=distance(data[:,0],data[:,1],pa,inc,ra_cnt,dec_cnt,scale)
mask = data[:,12][y>0]

factor = 1.222 * 10**6 / beam**2 / 230.53800**2
data[:,3] = data[:,3] * factor
data[:,5] = data[:,5] * factor

### plot
# setup
plt.figure(figsize=(10,3))
plt.rcParams["font.size"] = 10
gs = gridspec.GridSpec(nrows=12, ncols=17)
scat1 = plt.subplot(gs[0:9,0:4])
scat2 = plt.subplot(gs[0:9,4:8])
scat3 = plt.subplot(gs[0:9,8:12])
scat4 = plt.subplot(gs[0:9,12:16])
hist1 = plt.subplot(gs[9:11,0:4])
hist2 = plt.subplot(gs[9:11,4:8])
hist3 = plt.subplot(gs[9:11,8:12])
hist4 = plt.subplot(gs[9:11,12:16])
#hist5b = plt.subplot(gs[0:9,16])

# scat1
cx_tmp = r[y>0]
cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat1.set_xticks([])
#scat1.set_yticks([])
scat1.set_xlim([-0.6,1.4])
scat1.set_ylim([-1.0,0.8])
scat1.set_ylabel("log $R_{21}$")
scat1.text(-0.6+(1.4+0.6)*0.05,0.8-(0.8+1.0)*0.12,"a) Radial $R_{21}$")
scat1.scatter(np.log10(r[y>0]),np.log10(y[y>0]),lw=0,alpha=0.4,c="grey")

#scat1.scatter(np.log10(cx),np.log10(cy),lw=0,alpha=0.4,c="red")
X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),[-0.6,1.4],[-1.0,0.8])
scat1.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx),np.log10(dy),[-0.6,1.4],[-1.0,0.8])
scat1.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(r[y>0]),np.log10(y[y>0]),7,
                        [np.log10(r[y>0]).min(),np.log10(r[y>0]).max()])
scat1.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(r[y>0]),np.log10(y[y>0]))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx),np.log10(cy))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx),np.log10(dy))[0][1],2))
scat1.text(-0.6+(1.4+0.6)*0.05,0.8-(0.8+1.0)*0.22,coef_all)
scat1.text(-0.6+(1.4+0.6)*0.28,0.8-(0.8+1.0)*0.22,coef_red,color="red")
scat1.text(-0.6+(1.4+0.6)*0.51,0.8-(0.8+1.0)*0.22,coef_blue,color="blue")


sigma_tmp = data[:,3]/data[:,2]/4.\
            * np.sqrt((0.036)**2/data[:,3]**2 + 0.024**2/data[:,2]**2)
sigma = sigma_tmp[y>0]

popt, pcov = curve_fit(func,np.log10(r[y>0]),np.log10(y[y>0]),
                       sigma=sigma)
scat1.plot(np.log10(r[y>0]),
           func(np.log10(r[y>0]),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

os.system("rm -rf "+txtfile.replace(".txt","_linearfit.txt"))
f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("1 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# scat2
cx_tmp = data[:,3][y>0]
cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat2.set_xticks([])
scat2.set_yticks([])
scat2.set_xlim([-1.6,2.6])
scat2.set_ylim([-1.0,0.8])
scat2.text(-1.6+(2.6+1.6)*0.05,0.8-(0.8+1.0)*0.12,"b) $R_{21}$ vs. $I_{CO(2-1)}$")
scat2.scatter(np.log10(data[:,3][y>0]),np.log10(y[y>0]),lw=0,alpha=0.4,c="grey")

#scat2.scatter(np.log10(cx),np.log10(cy),lw=0,alpha=0.4,c="red")
X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),[-1.6,2.6],[-1.0,0.8])
scat2.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx),np.log10(dy),[-1.6,2.6],[-1.0,0.8])
scat2.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp),np.log10(cy_tmp),7,
                        [np.log10(cx_tmp).min(),
                         np.log10(cx_tmp).max()])
scat2.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(data[:,3][y>0]),np.log10(y[y>0]))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx),np.log10(cy))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx),np.log10(dy))[0][1],2))
scat2.text(-1.6+(2.6+1.6)*0.05,0.8-(0.8+1.0)*0.22,coef_all)
scat2.text(-1.6+(2.6+1.6)*0.28,0.8-(0.8+1.0)*0.22,coef_red,color="red")
scat2.text(-1.6+(2.6+1.6)*0.51,0.8-(0.8+1.0)*0.22,coef_blue,color="blue")

popt, pcov = curve_fit(func,np.log10(data[:,3][y>0]),np.log10(y[y>0]),
                       sigma=sigma)
scat2.plot(np.log10(data[:,3][y>0]),
           func(np.log10(data[:,3][y>0]),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("2 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# scat3
xlim = [-0.6,1.4]
cx_tmp = data[:,5][y>0]
cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat3.set_xticks([])
scat3.set_yticks([])
scat3.set_xlim(xlim)
scat3.set_ylim([-1.0,0.8])
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.05,0.8-(0.8+1.0)*0.12,"c) $R_{21}$ vs. $T_{CO(2-1)}$")
scat3.scatter(np.log10(cx_tmp),np.log10(cy_tmp),lw=0,alpha=0.4,c="grey")

#scat3.scatter(np.log10(cx),np.log10(cy),lw=0,alpha=0.4,c="red")
X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),xlim,[-1.0,0.8])
scat3.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx),np.log10(dy),xlim,[-1.0,0.8])
scat3.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp[cx_tmp>0.3]),
                        np.log10(cy_tmp[cx_tmp>0.3]),7,
                        [np.log10(cx_tmp[cx_tmp>0.3]).min(),
                         np.log10(cx_tmp[cx_tmp>0.3]).max()])
scat3.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(cx_tmp),np.log10(cy_tmp))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx),np.log10(cy))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx),np.log10(dy))[0][1],2))
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.05,0.8-(0.8+1.0)*0.22,coef_all)
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.28,0.8-(0.8+1.0)*0.22,coef_red,color="red")
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.51,0.8-(0.8+1.0)*0.22,coef_blue,color="blue")

popt, pcov = curve_fit(func,np.log10(cx_tmp),np.log10(cy_tmp),
                       sigma=sigma)
scat3.plot(np.log10(cx_tmp),
           func(np.log10(cx_tmp),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("3 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# scat4
cx_tmp = data[:,7][y>0]
cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat4.set_xticks([])
scat4.set_yticks([])
scat4.set_xlim([-1.9,0.7])
scat4.set_ylim([-1.0,0.8])
scat4.text(-1.9+(0.7+1.9)*0.05,0.8-(0.8+1.0)*0.12,"d) $R_{21}$ vs. $\sigma_{CO(2-1)}$")
scat4.scatter(np.log10(data[:,7][y>0]),np.log10(y[y>0]),lw=0,alpha=0.4,c="grey")

#scat4.scatter(np.log10(cx),np.log10(cy),lw=0,alpha=0.4,c="red")
X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),[-1.9,0.7],[-1.0,0.8])
scat4.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx),np.log10(dy),[-1.9,0.7],[-1.0,0.8])
scat4.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp[cx_tmp>0.0125]),
                        np.log10(cy_tmp[cx_tmp>0.0125]),7,
                        [np.log10(cx_tmp[cx_tmp>0.0125]).min(),
                         np.log10(cx_tmp[cx_tmp>0.0125]).max()])
scat4.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(cx_tmp),np.log10(cy_tmp))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx),np.log10(cy))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx),np.log10(dy))[0][1],2))
scat4.text(-1.9+(0.7+1.9)*0.05,0.8-(0.8+1.0)*0.22,coef_all)
scat4.text(-1.9+(0.7+1.9)*0.28,0.8-(0.8+1.0)*0.22,coef_red,color="red")
scat4.text(-1.9+(0.7+1.9)*0.51,0.8-(0.8+1.0)*0.22,coef_blue,color="blue")

popt, pcov = curve_fit(func,np.log10(cx_tmp),np.log10(cy_tmp),
                       sigma=sigma)
scat4.plot(np.log10(cx_tmp),
           func(np.log10(cx_tmp),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("4 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# hist1
cx_tmp = r[y>0]
cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist1.set_xticks([])
hist1.set_yticks([])
hist=hist1.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=[-0.6,1.4])
hist1.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist1.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist1.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist1.plot([np.percentile(np.log10(dx),25),np.percentile(np.log10(dx),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist1.plot([np.percentile(np.log10(dx),50),np.percentile(np.log10(dx),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist1.plot([np.percentile(np.log10(dx),75),np.percentile(np.log10(dx),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist1.set_xlim([-0.6,1.4])
hist1.set_ylim([hist[0].max()*1.2,0])
hist1.set_xlabel("log Radius (kpc)")

# hist2
cx_tmp = data[:,3][y>0]
cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist2.set_xticks([])
hist2.set_yticks([])
hist=hist2.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=[-1.6,2.6])
hist2.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist2.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist2.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist2.plot([np.percentile(np.log10(dx),25),np.percentile(np.log10(dx),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist2.plot([np.percentile(np.log10(dx),50),np.percentile(np.log10(dx),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist2.plot([np.percentile(np.log10(dx),75),np.percentile(np.log10(dx),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist2.set_xlim([-1.6,2.6])
hist2.set_ylim([hist[0].max()*1.2,0])
hist2.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")

# hist3
cx_tmp = data[:,5][y>0]
cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist3.set_xticks([])
hist3.set_yticks([])
hist=hist3.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=[-0.1,1.4])
hist3.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist3.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist3.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist3.plot([np.percentile(np.log10(dx),25),np.percentile(np.log10(dx),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist3.plot([np.percentile(np.log10(dx),50),np.percentile(np.log10(dx),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist3.plot([np.percentile(np.log10(dx),75),np.percentile(np.log10(dx),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist3.set_xlim([-0.6,1.4])
hist3.set_ylim([hist[0].max()*1.2,0])
hist3.set_xlabel("log $T_{CO(2-1)}$ (K)")

# hist4
cx_tmp = data[:,7][y>0]
cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist4.set_xticks([])
hist4.set_yticks([])
hist=hist4.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=[-1.9,0.7])
hist4.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist4.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist4.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist4.plot([np.percentile(np.log10(dx),25),np.percentile(np.log10(dx),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist4.plot([np.percentile(np.log10(dx),50),np.percentile(np.log10(dx),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist4.plot([np.percentile(np.log10(dx),75),np.percentile(np.log10(dx),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist4.set_xlim([-1.9,0.7])
hist4.set_ylim([hist[0].max()*1.2,0])
hist4.set_xlabel("log $\sigma_{CO(2-1)}$ (km s$^{-1}$)")
"""
# hist5
cx_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

hist5b.set_xticks([])
hist5b.set_yticks([])
hist5 = hist5b.twinx()
hist5.set_xticks([])
hist=hist5.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=[-1.0,0.8],
                orientation="horizontal")
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           c="red",lw=1,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           c="red",lw=1.5,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           c="red",lw=2,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(dx),25),np.percentile(np.log10(dx),25)],
           c="blue",lw=1,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(dx),50),np.percentile(np.log10(dx),50)],
           c="blue",lw=1.5,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(dx),75),np.percentile(np.log10(dx),75)],
           c="blue",lw=2,alpha=0.7)
hist5.set_ylim([-1.0,0.8])
hist5.set_xlim([0,hist[0].max()*1.2])
hist5.set_ylabel("log $R_{21}$")
"""
plt.savefig(dir_eps+"figure7_multiplot1.png",dpi=200)


##################### data 2
data = np.loadtxt(txtfile)
y=data[:,3]/data[:,2]/4.
for i in range(len(y)):
    if data[:,2][i]==0:
        y[i]=-1

mask = data[:,12][y>0]

### plot
# setup
plt.figure(figsize=(10,3))
plt.rcParams["font.size"] = 10
gs = gridspec.GridSpec(nrows=12, ncols=17)
scat1 = plt.subplot(gs[0:9,0:4])
scat2 = plt.subplot(gs[0:9,4:8])
scat3 = plt.subplot(gs[0:9,8:12])
scat4 = plt.subplot(gs[0:9,12:16])
hist1 = plt.subplot(gs[9:11,0:4])
hist2 = plt.subplot(gs[9:11,4:8])
hist3 = plt.subplot(gs[9:11,8:12])
hist4 = plt.subplot(gs[9:11,12:16])
#hist5b = plt.subplot(gs[0:9,16])

# scat1
xlim = [-3.9,-1.4]
ylim = [-1,0.8]

cx_tmp = data[:,8][y>0]
cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat1.set_xticks([])
#scat1.set_yticks([])
scat1.set_xlim(xlim)
scat1.set_ylim(ylim)
scat1.set_ylabel("log $R_{21}$")
scat1.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.12,
           "e) $R_{21}$ vs. W1")
scat1.scatter(np.log10(cx_tmp),np.log10(cy_tmp),lw=0,alpha=0.4,c="grey")

X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),xlim,ylim)
scat1.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx[dx>0]),np.log10(dy[dx>0]),xlim,ylim)
scat1.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp[cx_tmp>0]),
                        np.log10(cy_tmp[cx_tmp>0]),
                        10,xlim)
scat1.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(cx_tmp[cx_tmp>0]),
                                    np.log10(cy_tmp[cx_tmp>0]))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx[cx>0]),
                                    np.log10(cy[cx>0]))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx[dx>0]),
                                     np.log10(dy[dx>0]))[0][1],2))
scat1.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_all)
scat1.text(xlim[0]+(xlim[1]-xlim[0])*0.28,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_red,color="red")
scat1.text(xlim[0]+(xlim[1]-xlim[0])*0.51,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_blue,color="blue")

sigma_tmp = data[:,3][y>0]/data[:,2][y>0]/4.\
    * np.sqrt((0.036)**2/data[:,3][y>0]**2 + 0.024**2/data[:,2][y>0]**2)
sigma = sigma_tmp[cx_tmp>0]
popt, pcov = curve_fit(func,np.log10(cx_tmp[cx_tmp>0]),
                       np.log10(cy_tmp[cx_tmp>0]),
                       sigma=sigma)
scat1.plot(np.log10(cx_tmp[cx_tmp>0]),
           func(np.log10(cx_tmp[cx_tmp>0]),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("5 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# scat2
xlim = [-3.9,-1.4]
ylim = [-1,0.8]

cx_tmp = data[:,9][y>0]
cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat2.set_xticks([])
scat2.set_yticks([])
scat2.set_xlim(xlim)
scat2.set_ylim(ylim)
scat2.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.12,
           "f) $R_{21}$ vs. W2")
scat2.scatter(np.log10(cx_tmp),np.log10(cy_tmp),lw=0,alpha=0.4,c="grey")

X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),xlim,ylim)
scat2.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx[dx>0]),np.log10(dy[dx>0]),xlim,ylim)
scat2.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp[cx_tmp>0]),
                        np.log10(cy_tmp[cx_tmp>0]),
                        10,xlim)
scat2.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(cx_tmp[cx_tmp>0]),
                                    np.log10(cy_tmp[cx_tmp>0]))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx[cx>0]),
                                    np.log10(cy[cx>0]))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx[dx>0]),
                                     np.log10(dy[dx>0]))[0][1],2))
scat2.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_all)
scat2.text(xlim[0]+(xlim[1]-xlim[0])*0.28,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_red,color="red")
scat2.text(xlim[0]+(xlim[1]-xlim[0])*0.51,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_blue,color="blue")

sigma = sigma_tmp[cx_tmp>0]
popt, pcov = curve_fit(func,np.log10(cx_tmp[cx_tmp>0]),
                       np.log10(cy_tmp[cx_tmp>0]),
                       sigma=sigma)
scat2.plot(np.log10(cx_tmp[cx_tmp>0]),
           func(np.log10(cx_tmp[cx_tmp>0]),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("6 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# scat3
xlim = [-3.2,-0.7]
ylim = [-1,0.8]

cx_tmp = data[:,10][y>0]
cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat3.set_xticks([])
scat3.set_yticks([])
scat3.set_xlim(xlim)
scat3.set_ylim(ylim)
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.12,
           "g) $R_{21}$ vs. W3")
scat3.scatter(np.log10(cx_tmp),np.log10(cy_tmp),lw=0,alpha=0.4,c="grey")

X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),xlim,ylim)
scat3.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx[dx>0]),np.log10(dy[dx>0]),xlim,ylim)
scat3.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp[cx_tmp>0]),
                        np.log10(cy_tmp[cx_tmp>0]),
                        10,xlim)
scat3.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(cx_tmp[cx_tmp>0]),
                                    np.log10(cy_tmp[cx_tmp>0]))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx[cx>0]),
                                    np.log10(cy[cx>0]))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx[dx>0]),
                                     np.log10(dy[dx>0]))[0][1],2))
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_all)
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.28,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_red,color="red")
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.51,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_blue,color="blue")

sigma = sigma_tmp[cx_tmp>0]
popt, pcov = curve_fit(func,np.log10(cx_tmp[cx_tmp>0]),np.log10(cy_tmp[cx_tmp>0]))
scat3.plot(np.log10(cx_tmp[cx_tmp>0]),
           func(np.log10(cx_tmp[cx_tmp>0]),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("7 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# scat4
xlim = [-0.1,1.0]
ylim = [-1,0.8]

cx_tmp = data[:,10][y>0] / data[:,8][y>0]
for i in range(len(cx_tmp)):
    if data[:,8][y>0][i]==0:
        cx_tmp[i]=0

cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat4.set_xticks([])
scat4.set_yticks([])
scat4.set_xlim(xlim)
scat4.set_ylim(ylim)
scat4.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.12,
           "h) $R_{21}$ vs. W3/W1")
scat4.scatter(np.log10(cx_tmp),np.log10(cy_tmp),lw=0,alpha=0.4,c="grey")

X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),xlim,ylim)
scat4.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx[dx>0]),np.log10(dy[dx>0]),xlim,ylim)
scat4.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp[cx_tmp>1.1]),
                        np.log10(cy_tmp[cx_tmp>1.1]),
                        9,xlim)
scat4.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(cx_tmp[cx_tmp>0]),
                                    np.log10(cy_tmp[cx_tmp>0]))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx[cx>0]),
                                    np.log10(cy[cx>0]))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx[dx>0]),
                                     np.log10(dy[dx>0]))[0][1],2))
scat4.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_all)
scat4.text(xlim[0]+(xlim[1]-xlim[0])*0.28,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_red,color="red")
scat4.text(xlim[0]+(xlim[1]-xlim[0])*0.51,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_blue,color="blue")

sigma = sigma_tmp[cx_tmp>0]
popt, pcov = curve_fit(func,np.log10(cx_tmp[cx_tmp>0]),np.log10(cy_tmp[cx_tmp>0]))
scat4.plot(np.log10(cx_tmp[cx_tmp>0]),
           func(np.log10(cx_tmp[cx_tmp>0]),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("8 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# hist1
xlim = [-3.9,-1.4]

cx_tmp = data[:,8][y>0]
cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist1.set_xticks([])
hist1.set_yticks([])
hist=hist1.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=xlim)
hist1.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist1.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist1.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist1.plot([np.percentile(np.log10(dx[dx>0]),25),np.percentile(np.log10(dx[dx>0]),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist1.plot([np.percentile(np.log10(dx[dx>0]),50),np.percentile(np.log10(dx[dx>0]),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist1.plot([np.percentile(np.log10(dx[dx>0]),75),np.percentile(np.log10(dx[dx>0]),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist1.set_xlim(xlim)
hist1.set_ylim([hist[0].max()*1.2,0])
hist1.set_xlabel("log W1 (Jy beam$^{-1}$)")

# hist2
xlim = [-3.9,-1.4]

cx_tmp = data[:,9][y>0]
cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist2.set_xticks([])
hist2.set_yticks([])
hist=hist2.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=xlim)
hist2.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist2.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist2.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist2.plot([np.percentile(np.log10(dx[dx>0]),25),np.percentile(np.log10(dx[dx>0]),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist2.plot([np.percentile(np.log10(dx[dx>0]),50),np.percentile(np.log10(dx[dx>0]),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist2.plot([np.percentile(np.log10(dx[dx>0]),75),np.percentile(np.log10(dx[dx>0]),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist2.set_xlim(xlim)
hist2.set_ylim([hist[0].max()*1.2,0])
hist2.set_xlabel("log W2 (Jy beam$^{-1}$)")

# hist3
xlim = [-3.2,-0.7]

cx_tmp = data[:,10][y>0]
cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist3.set_xticks([])
hist3.set_yticks([])
hist=hist3.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=xlim)
hist3.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist3.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist3.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist3.plot([np.percentile(np.log10(dx[dx>0]),25),np.percentile(np.log10(dx[dx>0]),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist3.plot([np.percentile(np.log10(dx[dx>0]),50),np.percentile(np.log10(dx[dx>0]),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist3.plot([np.percentile(np.log10(dx[dx>0]),75),np.percentile(np.log10(dx[dx>0]),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist3.set_xlim(xlim)
hist3.set_ylim([hist[0].max()*1.2,0])
hist3.set_xlabel("log W3 (Jy beam$^{-1}$)")

# hist4
xlim = [-0.1,1.0]

cx_tmp = data[:,10][y>0] / data[:,8][y>0]
for i in range(len(cx_tmp)):
    if data[:,8][y>0][i]==0:
        cx_tmp[i]=0

cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist4.set_xticks([])
hist4.set_yticks([])
hist=hist4.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=xlim)
hist4.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist4.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist4.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist4.plot([np.percentile(np.log10(dx[dx>0]),25),np.percentile(np.log10(dx[dx>0]),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist4.plot([np.percentile(np.log10(dx[dx>0]),50),np.percentile(np.log10(dx[dx>0]),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist4.plot([np.percentile(np.log10(dx[dx>0]),75),np.percentile(np.log10(dx[dx>0]),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist4.set_xlim(xlim)
hist4.set_ylim([hist[0].max()*1.2,0])
hist4.set_xlabel("log W3/W1")
"""
# hist5
cx_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

hist5b.set_xticks([])
hist5b.set_yticks([])
hist5 = hist5b.twinx()
hist5.set_xticks([])
hist=hist5.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=[-1.0,0.8],
                orientation="horizontal")
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           c="red",lw=1,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           c="red",lw=1.5,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           c="red",lw=2,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(dx),25),np.percentile(np.log10(dx),25)],
           c="blue",lw=1,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(dx),50),np.percentile(np.log10(dx),50)],
           c="blue",lw=1.5,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(dx),75),np.percentile(np.log10(dx),75)],
           c="blue",lw=2,alpha=0.7)
hist5.set_ylim([-1.0,0.8])
hist5.set_xlim([0,hist[0].max()*1.2])
hist5.set_ylabel("log $R_{21}$")
"""
plt.savefig(dir_eps+"figure7_multiplot2.png",dpi=200)



##################### data 3
data = np.loadtxt(txtfile)
y=data[:,3]/data[:,2]/4.
for i in range(len(y)):
    if data[:,2][i]==0:
        y[i]=-1

mask = data[:,12][y>0]

### plot
# setup
plt.figure(figsize=(10,3))
plt.rcParams["font.size"] = 10
gs = gridspec.GridSpec(nrows=12, ncols=17)
scat1 = plt.subplot(gs[0:9,0:4])
scat2 = plt.subplot(gs[0:9,4:8])
scat3 = plt.subplot(gs[0:9,8:12])
scat4 = plt.subplot(gs[0:9,12:16])
hist1 = plt.subplot(gs[9:11,0:4])
hist2 = plt.subplot(gs[9:11,4:8])
hist3 = plt.subplot(gs[9:11,8:12])
hist4 = plt.subplot(gs[9:11,12:16])
#hist5b = plt.subplot(gs[0:9,16])

# scat1
xlim = [-3.6,-1.6]
ylim = [-1,0.8]

cx_tmp = data[:,8][y>0] / data[:,7][y>0]
for i in range(len(cx_tmp)):
    if data[:,7][y>0][i]==0:
        cx_tmp[i]=0

cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat1.set_xticks([])
#scat1.set_yticks([])
scat1.set_xlim(xlim)
scat1.set_ylim(ylim)
scat1.set_ylabel("log $R_{21}$")
scat1.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.12,
           "i) $R_{21}$ vs. W1/$T_{CO(2-1)}$")
scat1.scatter(np.log10(cx_tmp),np.log10(cy_tmp),lw=0,alpha=0.4,c="grey")

X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),xlim,ylim)
scat1.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx[dx>0]),np.log10(dy[dx>0]),xlim,ylim)
scat1.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp),
                        np.log10(cy_tmp),
                        10,xlim)
scat1.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(cx_tmp[cx_tmp>0]),
                                    np.log10(cy_tmp[cx_tmp>0]))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx[cx>0]),
                                    np.log10(cy[cx>0]))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx[dx>0]),
                                     np.log10(dy[dx>0]))[0][1],2))
scat1.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_all)
scat1.text(xlim[0]+(xlim[1]-xlim[0])*0.28,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_red,color="red")
scat1.text(xlim[0]+(xlim[1]-xlim[0])*0.51,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_blue,color="blue")

sigma = sigma_tmp[cx_tmp>0]
popt, pcov = curve_fit(func,np.log10(cx_tmp[cx_tmp>0]),
                       np.log10(cy_tmp[cx_tmp>0]),
                       sigma=sigma)
scat1.plot(np.log10(cx_tmp[cx_tmp>0]),
           func(np.log10(cx_tmp[cx_tmp>0]),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("9 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# scat2
xlim = [-3.7,-1.7]
ylim = [-1,0.8]

cx_tmp = data[:,9][y>0] / data[:,7][y>0]
for i in range(len(cx_tmp)):
    if data[:,7][y>0][i]==0:
        cx_tmp[i]=0

cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat2.set_xticks([])
scat2.set_yticks([])
scat2.set_xlim(xlim)
scat2.set_ylim(ylim)
scat2.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.12,
           "j) $R_{21}$ vs. W2/$T_{CO(2-1)}$")
scat2.scatter(np.log10(cx_tmp),np.log10(cy_tmp),lw=0,alpha=0.4,c="grey")

X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),xlim,ylim)
scat2.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx[dx>0]),np.log10(dy[dx>0]),xlim,ylim)
scat2.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp)[np.log10(cx_tmp)<-1.5],
                        np.log10(cy_tmp)[np.log10(cx_tmp)<-1.5],
                        8,xlim)
scat2.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(cx_tmp[cx_tmp>0]),
                                    np.log10(cy_tmp[cx_tmp>0]))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx[cx>0]),
                                    np.log10(cy[cx>0]))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx[dx>0]),
                                     np.log10(dy[dx>0]))[0][1],2))
scat2.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_all)
scat2.text(xlim[0]+(xlim[1]-xlim[0])*0.28,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_red,color="red")
scat2.text(xlim[0]+(xlim[1]-xlim[0])*0.51,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_blue,color="blue")

sigma = sigma_tmp[cx_tmp>0]
popt, pcov = curve_fit(func,np.log10(cx_tmp[cx_tmp>0]),
                       np.log10(cy_tmp[cx_tmp>0]),
                       sigma=sigma)
scat2.plot(np.log10(cx_tmp[cx_tmp>0]),
           func(np.log10(cx_tmp[cx_tmp>0]),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("10 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# scat3
xlim = [-2.75,-1.3]
ylim = [-1,0.8]

cx_tmp = data[:,10][y>0] / data[:,7][y>0]
for i in range(len(cx_tmp)):
    if data[:,7][y>0][i]==0:
        cx_tmp[i]=0

cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat3.set_xticks([])
scat3.set_yticks([])
scat3.set_xlim(xlim)
scat3.set_ylim(ylim)
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.12,
           "k) $R_{21}$ vs. W3/$T_{CO(2-1)}$")
scat3.scatter(np.log10(cx_tmp),np.log10(cy_tmp),lw=0,alpha=0.4,c="grey")

X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),xlim,ylim)
scat3.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx[dx>0]),np.log10(dy[dx>0]),xlim,ylim)
scat3.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp)[np.log10(cx_tmp)<-1.0],
                        np.log10(cy_tmp)[np.log10(cx_tmp)<-1.0],
                        9,xlim)
scat3.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(cx_tmp[cx_tmp>0]),
                                    np.log10(cy_tmp[cx_tmp>0]))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx[cx>0]),
                                    np.log10(cy[cx>0]))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx[dx>0]),
                                     np.log10(dy[dx>0]))[0][1],2))
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_all)
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.28,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_red,color="red")
scat3.text(xlim[0]+(xlim[1]-xlim[0])*0.51,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_blue,color="blue")

sigma = sigma_tmp[cx_tmp>0]
popt, pcov = curve_fit(func,np.log10(cx_tmp[cx_tmp>0]),
                       np.log10(cy_tmp[cx_tmp>0]),
                       sigma=sigma)
scat3.plot(np.log10(cx_tmp[cx_tmp>0]),
           func(np.log10(cx_tmp[cx_tmp>0]),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("11 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# scat4
xlim = [-4.4,-2.5]
ylim = [-1,0.8]

cx_tmp = data[:,10][y>0] / data[:,5][y>0]
for i in range(len(cx_tmp)):
    if data[:,7][y>0][i]==0:
        cx_tmp[i]=0

cy_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
cy = cy_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]
dy = cy_tmp[mask<0.5]

scat4.set_xticks([])
scat4.set_yticks([])
scat4.set_xlim(xlim)
scat4.set_ylim(ylim)
scat4.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.12,
           "l) $R_{21}$ vs. W3/$\sigma$")
scat4.scatter(np.log10(cx_tmp),np.log10(cy_tmp),lw=0,alpha=0.4,c="grey")

X,Y,Z=density_estimation(np.log10(cx),np.log10(cy),xlim,ylim)
scat4.contour(X,Y,Z,colors="red",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)
X,Y,Z=density_estimation(np.log10(dx[dx>0]),np.log10(dy[dx>0]),xlim,ylim)
scat4.contour(X,Y,Z,colors="blue",
              levels=[0.2,1.5,5]*np.max(Z),lw=5,alpha=0.4)

_, mean, std = scatbins(np.log10(cx_tmp),
                        np.log10(cy_tmp),
                        8,xlim)
scat4.errorbar((_[1:]+_[:-1])/2,mean,yerr=std,fmt="k-",lw=2)

coef_all = str(np.round(np.corrcoef(np.log10(cx_tmp[cx_tmp>0]),
                                    np.log10(cy_tmp[cx_tmp>0]))[0][1],2))
coef_red = str(np.round(np.corrcoef(np.log10(cx[cx>0]),
                                    np.log10(cy[cx>0]))[0][1],2))
coef_blue = str(np.round(np.corrcoef(np.log10(dx[dx>0]),
                                     np.log10(dy[dx>0]))[0][1],2))
scat4.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_all)
scat4.text(xlim[0]+(xlim[1]-xlim[0])*0.28,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_red,color="red")
scat4.text(xlim[0]+(xlim[1]-xlim[0])*0.51,ylim[1]-(ylim[1]-ylim[0])*0.22,coef_blue,color="blue")

sigma = sigma_tmp[cx_tmp>0]
popt, pcov = curve_fit(func,np.log10(cx_tmp[cx_tmp>0]),
                       np.log10(cy_tmp[cx_tmp>0]),
                       sigma=sigma)
scat4.plot(np.log10(cx_tmp[cx_tmp>0]),
           func(np.log10(cx_tmp[cx_tmp>0]),popt[0],popt[1]),
           'g-',lw=2,alpha=0.7)

f = open(txtfile.replace(".txt","_linearfit.txt"),"a")
f.write("12 "+str(popt[0])+" "+str(popt[1])+"\n")
f.close()

# hist1
xlim = [-3.6,-1.6]

cx_tmp = data[:,8][y>0] / data[:,7][y>0]
for i in range(len(cx_tmp)):
    if data[:,7][y>0][i]==0:
        cx_tmp[i]=0

cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist1.set_xticks([])
hist1.set_yticks([])
hist=hist1.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=xlim)
hist1.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist1.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist1.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist1.plot([np.percentile(np.log10(dx[dx>0]),25),np.percentile(np.log10(dx[dx>0]),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist1.plot([np.percentile(np.log10(dx[dx>0]),50),np.percentile(np.log10(dx[dx>0]),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist1.plot([np.percentile(np.log10(dx[dx>0]),75),np.percentile(np.log10(dx[dx>0]),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist1.set_xlim(xlim)
hist1.set_ylim([hist[0].max()*1.2,0])
hist1.set_xlabel("log W1/$T_{CO(2-1)}$")

# hist2
xlim = [-3.7,-1.7]
ylim = [-1,0.8]

cx_tmp = data[:,9][y>0] / data[:,7][y>0]
for i in range(len(cx_tmp)):
    if data[:,7][y>0][i]==0:
        cx_tmp[i]=0

cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist2.set_xticks([])
hist2.set_yticks([])
hist=hist2.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=xlim)
hist2.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist2.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist2.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist2.plot([np.percentile(np.log10(dx[dx>0]),25),np.percentile(np.log10(dx[dx>0]),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist2.plot([np.percentile(np.log10(dx[dx>0]),50),np.percentile(np.log10(dx[dx>0]),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist2.plot([np.percentile(np.log10(dx[dx>0]),75),np.percentile(np.log10(dx[dx>0]),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist2.set_xlim(xlim)
hist2.set_ylim([hist[0].max()*1.2,0])
hist2.set_xlabel("log W2/$T_{CO(2-1)}$")

# hist3
xlim = [-2.75,-1.3]
ylim = [-1,0.8]

cx_tmp = data[:,10][y>0] / data[:,7][y>0]
for i in range(len(cx_tmp)):
    if data[:,7][y>0][i]==0:
        cx_tmp[i]=0

cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist3.set_xticks([])
hist3.set_yticks([])
hist=hist3.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=xlim)
hist3.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist3.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist3.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist3.plot([np.percentile(np.log10(dx[dx>0]),25),np.percentile(np.log10(dx[dx>0]),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist3.plot([np.percentile(np.log10(dx[dx>0]),50),np.percentile(np.log10(dx[dx>0]),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist3.plot([np.percentile(np.log10(dx[dx>0]),75),np.percentile(np.log10(dx[dx>0]),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist3.set_xlim(xlim)
hist3.set_ylim([hist[0].max()*1.2,0])
hist3.set_xlabel("log W3/$T_{CO(2-1)}$")

# hist4
xlim = [-4.4,-2.5]

cx_tmp = data[:,10][y>0] / data[:,5][y>0]
for i in range(len(cx_tmp)):
    if data[:,7][y>0][i]==0:
        cx_tmp[i]=0

cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

#hist4.set_xticks([])
hist4.set_yticks([])
hist=hist4.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=xlim)
hist4.plot([np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           [hist[0].max()*1.2,0],c="red",lw=1,alpha=0.7)
hist4.plot([np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           [hist[0].max()*1.2,0],c="red",lw=1.5,alpha=0.7)
hist4.plot([np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           [hist[0].max()*1.2,0],c="red",lw=2,alpha=0.7)
hist4.plot([np.percentile(np.log10(dx[dx>0]),25),np.percentile(np.log10(dx[dx>0]),25)],
           [hist[0].max()*1.2,0],c="blue",lw=1,alpha=0.7)
hist4.plot([np.percentile(np.log10(dx[dx>0]),50),np.percentile(np.log10(dx[dx>0]),50)],
           [hist[0].max()*1.2,0],c="blue",lw=1.5,alpha=0.7)
hist4.plot([np.percentile(np.log10(dx[dx>0]),75),np.percentile(np.log10(dx[dx>0]),75)],
           [hist[0].max()*1.2,0],c="blue",lw=2,alpha=0.7)
hist4.set_xlim(xlim)
hist4.set_ylim([hist[0].max()*1.2,0])
hist4.set_xlabel("log W3/$\sigma$ (Jy beam$^{-1}$) (km s$^{-1}$)$^{-1}$")
"""
# hist5
cx_tmp = y[y>0]
cx = cx_tmp[mask>=0.5]
dx = cx_tmp[mask<0.5]

hist5b.set_xticks([])
hist5b.set_yticks([])
hist5 = hist5b.twinx()
hist5.set_xticks([])
hist=hist5.hist(np.log10(cx_tmp),
                bins=30,color="grey",alpha=0.4,lw=0,range=[-1.0,0.8],
                orientation="horizontal")
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(cx),25),np.percentile(np.log10(cx),25)],
           c="red",lw=1,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(cx),50),np.percentile(np.log10(cx),50)],
           c="red",lw=1.5,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(cx),75),np.percentile(np.log10(cx),75)],
           c="red",lw=2,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(dx),25),np.percentile(np.log10(dx),25)],
           c="blue",lw=1,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(dx),50),np.percentile(np.log10(dx),50)],
           c="blue",lw=1.5,alpha=0.7)
hist5.plot([0,hist[0].max()*1.2],
           [np.percentile(np.log10(dx),75),np.percentile(np.log10(dx),75)],
           c="blue",lw=2,alpha=0.7)
hist5.set_ylim([-1.0,0.8])
hist5.set_xlim([0,hist[0].max()*1.2])
hist5.set_ylabel("log $R_{21}$")
"""
plt.savefig(dir_eps+"figure7_multiplot3.png",dpi=200)
