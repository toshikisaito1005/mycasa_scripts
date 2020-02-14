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


###
def distance(x, y, pa, inc, ra_cnt, dec_cnt):
    tilt_cos = math.cos(math.radians(pa))
    tilt_sin = math.sin(math.radians(pa))

    x_tmp = x - ra_cnt
    y_tmp = y - dec_cnt

    x_new = (x_tmp*tilt_cos - y_tmp*tilt_sin)
    y_new = (x_tmp*tilt_sin + y_tmp*tilt_cos) * 1/math.sin(math.radians(inc))
    
    r = np.sqrt(x_new**2 + y_new**2)

    return r

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

###
bins=40
step=0.03
xlim = [0.01,1.2]

ra_cnt = 185.729
dec_cnt = 15.8223
pa = 180-157.8
inc = 35.1


###
gal="ngc0628" # "ngc4321"
dir_data="/Users/saito/data/phangs/co_ratio/"+gal+"_co/"
txtdata=dir_data+gal+"_flux_4p0_4p0_no.txt"
data=np.loadtxt(txtdata)

y=data[:,3]/data[:,2]/4.
for i in range(len(y)):
    if data[:,2][i]==0:
        y[i]=-1

x=[]
histo_num=[]
histo_co10=[]
histo_co21=[]
histo_dist=[]
for i in range(bins):
    x.append(i*step)
    
    data_select = data[np.where((y >= i*step) & (y < (i+1)*step))]
    if len(data_select)>1:
        histo_num.append(len(data_select))
        histo_co10.append(np.sum(data_select[:,2]))
        histo_co21.append(np.sum(data_select[:,3]))
        r=distance(data_select[:,0],
                   data_select[:,1],
                   pa, inc, ra_cnt, dec_cnt)
        histo_dist.append(np.median(r))
    else:
        histo_num.append(0)
        histo_co10.append(0)
        histo_co21.append(0)
        histo_dist.append(0)


### plot
plt.figure(figsize=(9,9))
plt.rcParams["font.size"] = 18

gs = gridspec.GridSpec(nrows=4, ncols=3)
plt1 = plt.subplot(gs[0,0:3])
plt2 = plt.subplot(gs[1,0:3])
plt3 = plt.subplot(gs[2,0:3])

#
plt1.plot(x,histo_num,color="grey",drawstyle="steps-post",lw=4)
popt1,residual = fit_func1(func1, x, histo_num, [300,0.4,0.1])
plt1.plot(x,func1(x,popt1[0],popt1[1],popt1[2]),"k",lw=2)

plt1.plot([popt1[1],popt1[1]],[0,popt1[0]*1.5],"k",lw=2)
plt1.plot([np.percentile(y[y>0],3),np.percentile(y[y>0],3)],
          [0,popt1[0]*1.5],"grey",lw=1,ls="dashed")
plt1.plot([np.percentile(y[y>0],10),np.percentile(y[y>0],10)],
          [0,popt1[0]*1.5],"grey",lw=1.5,ls="dashed")
plt1.plot([np.percentile(y[y>0],25),np.percentile(y[y>0],25)],
          [0,popt1[0]*1.5],"grey",lw=2,ls="dashed")
plt1.plot([np.percentile(y[y>0],50),np.percentile(y[y>0],50)],
          [0,popt1[0]*1.5],"grey",lw=2.5,ls="dashed")
plt1.plot([np.percentile(y[y>0],75),np.percentile(y[y>0],75)],
          [0,popt1[0]*1.5],"grey",lw=3,ls="dashed")
plt1.plot([np.percentile(y[y>0],90),np.percentile(y[y>0],90)],
          [0,popt1[0]*1.5],"grey",lw=3.5,ls="dashed")
plt1.plot([np.percentile(y[y>0],97),np.percentile(y[y>0],97)],
          [0,popt1[0]*1.5],"grey",lw=4,ls="dashed")

#
plt2.plot(x,histo_co10,color="blue",drawstyle="steps-post",lw=4)
popt2,residual = fit_func1(func1, x, histo_co10, [300,0.4,0.1])
plt2.plot(x,func1(x,popt2[0],popt2[1],popt2[2]),"k",lw=2)

plt2.plot([popt2[1],popt2[1]],[0,popt2[0]*1.5],"k",lw=1)
i = hist_percent(histo_co10,0.03)
plt2.plot([x[i],x[i]],[0,popt2[0]*1.5],"blue",lw=1.5,ls="dashed")
i = hist_percent(histo_co10,0.10)
plt2.plot([x[i],x[i]],[0,popt2[0]*1.5],"blue",lw=2,ls="dashed")
i = hist_percent(histo_co10,0.25)
plt2.plot([x[i],x[i]],[0,popt2[0]*1.5],"blue",lw=2.5,ls="dashed")
i = hist_percent(histo_co10,0.50)
plt2.plot([x[i],x[i]],[0,popt2[0]*1.5],"blue",lw=3,ls="dashed")
i = hist_percent(histo_co10,0.75)
plt2.plot([x[i],x[i]],[0,popt2[0]*1.5],"blue",lw=3.5,ls="dashed")
i = hist_percent(histo_co10,0.90)
plt2.plot([x[i],x[i]],[0,popt2[0]*1.5],"blue",lw=4,ls="dashed")
i = hist_percent(histo_co10,0.97)
plt2.plot([x[i],x[i]],[0,popt2[0]*1.5],"blue",lw=4.5,ls="dashed")

#
plt3.plot(x,histo_co21,color="green",drawstyle="steps-post",lw=4)
popt3,residual = fit_func1(func1, x, histo_co21, [300,0.4,0.1])
plt3.plot(x,func1(x,popt3[0],popt3[1],popt3[2]),"k",lw=2)

plt3.plot([popt3[1],popt3[1]],[0,popt3[0]*1.5],"k",lw=2)
i = hist_percent(histo_co21,0.03)
plt3.plot([x[i],x[i]],[0,popt3[0]*1.5],"green",lw=1,ls="dashed")
i = hist_percent(histo_co21,0.10)
plt3.plot([x[i],x[i]],[0,popt3[0]*1.5],"green",lw=1.5,ls="dashed")
i = hist_percent(histo_co21,0.25)
plt3.plot([x[i],x[i]],[0,popt3[0]*1.5],"green",lw=2,ls="dashed")
i = hist_percent(histo_co21,0.50)
plt3.plot([x[i],x[i]],[0,popt3[0]*1.5],"green",lw=2.5,ls="dashed")
i = hist_percent(histo_co21,0.75)
plt3.plot([x[i],x[i]],[0,popt3[0]*1.5],"green",lw=3,ls="dashed")
i = hist_percent(histo_co21,0.90)
plt3.plot([x[i],x[i]],[0,popt3[0]*1.5],"green",lw=3.5,ls="dashed")
i = hist_percent(histo_co21,0.97)
plt3.plot([x[i],x[i]],[0,popt3[0]*1.5],"green",lw=4,ls="dashed")


plt1.set_xlim(xlim)
plt2.set_xlim(xlim)
plt3.set_xlim(xlim)
plt1.set_ylim([0,popt1[0]*1.5])
plt2.set_ylim([0,popt2[0]*1.5])
plt3.set_ylim([0,popt3[0]*1.5])
plt.xlabel("$R_{21}$")
plt1.set_ylabel("# of Sightlines")
plt2.set_ylabel("CO(1-0) Flux")
plt3.set_ylabel("CO(2-1) Flux")
plt1.legend()
plt2.legend()
plt3.legend()
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/f2_hists_co.png",dpi=100)

