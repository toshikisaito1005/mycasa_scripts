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



####################################################################################
### Define Main Functions
####################################################################################
def scatter_hists(txtfiles,
                  usecols, # [[2], [3]]
                  keys, # ["Ico10", "Ico21"]
                  limit,
                  limit2,
                  bins,
                  xlabel,
                  ylabel,
                  text,
                  title,
                  xlog,
                  ylog,
                  c,
                  variable,
                  savefig):
    """
    """
    print("###########################")
    print("### running scatter_hists")
    print("###########################")
    plot_a0xy(txtfiles,
              usecols,
              keys,
              limit,
              limit2,
              bins,
              xlabel,
              ylabel,
              text,
              title,
              xlog,
              ylog,
              c,
              variable,
              savefig)

def heatmap_ratio(txt_files,
                  output,
                  outpng,
                  usecols_orig,
                  c,
                  xlog,
                  ylog,
                  scale,
                  xlim, # [1*scale,35*scale]
                  ylim, # [1*scale,35*scale]
                  xlabel, # "Aperture Size (kpc)"
                  ylabel, # "Beam Size (kpc)"
                  text, # "(a) median $R_{21}$, $Me$($R_{21}$)"
                  label, # "$Me$($R_{21}$)"
                  clim, # [0.4,0.65]
                  keys1=["Ico21", "R21"],
                  keys2=["Ico10", "Ico21"]):
    """
    """
    print("###########################")
    print("### running heatmap_ratio")
    print("###########################")
    prepare_heatmap_ratio(txt_files,
                          output,
                          usecols_orig,
                          c,
                          xlog,
                          ylog,
                          keys1,
                          keys2)

    plotter_heatmap_ratio(output,
                          outpng,
                          scale,
                          xlim, # [1*scale,35*scale]
                          ylim, # [1*scale,35*scale]
                          xlabel, # "Aperture Size (kpc)"
                          ylabel, # "Beam Size (kpc)"
                          text, # "(a) median $R_{21}$, $Me$($R_{21}$)"
                          label, # "$Me$($R_{21}$)"
                          clim) # [0.4,0.65]

####################################################################################
### Define functions
####################################################################################
def beam_data(txt_data,variable): # [0] or [0,1]
    """
    """
    ap_size = float(txt_data.split("_")[5].replace("p","."))
    bm_size = float(txt_data.split("_")[4].replace("p","."))

    if variable=="beam":
        return bm_size
    elif variable=="aperture":
        return ap_size

def load_data(txt_data,key,usecols): # [0] or [0,1]
    """
    key = "Ico10", "Ico21", "Tco10", "Tco21", "W1", "W2", "W3"
    key = "R21", "M21", "W1/Ico21", "W2/Ico21", "W3/Ico21"
    """
    ap_size = float(txt_data.split("_")[5].replace("p","."))
    bm_size = float(txt_data.split("_")[4].replace("p","."))

    # x-axis
    if key=="Ico10" or key=="Tco10":
        data = np.loadtxt(txt_data, usecols=usecols)
        factor = 1.222 * 10**6 / bm_size**2 / 115.27120**2
        x = data * factor # co10_m0 or co10_m8

    if key=="Ico21" or key=="Tco21":
        data = np.loadtxt(txt_data, usecols=usecols)
        factor = 1.222 * 10**6 / bm_size**2 / 230.53800**2
        x = data * factor # co21_m0 or co21_m8

    if key=="W1" or key=="W2" or key=="W3":
        data = np.loadtxt(txt_data, usecols=usecols)
        x = data # WISE

    if key=="R21" or key=="M21":
        data = np.loadtxt(txt_data, usecols=usecols)
        factor = 1.222 * 10**6 / bm_size**2 / 115.27120**2
        x1 = data[:,0] * factor # co10_m0
        factor = 1.222 * 10**6 / bm_size**2 / 230.53800**2
        x2 = data[:,1] * factor # co21_m0
        x = x2/x1
        for i in range(len(x)):
            if x1[i] == 0.0:
                x[i] = 0.0

    if key=="W1/Ico21" or key=="W2/Ico21" or key=="W3/Ico21":
        data = np.loadtxt(txt_data, usecols=usecols)
        x1 = data[:,0] # co21_m0 (Jy/beam.km/s)
        x2 = data[:,1] # wise1 or wise2 or wise3 (Jy/beam)
        x = x2/x1
        for i in range(len(x)):
            if x1[i] == 0.0:
                x[i] = 0.0

    if key=="W1/Tco21" or key=="W2/Tco21" or key=="W3/Tco21":
        data = np.loadtxt(txt_data, usecols=usecols)
        x1 = data[:,0] # co21_m8 (Jy/beam)
        x2 = data[:,1] # wise1 or wise2 or wise3 (Jy/beam)
        x = x2/x1
        for i in range(len(x)):
            if x1[i] == 0.0:
                x[i] = 0.0

    return x

def process_data(x_tmp,y_tmp,xlog,ylog):
    """
    """
    x, y = [], []
    for i in range(len(x_tmp)):
        if x_tmp[i]>0.0 and y_tmp[i]>0.0:
            x.append(x_tmp[i])
            y.append(y_tmp[i])

    if xlog==True:
        x=np.log10(x)

    if ylog==True:
        y=np.log10(y)

    return x, y

def set_color(c,n):
    if c == "rainbow":
        color = cm.rainbow(n/8.)
    elif c == "gnuplot":
        color = cm.gnuplot(n/8.)
    elif c == "autumn":
        color = cm.autumn(n/8.)
    elif c == "cool":
        color = cm.cool(n/8.)

    return color

def get_data(txtfile,usecols,keys,variable,c,n,xlog,ylog):
    """
    """
    x = load_data(txtfile,keys[0],usecols[0])
    y = load_data(txtfile,keys[1],usecols[1])
    x, y = process_data(x,y,xlog,ylog)
    size = beam_data(txtfile,variable)
    color = set_color(c,n)

    return x, y, size, color

def get_data_both(txtfile,usecols,keys,xlog,ylog):
    """
    """
    x = load_data(txtfile,keys[0],usecols[0])
    y = load_data(txtfile,keys[1],usecols[1])
    x, y = process_data(x,y,xlog,ylog)
    bm_size = beam_data(txtfile,"beam")
    ap_size = beam_data(txtfile,"aperture")
    
    return x, y, bm_size, ap_size

def get_stats(y):
    stats = []
    for i in range(len(y)):
        if y[i] > -10000:
            stats.append(y[i])

    mean = np.mean(stats)
    medi = np.median(stats)
    std = np.std(stats)

    return mean, medi, std

def plot_a0xy(txtfiles,
              usecols,
              keys,
              limit,
              limit2,
              bins,
              xlabel,
              ylabel,
              text,
              title,
              xlog,
              ylog,
              c,
              variable,
              savefig):
    """
    """
    figure = plt.figure(figsize=(16, 16))
    plt.rcParams["font.size"] = 24

    gs = gridspec.GridSpec(nrows=18, ncols=18)
    a00 = plt.subplot(gs[0:9,0:9])
    a00.set_xticks([])
    a00b = a00.twiny()

    # a00
    a00.set_xlim(limit)
    a00.set_ylim(limit2)
    a00b.set_xlim(limit)
    a00b.set_xlabel(xlabel)
    a00.set_ylabel(ylabel)

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
    ax1.spines["top"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax3.spines["top"].set_visible(False)
    ax3.spines["bottom"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.spines["left"].set_visible(False)
    ax4.spines["top"].set_visible(False)
    ax4.spines["bottom"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    ax4.spines["left"].set_visible(False)
    ax5.spines["top"].set_visible(False)
    ax5.spines["bottom"].set_visible(False)
    ax5.spines["right"].set_visible(False)
    ax5.spines["left"].set_visible(False)
    ax6.spines["top"].set_visible(False)
    ax6.spines["bottom"].set_visible(False)
    ax6.spines["right"].set_visible(False)
    ax6.spines["left"].set_visible(False)
    ax7.spines["top"].set_visible(False)
    ax7.spines["bottom"].set_visible(False)
    ax7.spines["right"].set_visible(False)
    ax7.spines["left"].set_visible(False)
    ax8.spines["top"].set_visible(False)
    ax8.spines["bottom"].set_visible(False)
    ax8.spines["right"].set_visible(False)
    ax8.spines["left"].set_visible(False)
    ax9.spines["top"].set_visible(False)
    ax9.spines["bottom"].set_visible(False)
    ax9.spines["left"].set_visible(False)
    ax9b.spines["top"].set_visible(False)
    ax9b.spines["bottom"].set_visible(False)
    ax9b.spines["left"].set_visible(False)
    ax1.set_ylim(limit2)
    ax2.set_ylim(limit2)
    ax3.set_ylim(limit2)
    ax4.set_ylim(limit2)
    ax5.set_ylim(limit2)
    ax6.set_ylim(limit2)
    ax7.set_ylim(limit2)
    ax8.set_ylim(limit2)
    ax9b.set_ylim(limit2)
    ax9b.set_ylabel(ylabel)
    
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
    ay1.invert_yaxis()
    ay1.spines["top"].set_visible(False)
    ay1.spines["bottom"].set_visible(False)
    ay1.spines["right"].set_visible(False)
    ay1.spines["left"].set_visible(False)
    ay2.invert_yaxis()
    ay2.spines["top"].set_visible(False)
    ay2.spines["bottom"].set_visible(False)
    ay2.spines["right"].set_visible(False)
    ay2.spines["left"].set_visible(False)
    ay3.invert_yaxis()
    ay3.spines["top"].set_visible(False)
    ay3.spines["bottom"].set_visible(False)
    ay3.spines["right"].set_visible(False)
    ay3.spines["left"].set_visible(False)
    ay4.invert_yaxis()
    ay4.spines["top"].set_visible(False)
    ay4.spines["bottom"].set_visible(False)
    ay4.spines["right"].set_visible(False)
    ay4.spines["left"].set_visible(False)
    ay5.invert_yaxis()
    ay5.spines["top"].set_visible(False)
    ay5.spines["bottom"].set_visible(False)
    ay5.spines["right"].set_visible(False)
    ay5.spines["left"].set_visible(False)
    ay6.invert_yaxis()
    ay6.spines["top"].set_visible(False)
    ay6.spines["bottom"].set_visible(False)
    ay6.spines["right"].set_visible(False)
    ay6.spines["left"].set_visible(False)
    ay7.invert_yaxis()
    ay7.spines["top"].set_visible(False)
    ay7.spines["bottom"].set_visible(False)
    ay7.spines["right"].set_visible(False)
    ay7.spines["left"].set_visible(False)
    ay8.invert_yaxis()
    ay8.spines["top"].set_visible(False)
    ay8.spines["bottom"].set_visible(False)
    ay8.spines["right"].set_visible(False)
    ay8.spines["left"].set_visible(False)
    ay9.invert_yaxis()
    ay9.spines["top"].set_visible(False)
    ay9.spines["left"].set_visible(False)
    ay9.spines["right"].set_visible(False)
    ay1.set_xlim(limit)
    ay2.set_xlim(limit)
    ay3.set_xlim(limit)
    ay4.set_xlim(limit)
    ay5.set_xlim(limit)
    ay6.set_xlim(limit)
    ay7.set_xlim(limit)
    ay8.set_xlim(limit)
    ay9.set_xlim(limit)
    ay9.set_xlabel(xlabel)

    histtype="stepfilled"
    orientation="horizontal"

    ### a00
    if keys[0]=="Ico10" or keys[0]=="Tco10" or keys[0]=="Ico21" or keys[0]=="Tco21":
        if keys[1] == "Ico21" or keys[1] == "Tco21":
            a00.plot([limit[0],limit[1]],
                     [limit[0],limit[1]],
                     "black",
                     linewidth = 2)
            a00.plot([limit[0],limit[1]],
                     [limit[0]+np.log10(0.8),limit[1]+np.log10(0.8)],
                     "black",
                     linestyle="dashed",
                     linewidth = 2)
            a00.plot([limit[0],limit[1]],
                     [limit[0]+np.log10(0.5),limit[1]+np.log10(0.5)],
                     "black",
                     linestyle="dashed",
                     linewidth = 2)
            a00.plot([limit[0],limit[1]],
                     [limit[0]+np.log10(0.2),limit[1]+np.log10(0.2)],
                     "black",
                     linestyle="dashed",
                     linewidth = 2)

    if keys[1] == "R21" or keys[1] == "M21":
        a00.plot([limit[0],limit[1]],
                 [np.log10(1),np.log10(1)],
                 "black",
                 linewidth = 2)
        a00.plot([limit[0],limit[1]],
                 [np.log10(0.8),np.log10(0.8)],
                 "black",
                 linestyle="dashed",
                 linewidth = 2)
        a00.plot([limit[0],limit[1]],
                 [np.log10(0.5),np.log10(0.5)],
                 "black",
                 linestyle="dashed",
                 linewidth = 2)
        a00.plot([limit[0],limit[1]],
                 [np.log10(0.2),np.log10(0.2)],
                 "black",
                 linestyle="dashed",
                 linewidth = 2)

    for i in range(len(txtfiles)):
        # a00: plot
        x, y, size, color = get_data(txtfiles[i],usecols,keys,variable,c,i,xlog,ylog)
        a00.scatter(x,y,s=70,c=color,alpha=0.4,linewidth=0,
                    label=str(size)+"\"")

    length, length2 = limit[1] - limit[0], limit2[1] - limit2[0]
    a00.text(limit[0] + length*0.05, limit2[1] - length2*0.15, text)
    a00.legend(bbox_to_anchor=(1.02,-0.2),loc="upper left",ncol=2,title=title)

    ### ax1
    x, y, size, color = get_data(txtfiles[0],usecols,keys,variable,c,0,xlog,ylog)
    mean, medi, std = get_stats(y)
    histo=ax1.hist(y,alpha=0.4,histtype=histtype,orientation=orientation,
                   color=color,bins=bins,linewidth=0,range=limit2)
    ax1.set_xlim(0,max(histo[0][1:]))
    ax1.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
    ax1.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)
    ax1.fill_between([0,max(histo[0][1:])],mean-std,mean+std,
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ax2
    x, y, size, color = get_data(txtfiles[1],usecols,keys,variable,c,1,xlog,ylog)
    mean, medi, std = get_stats(y)
    histo=ax2.hist(y,alpha=0.4,histtype=histtype,orientation=orientation,
                   color=color,bins=bins,linewidth=0,range=limit2)
    ax2.set_xlim(0,max(histo[0][1:]))
    ax2.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
    ax2.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)
    ax2.fill_between([0,max(histo[0][1:])],mean-std,mean+std,
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ax3
    x, y, size, color = get_data(txtfiles[2],usecols,keys,variable,c,2,xlog,ylog)
    mean, medi, std = get_stats(y)
    histo=ax3.hist(y,alpha=0.4,histtype=histtype,orientation=orientation,
                   color=color,bins=bins,linewidth=0,range=limit2)
    ax3.set_xlim(0,max(histo[0][1:]))
    ax3.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
    ax3.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)
    ax3.fill_between([0,max(histo[0][1:])],mean-std,mean+std,
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ax4
    x, y, size, color = get_data(txtfiles[3],usecols,keys,variable,c,3,xlog,ylog)
    mean, medi, std = get_stats(y)
    histo=ax4.hist(y,alpha=0.4,histtype=histtype,orientation=orientation,
                   color=color,bins=bins,linewidth=0,range=limit2)
    ax4.set_xlim(0,max(histo[0][1:]))
    ax4.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
    ax4.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)
    ax4.fill_between([0,max(histo[0][1:])],mean-std,mean+std,
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ax5
    x, y, size, color = get_data(txtfiles[4],usecols,keys,variable,c,4,xlog,ylog)
    mean, medi, std = get_stats(y)
    histo=ax5.hist(y,alpha=0.4,histtype=histtype,orientation=orientation,
                   color=color,bins=bins,linewidth=0,range=limit2)
    ax5.set_xlim(0,max(histo[0][1:]))
    ax5.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
    ax5.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)
    ax5.fill_between([0,max(histo[0][1:])],mean-std,mean+std,
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ax6
    x, y, size, color = get_data(txtfiles[5],usecols,keys,variable,c,5,xlog,ylog)
    mean, medi, std = get_stats(y)
    histo=ax6.hist(y,alpha=0.4,histtype=histtype,orientation=orientation,
                   color=color,bins=bins,linewidth=0,range=limit2)
    ax6.set_xlim(0,max(histo[0][1:]))
    ax6.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
    ax6.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)
    ax6.fill_between([0,max(histo[0][1:])],mean-std,mean+std,
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ax7
    x, y, size, color = get_data(txtfiles[6],usecols,keys,variable,c,6,xlog,ylog)
    mean, medi, std = get_stats(y)
    histo=ax7.hist(y,alpha=0.4,histtype=histtype,orientation=orientation,
                   color=color,bins=bins,linewidth=0,range=limit2)
    ax7.set_xlim(0,max(histo[0][1:]))
    ax7.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
    ax7.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)
    ax7.fill_between([0,max(histo[0][1:])],mean-std,mean+std,
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ax8
    x, y, size, color = get_data(txtfiles[7],usecols,keys,variable,c,7,xlog,ylog)
    mean, medi, std = get_stats(y)
    histo=ax8.hist(y,alpha=0.4,histtype=histtype,orientation=orientation,
                   color=color,bins=bins,linewidth=0,range=limit2)
    ax8.set_xlim(0,max(histo[0][1:]))
    ax8.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
    ax8.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)
    ax8.fill_between([0,max(histo[0][1:])],mean-std,mean+std,
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ax9
    x, y, size, color = get_data(txtfiles[8],usecols,keys,variable,c,8,xlog,ylog)
    mean, medi, std = get_stats(y)
    histo=ax9b.hist(y,alpha=0.4,histtype=histtype,orientation=orientation,
                    color=color,bins=bins,linewidth=0,range=limit2)
    ax9b.set_xlim(0,max(histo[0][1:]))
    ax9b.plot([0,max(histo[0][1:])], [mean,mean], '--', c="black", lw=2)
    ax9b.plot([0,max(histo[0][1:])], [medi,medi], '-', c="black", lw=2)
    ax9b.fill_between([0,max(histo[0][1:])],mean-std,mean+std,
                      linewidth=0,facecolor="grey",alpha=0.5)

    ### ay1
    x, y, size, color = get_data(txtfiles[0],usecols,keys,variable,c,0,xlog,ylog)
    mean, medi, std = get_stats(x)
    histo=ay1.hist(x,alpha=0.4,histtype=histtype,
                   color=color,bins=bins,linewidth=0,range=limit)
    ay1.set_ylim(0,max(histo[0][1:]))
    ay1.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
    ay1.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)
    ay1.fill_between([mean-std,mean+std],0,max(histo[0][1:]),
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ay2
    x, y, size, color = get_data(txtfiles[1],usecols,keys,variable,c,1,xlog,ylog)
    mean, medi, std = get_stats(x)
    histo=ay2.hist(x,alpha=0.4,histtype=histtype,
                   color=color,bins=bins,linewidth=0,range=limit)
    ay2.set_ylim(0,max(histo[0][1:]))
    ay2.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
    ay2.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)
    ay2.fill_between([mean-std,mean+std],0,max(histo[0][1:]),
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ay3
    x, y, size, color = get_data(txtfiles[2],usecols,keys,variable,c,2,xlog,ylog)
    mean, medi, std = get_stats(x)
    histo=ay3.hist(x,alpha=0.4,histtype=histtype,
                   color=color,bins=bins,linewidth=0,range=limit)
    ay3.set_ylim(0,max(histo[0][1:]))
    ay3.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
    ay3.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)
    ay3.fill_between([mean-std,mean+std],0,max(histo[0][1:]),
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ay4
    x, y, size, color = get_data(txtfiles[3],usecols,keys,variable,c,3,xlog,ylog)
    mean, medi, std = get_stats(x)
    histo=ay4.hist(x,alpha=0.4,histtype=histtype,
                   color=color,bins=bins,linewidth=0,range=limit)
    ay4.set_ylim(0,max(histo[0][1:]))
    ay4.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
    ay4.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)
    ay4.fill_between([mean-std,mean+std],0,max(histo[0][1:]),
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ay5
    x, y, size, color = get_data(txtfiles[4],usecols,keys,variable,c,4,xlog,ylog)
    mean, medi, std = get_stats(x)
    histo=ay5.hist(x,alpha=0.4,histtype=histtype,
                   color=color,bins=bins,linewidth=0,range=limit)
    ay5.set_ylim(0,max(histo[0][1:]))
    ay5.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
    ay5.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)
    ay5.fill_between([mean-std,mean+std],0,max(histo[0][1:]),
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ay6
    x, y, size, color = get_data(txtfiles[5],usecols,keys,variable,c,5,xlog,ylog)
    mean, medi, std = get_stats(x)
    histo=ay6.hist(x,alpha=0.4,histtype=histtype,
                   color=color,bins=bins,linewidth=0,range=limit)
    ay6.set_ylim(0,max(histo[0][1:]))
    ay6.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
    ay6.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)
    ay6.fill_between([mean-std,mean+std],0,max(histo[0][1:]),
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ay7
    x, y, size, color = get_data(txtfiles[6],usecols,keys,variable,c,6,xlog,ylog)
    mean, medi, std = get_stats(x)
    histo=ay7.hist(x,alpha=0.4,histtype=histtype,
                   color=color,bins=bins,linewidth=0,range=limit)
    ay7.set_ylim(0,max(histo[0][1:]))
    ay7.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
    ay7.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)
    ay7.fill_between([mean-std,mean+std],0,max(histo[0][1:]),
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ay8
    x, y, size, color = get_data(txtfiles[7],usecols,keys,variable,c,7,xlog,ylog)
    mean, medi, std = get_stats(x)
    histo=ay8.hist(x,alpha=0.4,histtype=histtype,
                   color=color,bins=bins,linewidth=0,range=limit)
    ay8.set_ylim(0,max(histo[0][1:]))
    ay8.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
    ay8.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)
    ay8.fill_between([mean-std,mean+std],0,max(histo[0][1:]),
                     linewidth=0,facecolor="grey",alpha=0.5)

    ### ay9
    x, y, size, color = get_data(txtfiles[8],usecols,keys,variable,c,8,xlog,ylog)
    mean, medi, std = get_stats(x)
    histo=ay9.hist(x,alpha=0.4,histtype=histtype,
                   color=color,bins=bins,linewidth=0,range=limit)
    ay9.set_ylim(0,max(histo[0][1:]))
    ay9.plot([mean,mean], [0,max(histo[0][1:])], '--', c="black", lw=2)
    ay9.plot([medi,medi], [0,max(histo[0][1:])], '-', c="black", lw=2)
    ay9.fill_between([mean-std,mean+std],0,max(histo[0][1:]),
                     linewidth=0,facecolor="grey",alpha=0.5)

    plt.legend(loc="upper left",ncol=2)
    plt.savefig(savefig,dpi=100)

def prepare_heatmap_ratio(txt_files,
                          output,
                          usecols_orig, # usecols = [2,3]
                          c,
                          xlog,
                          ylog,
                          keys1,
                          keys2,
                          ):
    """
    """
    usecols1 = [[usecols_orig[1]], usecols_orig]
    usecols2 = [[usecols_orig[0]], [usecols_orig[1]]]
    os.system("rm -rf " + output)
    f = open(output, "a")
    f.write("#ap bm median std theta\n")

    for i in range(len(txt_files)):
        x,y,bm_size,ap_size=get_data_both(txt_files[i],usecols1,keys1,xlog,ylog)
        x2,y2,bm_size,ap_size=get_data_both(txt_files[i],usecols2,keys2,xlog=True,ylog=True)
        popt, pcov = curve_fit(func_c1, x2, y2)

        atan1 = math.degrees(math.atan(popt[0]))
        
        f.write(str(ap_size)+" "+str(bm_size)+" "\
                +str(np.median(y))+" "+str(np.std(y))+" "+str(atan1)+"\n")

    f.close()

def func_c1(x, a, b):
    return a*x + b

def plotter_heatmap_ratio(txt_data,
                          outpng,
                          scale,
                          xlim,
                          ylim,
                          xlabel,
                          ylabel,
                          text,
                          label,
                          clim):
    """
    """
    data = np.loadtxt(txt_data, usecols=(0,1,2,3,4))

    plt.figure(figsize=(10,8))
    plt.rcParams["font.size"] = 18

    plt.scatter(data[:,0]*scale,
                data[:,1]*scale,
                s=750,
                linewidth=0,
                c=data[:,2],
                marker="s")

    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.clim(clim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.text(xlim[0]+(xlim[1]-xlim[0])*0.05,ylim[1]-(ylim[1]-ylim[0])*0.08,text)
    cbar=plt.colorbar()
    cbar.set_label(label, size=18)
    plt.savefig(outpng,dpi=100)
