import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.optimize
from scipy.optimize import curve_fit
import matplotlib.colors as clr
plt.ioff()


#####################
### Define Functions
#####################
def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

def plotter(aperture,
            dx,
            dy,
            fco10,
            fco21,
            dval,
            savefig,
            ylim_rval = [0,1.201],
            xlim = [120,-120],
            ylim = [-120,120]):
    ### setup
    figure = plt.figure(figsize=(16, 6))
    plt.rcParams["font.size"] = 18
    gs = gridspec.GridSpec(nrows=6, ncols=13)
    ax1 = plt.subplot(gs[0:5,12])
    ax2 = plt.subplot(gs[0:5,0:4])
    ax3 = plt.subplot(gs[5,0:4])
    ax4 = plt.subplot(gs[0:5,4:8])
    ax5 = plt.subplot(gs[5,4:8])
    ax6 = plt.subplot(gs[0:5,8:12])
    ax7 = plt.subplot(gs[5,8:12])
    plt.subplots_adjust(left=0.06, right=0.93, bottom=0.11, top=0.94)
    
    #
    cdict3 = {'red':((0.0,1.0,1.0),
                     (0.5,0.25,0.25),
                     (1.0,1.0,1.0)),
              'green':((0.0,1.0,1.0),
                       (0.5,0.5,0.5),
                       (0.75,1.0,1.0),
                       (1.0,0.25,0.25)),
              'blue':((0.0,1.0,1.0),
                      (0.5,0.75,0.75),
                      (0.75,0.0,0.0),
                      (1.0,0.0,0.0))}
    mycolor3 = clr.LinearSegmentedColormap('mycolor3', cdict3)

    ax2.set_title("CO(1-0) Integrated Intensity")
    ax4.set_title("CO(2-1) Integrated Intensity")
    ax6.set_title("$R_{21}$")

    ### ax1
    ax1.set_visible(False)

    ### ax2
    if "3627" in savefig:
        size_x = 20
        size_y = 22
    else:
        if np.sqrt(len(dx)).is_integer() == True:
            size_x = int(np.sqrt(len(dx)))
            size_y = int(np.sqrt(len(dy)))
        else:
            size_x = int(np.sqrt(len(dx))+1.0)
            size_y = int(np.sqrt(len(dx)))

    X1 = np.reshape(dx*3600, (size_x, size_y))
    Y1 = np.reshape(dy*3600, (size_x, size_y))
    Z1 = np.reshape(fco10, (size_x, size_y))
    ax2.pcolor(X1, Y1, Z1, cmap="PuBu")
    pk = max(fco10)
    levels = [pk*0.02, pk*0.04, pk*0.08, pk*0.16,
              pk*0.32, pk*0.64, pk*0.96]
    ax2.contour(X1, Y1, Z1, levels=levels, linewidths=0.5,
                colors = ["grey"])
    ax2.invert_xaxis()
    ax2.set_xlim(xlim)
    ax2.set_ylim(ylim)
    ax2.set_xlabel("x-offset (arcsec)")
    ax2.set_ylabel("y-offset (arcsec)")

    ### ax3
    ax3.set_visible(False)

    ### ax4
    X2 = np.reshape(dx*3600, (size_x, size_y))
    Y2 = np.reshape(dy*3600, (size_x, size_y))
    Z2 = np.reshape(fco21, (size_x, size_y))
    ax4.pcolor(X2, Y2, Z2, cmap="OrRd")
    pk = max(fco21)
    levels = [pk*0.01, pk*0.02, pk*0.04, pk*0.08,
              pk*0.16, pk*0.32, pk*0.64, pk*0.96]
    ax4.contour(X2, Y2, Z2, levels=levels, linewidths=0.5,
                colors = ["grey"])
    ax4.invert_xaxis()
    ax4.set_xlim(xlim)
    ax4.set_ylim(ylim)
    ax4.set_yticks([])
    ax4.set_xlabel("x-offset (arcsec)")
    
    ### ax5
    ax5.set_visible(False)

    ### ax6
    X3 = np.reshape(dx*3600, (size_x, size_y))
    Y3 = np.reshape(dy*3600, (size_x, size_y))
    Z3 = np.reshape(dval, (size_x, size_y))
    ratio_map=ax6.pcolor(X3, Y3, Z3, cmap=mycolor3)
    pk = max(fco21)
    ax6.contour(X2, Y2, Z2,
                levels=levels,
                linewidths=0.5,
                colors = ["black"])
    ax6.invert_xaxis()
    ax6.set_xlim(xlim)
    ax6.set_ylim(ylim)
    ax6.set_yticks([])
    ax6.set_xlabel("x-offset (arcsec)")
    #cbaxes = figure.add_axes([0.822, 0.278, 0.01, 0.3]) #l,b,w,h
    cbaxes = figure.add_axes([0.8735, 0.252, 0.0564/3., 0.688])
    cbar = plt.colorbar(ratio_map, ax=ax6,
                        cax=cbaxes,
                        ticks=[0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6])
    cbar.set_label("$R_{21}$")

    ### ax7
    ax7.set_visible(False)

    plt.savefig(savefig,dpi=300)



#####################
### Main Procedure
#####################
### ngc4321
scale = 0.103
pa = 157.8
incl = 35.1
ra_dgr = 185.729
dec_dgr = 15.8229
dir_data = "../../phangs/co_ratio/ngc4321/"

txtfiles = glob.glob(dir_data + "*_flux_4p0_*.txt")
for i in range(len(txtfiles)):
    aperture = int(txtfiles[i].split("_")[-1].replace(".txt",""))
    data = np.loadtxt(txtfiles[i], usecols=(0,1,6,7,5))
    dx = data[:,0] - ra_dgr
    dy = data[:,1] - dec_dgr
    fco10 = data[:,2]
    fco21 = data[:,3]
    dval = []
    for j in range(len(fco10)):
        if fco10[j] > 0:
            if fco21[j] > 0:
                dval.append(fco21[j]/fco10[j]/4.0)
            else:
                dval.append(0)
        else:
            dval.append(0)

    plotter(aperture,
            dx,
            dy,
            fco10,
            fco21,
            dval,
            savefig=txtfiles[i].replace(".txt","_map.png"),
            ylim_rval = [0,1.201],
            xlim = [99.0,-100],
            ylim = [-100,100])



### ngc0628
histobin = 50
scale = 0.044
pa = 21.1
incl = 8.7
ra_dgr = 24.1737
dec_dgr = 15.7829
dir_data = "../../phangs/co_ratio/ngc0628/"

txtfiles = glob.glob(dir_data + "*_flux_4p0_*.txt")
for i in range(len(txtfiles)):
    aperture = int(txtfiles[i].split("_")[-1].replace(".txt",""))
    histobin_ap = int(histobin*4 / aperture)
    data = np.loadtxt(txtfiles[i], usecols=(0,1,6,7,5))
    dx = data[:,0] - ra_dgr
    dy = data[:,1] - dec_dgr
    fco10 = data[:,2]
    fco21 = data[:,3]
    dval = []
    for j in range(len(fco10)):
        if fco10[j] > 0:
            if fco21[j] > 0:
                dval.append(fco21[j]/fco10[j]/4.0)
            else:
                dval.append(0)
        else:
            dval.append(0)

    plotter(aperture,
            dx,
            dy,
            fco10,
            fco21,
            dval,
            savefig=txtfiles[i].replace(".txt","_map.png"),
            ylim_rval = [0,1.01],
            xlim = [125,-125],
            ylim = [-125,125])


### ngc3627
histobin = 50
scale = 0.040
pa = 172.4
incl = 56.2
ra_dgr = 170.063
dec_dgr = 12.9916
dir_data = "../../phangs/co_ratio/ngc3627/"

txtfiles = glob.glob(dir_data + "*_flux_8p0_*.txt")
for i in range(len(txtfiles)):
    aperture = int(txtfiles[i].split("_")[-1].replace(".txt",""))
    histobin_ap = int(histobin*4 / aperture)
    data = np.loadtxt(txtfiles[i], usecols=(0,1,6,7,5))
    dx = data[:,0] - ra_dgr
    dy = data[:,1] - dec_dgr
    fco10 = data[:,2]
    fco21 = data[:,3]
    dval = []
    for j in range(len(fco10)):
        if fco10[j] > 0:
            if fco21[j] > 0:
                dval.append(fco21[j]/fco10[j]/4.0)
            else:
                dval.append(0)
        else:
            dval.append(0)

    plotter(aperture,
            dx,
            dy,
            fco10,
            fco21,
            dval,
            savefig=txtfiles[i].replace(".txt","_map.png"),
            ylim_rval = [0,1.01],
            xlim = [125,-125],
            ylim = [-125,125])



### ngc4254
histobin = 50
scale = 0.08125
dir_data = "../../phangs/co_ratio/ngc4254/"

txtfiles = glob.glob(dir_data + "*_flux_8p0_*.txt")
for i in range(len(txtfiles)):
    aperture = int(txtfiles[i].split("_")[-1].replace(".txt",""))
    histobin_ap = int(histobin*4 / aperture)
    data = np.loadtxt(txtfiles[i], usecols=(0,1,6,7,5))
    dx = data[:,0] - ra_dgr
    dy = data[:,1] - dec_dgr
    fco10 = data[:,2]
    fco21 = data[:,3]
    dval = []
    for j in range(len(fco10)):
        if fco10[j] > 0:
            if fco21[j] > 0:
                dval.append(fco21[j]/fco10[j]/4.0)
            else:
                dval.append(0)
        else:
            dval.append(0)

    plotter(aperture,
            dx,
            dy,
            fco10,
            fco21,
            dval,
            savefig=txtfiles[i].replace(".txt","_map.png"),
            ylim_rval = [0,1.01])

