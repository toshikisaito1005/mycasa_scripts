import glob
sys.path.append(os.getcwd())
import scripts_phangs_r21_plot as r21_plot


#####################
### Main Procedure
#####################
i = 3
gal = ["ngc0628", "ngc4321", "ngc3627", "ngc4254"]
clim = [[0.55,0.68], [0.4,0.65], [0.65,0.78], [0.6,0.69]]
scale = [44/1.0/1000., 103/1.4/1000., 52/1.3/1000., 130/1.6/1000.]
xlim = [[1*scale[i],35*scale[i]],
        [1*scale[i],35*scale[i]],
        [5*scale[i],39*scale[i]],
        [5*scale[i],39*scale[i]]]
gal, clim, scale, xlim, ylim = gal[i], clim[i], scale[i], xlim[i], xlim[i]

text = "(d) median $R_{21}$, $Me$($R_{21}$), for "+gal.replace("ngc","NGC ")


# uw
dir_data = "../../phangs/co_ratio/"+gal+"_co/"
output = dir_data + "bm_vs_ap_r21_median.txt"
outpng = "../../phangs/co_ratio/eps/heatmap_r21_median_"+gal+".png"
txt_files = glob.glob(dir_data+gal+"*no.txt")
usecols = [2,3]
c = "rainbow"
xlog = False
ylog = False
xlabel = "Aperture Size (kpc)"
ylabel = "Beam Size (kpc)"
label = "$Me$($R_{21}$)"

r21_plot.heatmap_ratio(txt_files,
                       output,
                       outpng,
                       usecols,
                       c,
                       xlog,
                       ylog,
                       scale,
                       xlim,
                       ylim,
                       xlabel,
                       ylabel,
                       text,
                       label,
                       clim,
                       keys1=["Ico21", "R21"],
                       keys2=["Ico10", "Ico21"])
"""
# w
dir_data = "../../phangs/co_ratio/"+gal+"_co/"
output = dir_data + "bm_vs_ap_r21_median_w.txt"
outpng = "../../phangs/co_ratio/eps/heatmap_r21_median_w.png"
txt_files = glob.glob(dir_data+gal+"*w.txt")
usecols = [2,3]
c = "rainbow"
xlog = False
ylog = False
xlim = [1*scale,35*scale]
ylim = [1*scale,35*scale]
xlabel = "Aperture Size (kpc)"
ylabel = "Beam Size (kpc)"
text = "(a) median $R_{21,w}$, $Me$($R_{21,w}$)"
label = "$Me$($R_{21,w}$)"

r21_plot.heatmap_ratio(txt_files,
                       output,
                       outpng,
                       usecols,
                       c,
                       xlog,
                       ylog,
                       scale,
                       xlim,
                       ylim,
                       xlabel,
                       ylabel,
                       text,
                       label,
                       clim,
                       keys1=["Ico21", "R21"],
                       keys2=["Ico10", "Ico21"])
"""
