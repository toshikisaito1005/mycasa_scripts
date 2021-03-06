import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.optimize
from scipy.optimize import curve_fit
plt.ioff()


#####################
### Define Functions
#####################
def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

def txt2ratio_radial(txtfile,
                     coeff,
                     cent_x,
                     cent_y,
                     scale,
                     pa,
                     incl):
    """
    """
    data = np.loadtxt(txtfile, usecols=(0,1,2,3,4,5,6,8,11))
    dx, dy = data[:,0] - cent_x, data[:,1] - cent_y
    pa_radi = math.radians(pa)
    incl_radi = math.radians(90-incl)
    dx2 = (dx*math.cos(pa_radi) - dy*math.sin(pa_radi)) \
          / math.sin(incl_radi)
    dy2 = dx*math.sin(pa_radi) + dy*math.cos(pa_radi)
    dval_tmp = data[:,3] / data[:,2] / coeff
    drad_tmp = np.sqrt((dx2)**2 + (dy2)**2)
    drad_tmp2 = drad_tmp * 3600 * scale
    ddisp_tmp = data[:,7] * math.sin(incl_radi)
    fw1_tmp = data[:,4]
    fw2_tmp = data[:,5]
    fw3_tmp = data[:,6]
    dval = []
    drad = []
    ddisp = []
    fco21 = []
    fw1 = []
    fw2 = []
    fw3 = []
    rw3w1 = []
    rw3ddisp = []
    rw3fco21 = []
    galmask = []
    for j in range(len(dval_tmp)):
        if data[:,2][j] > 0:
            if data[:,3][j] > 0:
                if fw1_tmp[j] > 0:
                    dval.append(dval_tmp[j])
                    drad.append(drad_tmp2[j])
                    ddisp.append(ddisp_tmp[j])
                    fco21.append(data[:,3][j])
                    fw1.append(fw1_tmp[j])
                    fw2.append(fw2_tmp[j])
                    fw3.append(fw3_tmp[j])
                    rw3w1.append(fw3_tmp[j]/fw1_tmp[j])
                    rw3ddisp.append(fw1_tmp[j]/ddisp_tmp[j])
                    rw3fco21.append(fw1_tmp[j]/data[:,3][j])
                    if data[:,8][j] > 0.5:
                        galmask.append(1.0)
                    else:
                        galmask.append(0.0)

    dval = np.array(dval)
    drad = np.array(drad)
    ddisp = np.array(ddisp)

    return dval, drad, ddisp, fco21, rw3w1, rw3ddisp, rw3fco21, galmask


def plotter(aperture,
            drad,
            dval,
            ddisp,
            fco21,
            rw3w1,
            rw3ddisp,
            rw3fco21,
            galamsk,
            histobin_ap,
            savefig,
            ylim_rval = [0,1.001]):
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

    #ax1.set_title(str(aperture)+"\"")
    ax2.set_title("log W3/W1")
    ax4.set_title("log W3/$\sigma$")
    ax6.set_title("log W3/$S_{CO(2-1)}dv$")

    ### ax1
    edges_y = [0.05*x for x in range(40)]
    hist_ax1 = ax1.hist(dval,
                        bins=edges_y,
                        alpha=0.4,
                        histtype="stepfilled",
                        orientation="horizontal",
                        color="grey")#"cornflowerblue")
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.yaxis.tick_right()
    ax1.set_xlim([max(hist_ax1[0])*1.2,0])
    ax1.set_ylim(ylim_rval)
    ax1.invert_xaxis()
    ax1b = ax1.twinx()
    ax1b.set_xticks([])
    ax1b.set_ylim(ylim_rval)
    ax1b.set_ylabel("$R_{21}$")
    
    # inside mask
    dval_masked_tmp = np.array(dval) * np.array(galmask)
    dval_masked = []
    for i in range(len(dval_masked_tmp)):
        if dval_masked_tmp[i] > 0.0:
            dval_masked.append(dval_masked_tmp[i])

    hist_ax1b = ax1.hist(dval_masked,
                         bins=edges_y,
                         alpha=0.4,
                         linewidth=0,
                         histtype="stepfilled",
                         orientation="horizontal",
                         color="red")

    # outside mask
    dval_masked_tmp = np.array(dval) * abs(np.array(galmask)-1)
    dval_masked_out = []
    for i in range(len(dval_masked_tmp)):
        if dval_masked_tmp[i] > 0.0:
            dval_masked_out.append(dval_masked_tmp[i])

    hist_ax1c = np.histogram(dval_masked_out,
                             bins=edges_y)

    #
    popt, pcov = curve_fit(gauss_function,
                           hist_ax1[1][2:],
                           hist_ax1[0][1:],
                           p0 = [150, 0.5, 0.1],
                           maxfev = 100000)
    x = np.linspace(hist_ax1[1][1], hist_ax1[1][-1], 50)
    ax1.plot(gauss_function(x, *popt),
             x,
             "-",
             c="black",
             lw=4)
    ratio_peak = round(popt[1], 2)
    ratio_disp = round(popt[2], 2)

    ax1.hlines([ratio_peak],
               max(hist_ax1[0])*1.2, 0,
               "black",
               linestyles="-",
               linewidth=3)
    ax1.hlines([ratio_peak-ratio_disp],
               max(hist_ax1[0])*1.2, 0,
               "black",
               linestyles="dashed",
               linewidth=3)
    ax1.hlines([ratio_peak+ratio_disp],
               max(hist_ax1[0])*1.2, 0,
               "black",
               linestyles="dashed",
               linewidth=3)

    #
    popt, pcov = curve_fit(gauss_function,
                           hist_ax1b[1][2:],
                           hist_ax1b[0][1:],
                           p0 = [150, 0.5, 0.1],
                           maxfev = 100000)
    x = np.linspace(hist_ax1b[1][1], hist_ax1b[1][-1], 50)
    ratio_peak_red = round(popt[1], 2)
    ratio_disp_red = round(popt[2], 2)

    ax1.hlines([ratio_peak_red],
               max(hist_ax1[0])*1.2, 0,
               "red",
               linestyles="-",
               linewidth=3)

    #
    popt, pcov = curve_fit(gauss_function,
                           hist_ax1c[1][2:],
                           hist_ax1c[0][1:],
                           p0 = [150, 0.5, 0.1],
                           maxfev = 100000)
    x = np.linspace(hist_ax1[1][1], hist_ax1c[1][-1], 50)
    ratio_peak_blue = round(popt[1], 2)
    ratio_disp_blue = round(popt[2], 2)
    
    ax1.hlines([ratio_peak_blue],
               max(hist_ax1[0])*1.2, 0,
               "blue",
               linestyles="-",
               linewidth=3)


    ### ax2
    log_rw3w1 = np.log10(rw3w1)
    #log_xlim = [-0.5, max(log_rw3w1)+0.5]
    log_xlim = [min(log_rw3w1)-0.1, max(log_rw3w1)+0.1]

    ax2.scatter(log_rw3w1,
                dval,
                alpha=0.4,
                c=galamsk,#'cornflowerblue',
                cmap="bwr",
                linewidth=0,
                s=180/(drad+0.5),
                )#label = "aperture = "+str(aperture)+"\"")

    ax2.set_xlim(log_xlim)
    ax2.set_ylim(ylim_rval)
    ax2.set_xticks([])
    ax2.set_ylabel("$R_{21}$")

    label = "$R_{21}$ = "+str(ratio_peak)+" $\pm$ "+str(ratio_disp)
    ax2.hlines([ratio_peak],
               log_xlim[0], log_xlim[1],
               "black",
               linestyles="-",
               linewidth=3,
               )#label = label)
    ax2.hlines([ratio_peak-ratio_disp],
               log_xlim[0], log_xlim[1],
               "black",
               linestyles="dashed",
               linewidth=3)
    ax2.hlines([ratio_peak+ratio_disp],
               log_xlim[0], log_xlim[1],
               "black",
               linestyles="dashed",
               linewidth=3)

    n, _ = np.histogram(log_rw3w1,bins=6)
    sy, _ = np.histogram(log_rw3w1,bins=6,weights=dval)
    sy2, _ = np.histogram(log_rw3w1,bins=6,weights=dval*dval)
    mean = sy / n
    std = np.sqrt(sy2/n - mean*mean)
    ax2.errorbar((_[1:] + _[:-1])/2,
                 mean,
                 yerr=std,
                 c="gray",
                 ecolor="gray",
                 linewidth=5)
    ax2.legend(loc="upper right")

    ### ax3
    edges_x = [0.05*x for x in range(-3,int(max(log_rw3w1)*2)*20,1)]
    hist_ax3 = ax3.hist(log_rw3w1,
                        bins=edges_x,
                        alpha=0.4,
                        histtype="stepfilled",
                        color="grey")#"cornflowerblue")
    ax3.set_xlim(log_xlim)
    ax3.set_ylim([0,max(hist_ax3[0])*1.2])
    ax3.invert_yaxis()
    ax3.set_yticks([])
    ax3.set_xlabel("log W3/W1")

    log_rw3w1_masked_tmp = np.array(log_rw3w1) * np.array(galmask)
    log_rw3w1_masked = []
    for i in range(len(log_rw3w1_masked_tmp)):
        if galmask[i] > 0.5:
            log_rw3w1_masked.append(log_rw3w1_masked_tmp[i])

    hist_ax3b = np.histogram(log_rw3w1_masked,bins=edges_x)

    ax3b = ax3.twinx()
    ax3b.set_xlim(log_xlim)
    ax3b.set_yticks([])
    ax3b.invert_yaxis()
    frac_x = hist_ax3[1]
    frac_y_red = np.array(hist_ax3b[0])/np.array(hist_ax3[0], dtype="float32")
    frac_y_blue = (np.array(hist_ax3[0])-np.array(hist_ax3b[0]))/np.array(hist_ax3[0], dtype="float32")
    ax3b.step(frac_x[1:], frac_y_red, c="red", linewidth=2)
    ax3b.step(frac_x[1:], frac_y_blue, c="blue", linewidth=2)


    ### ax4
    log_fw2 = np.log10(rw3ddisp)
    log_xlim = [min(log_fw2)-0.1, max(log_fw2)+0.1]

    ax4.scatter(log_fw2,
                dval,
                alpha=0.4,
                c=galamsk,#'cornflowerblue',
                cmap="bwr",
                linewidth=0,
                s=180/(drad+0.5),
                )#label = "aperture = "+str(aperture)+"\"")

    ax4.set_xlim(log_xlim)
    ax4.set_ylim(ylim_rval)
    ax4.set_xticks([])
    ax4.set_yticks([])

    ax4.hlines([ratio_peak],
               log_xlim[0], log_xlim[1],
               "black",
               linestyles="-",
               linewidth=3)
    ax4.hlines([ratio_peak-ratio_disp],
               log_xlim[0], log_xlim[1],
               "black",
               linestyles="dashed",
               linewidth=3)
    ax4.hlines([ratio_peak+ratio_disp],
               log_xlim[0], log_xlim[1],
               "black",
               linestyles="dashed",
               linewidth=3)

    n, _ = np.histogram(log_fw2,bins=6)
    sy, _ = np.histogram(log_fw2,bins=6,weights=dval)
    sy2, _ = np.histogram(log_fw2,bins=6,weights=dval*dval)
    mean = sy / n
    std = np.sqrt(sy2/n - mean*mean)
    ax4.errorbar((_[1:] + _[:-1])/2,
                 mean,
                 yerr=std,
                 c="gray",
                 ecolor="gray",
                 linewidth=5)
    ax4.legend(loc="lower right")

    ### ax5
    edges_x = [0.08*x for x in range(-24,int(max(log_fw2)*2)*10,1)]
    hist_ax5 = ax5.hist(log_fw2,
                        bins=edges_x,
                        alpha=0.4,
                        histtype="stepfilled",
                        color="grey")
    ax5.set_xlim(log_xlim)
    ax5.set_ylim([0,max(hist_ax5[0])*1.2])
    ax5.invert_yaxis()
    ax5.set_xticks([-1.2,-0.9,-0.6,-0.3,0.0])
    ax5.set_yticks([])
    ax5.set_xlabel("log W3/$\sigma$")

    log_fw2_masked_tmp = np.array(log_fw2) * np.array(galmask)
    log_fw2_masked = []
    for i in range(len(log_fw2_masked_tmp)):
        if galmask[i] > 0.5:
            log_fw2_masked.append(log_fw2_masked_tmp[i])
    
    hist_ax5b = np.histogram(log_fw2_masked, bins=edges_x)

    ax5b = ax5.twinx()
    ax5b.set_xlim(log_xlim)
    ax5b.set_yticks([])
    ax5b.invert_yaxis()
    frac_x = hist_ax5[1]
    frac_y_red = np.array(hist_ax5b[0])/np.array(hist_ax5[0], dtype="float32")
    frac_y_blue = (np.array(hist_ax5[0])-np.array(hist_ax5b[0]))/np.array(hist_ax5[0], dtype="float32")
    ax5b.step(frac_x[1:], frac_y_red, c="red", linewidth=2)
    ax5b.step(frac_x[1:], frac_y_blue, c="blue", linewidth=2)


    ### ax6
    log_fw3 = np.log10(rw3fco21)
    log_xlim = [min(log_fw3)-0.1, max(log_fw3)+0.1]

    ax6.scatter(log_fw3,
                dval,
                alpha=0.4,
                c=galmask,#'cornflowerblue',
                cmap="bwr",
                linewidth=0,
                s=180/(drad+0.5),
                )#label = "aperture = "+str(aperture)+"\"")

    ax6.set_xlim(log_xlim)
    ax6.set_ylim(ylim_rval)
    ax6.set_xticks([])
    ax6.set_yticks([])

    ax6.hlines([ratio_peak],
               log_xlim[0], log_xlim[1],
               "black",
               linestyles="-",
               linewidth=3)
    ax6.hlines([ratio_peak-ratio_disp],
               log_xlim[0], log_xlim[1],
               "black",
               linestyles="dashed",
               linewidth=3)
    ax6.hlines([ratio_peak+ratio_disp],
               log_xlim[0], log_xlim[1],
               "black",
               linestyles="dashed",
               linewidth=3)

    n, _ = np.histogram(log_fw3,bins=6)
    sy, _ = np.histogram(log_fw3,bins=6,weights=dval)
    sy2, _ = np.histogram(log_fw3,bins=6,weights=dval*dval)
    mean = sy / n
    std = np.sqrt(sy2/n - mean*mean)
    ax6.errorbar((_[1:] + _[:-1])/2,
                 mean,
                 yerr=std,
                 c="gray",
                 ecolor="gray",
                 linewidth=5)
    ax6.legend(loc="upper right")

    ### ax7
    edges_x = [0.1*x for x in range(-18,int(max(log_fw3)*2)*2,1)]
    hist_ax7 = ax7.hist(log_fw3,
                        bins=edges_x,
                        alpha=0.4,
                        histtype="stepfilled",
                        color="grey")#"cornflowerblue")
    ax7.set_xlim(log_xlim)
    ax7.set_ylim([0,max(hist_ax7[0])*1.2])
    ax7.invert_yaxis()
    ax7.set_yticks([])
    ax7.set_xlabel("log W3/$S_{CO(2-1)}dv$")

    log_fw3_masked_tmp = np.array(log_fw3) * np.array(galmask)
    log_fw3_masked = []
    for i in range(len(log_fw3_masked_tmp)):
        if galmask[i] > 0.5:
            log_fw3_masked.append(log_fw3_masked_tmp[i])

    hist_ax7b = np.histogram(log_fw3_masked, bins=edges_x)

    ax7b = ax7.twinx()
    ax7b.set_xlim(log_xlim)
    ax7b.set_xticks([-1.8,-1.5,-1.2,-0.9,-0.6])
    ax7b.set_yticks([0,0.5,1])
    ax7b.invert_yaxis()
    frac_x = hist_ax7[1]
    frac_y_red = np.array(hist_ax7b[0])/np.array(hist_ax7[0], dtype="float32")
    frac_y_blue = (np.array(hist_ax7[0])-np.array(hist_ax7b[0]))/np.array(hist_ax7[0], dtype="float32")
    ax7b.step(frac_x[1:], frac_y_red, c="red", linewidth=2)
    ax7b.step(frac_x[1:], frac_y_blue, c="blue", linewidth=2)

    plt.savefig(savefig,dpi=300)



#####################
### Main Procedure
#####################
### ngc4321
histobin = 50
scale = 0.0736
pa = 157.8
incl = 35.1
ra_dgr = 185.729
dec_dgr = 15.8229
dir_data = "../../phangs/co_ratio/ngc4321/"

txtfiles = glob.glob(dir_data + "*_flux_wise7p5_*.txt")
for i in range(len(txtfiles)):
    aperture = float(txtfiles[i].split("_")[-1].replace(".txt","").replace("p","."))
    histobin_ap = int(histobin*4 / aperture)
    dval, drad, ddisp, fco21, rw3w1, rw3ddisp, rw3fco21, galmask \
        = txt2ratio_radial(txtfiles[i], 4.,ra_dgr, dec_dgr,
                           scale, pa, incl)
    plotter(aperture, drad, dval, ddisp, fco21,
            rw3w1, rw3ddisp, rw3fco21, galmask, histobin_ap,
            savefig=txtfiles[i].replace(".txt","_ratio.png"),
            ylim_rval = [0,1.001])



### ngc0628
histobin = 50
scale = 0.044
pa = 21.1
incl = 8.7
ra_dgr = 24.1737
dec_dgr = 15.7829
dir_data = "../../phangs/co_ratio/ngc0628/"

txtfiles = glob.glob(dir_data + "*_flux_wise7p5_*.txt")
for i in range(len(txtfiles)):
    aperture = float(txtfiles[i].split("_")[-1].replace(".txt","").replace("p","."))
    histobin_ap = int(histobin*4 / aperture)
    dval, drad, ddisp, fco21, rw3w1, rw3ddisp, rw3fco21, galmask \
        = txt2ratio_radial(txtfiles[i], 4.,ra_dgr, dec_dgr,
                           scale, pa, incl)
    plotter(aperture, drad, dval, ddisp, fco21,
            rw3w1, rw3ddisp, rw3fco21, galmask, histobin_ap,
            savefig=txtfiles[i].replace(".txt","_ratio.png"),
            ylim_rval = [0,1.401])



### ngc3627
histobin = 50
scale = 0.040
pa = 172.4
incl = 56.2
ra_dgr = 170.063
dec_dgr = 12.9916
dir_data = "../../phangs/co_ratio/ngc3627/"

txtfiles = glob.glob(dir_data + "*_flux_wise7p5_*.txt")
for i in range(len(txtfiles)):
    aperture = float(txtfiles[i].split("_")[-1].replace(".txt","").replace("p","."))
    histobin_ap = int(histobin*4 / aperture)
    dval, drad, ddisp, fco21, rw3w1, rw3ddisp, rw3fco21, galmask \
        = txt2ratio_radial(txtfiles[i], 4.,ra_dgr, dec_dgr,
                           scale, pa, incl)
    plotter(aperture, drad, dval, ddisp, fco21,
            rw3w1, rw3ddisp, rw3fco21, galmask, histobin_ap,
            savefig=txtfiles[i].replace(".txt","_ratio.png"),
            ylim_rval = [0,1.401])
