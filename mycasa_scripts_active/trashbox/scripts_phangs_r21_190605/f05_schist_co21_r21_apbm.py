import glob
sys.path.append(os.getcwd())
import scripts_phangs_r21_plot as r21_plot


### setup
gal = "ngc0628" # ngc4321"
dir_data = "../../phangs/co_ratio/"+gal+"_co/"
xlog=True
ylog=True # False


### figure 4
# figure 4a
txtfiles = [dir_data+gal+"_flux_4p0_4p0_no.txt",
            dir_data+gal+"_flux_4p0_6p0_no.txt",
            dir_data+gal+"_flux_4p0_8p0_no.txt",
            dir_data+gal+"_flux_4p0_10p0_no.txt",
            dir_data+gal+"_flux_4p0_12p0_no.txt",
            dir_data+gal+"_flux_4p0_14p0_no.txt",
            dir_data+gal+"_flux_4p0_16p0_no.txt",
            dir_data+gal+"_flux_4p0_18p0_no.txt",
            dir_data+gal+"_flux_4p0_20p0_no.txt"]

usecols = [[3], [2,3]]
keys = ["Ico21", "R21"]
limit = [-1.5,2.49]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 30
xlabel = "log $I_{CO(2-1)}$ (K km s$^{-1}$)"
ylabel = "log $R_{21}$"
text = "a) log $I_{CO(2-1)}$ vs. log $R_{21}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/fig05a_n4321_r21_v_co21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 4b
txtfiles = [dir_data+gal+"_flux_4p0_20p0_no.txt",
            dir_data+gal+"_flux_6p0_20p0_no.txt",
            dir_data+gal+"_flux_8p0_20p0_no.txt",
            dir_data+gal+"_flux_10p0_20p0_no.txt",
            dir_data+gal+"_flux_12p0_20p0_no.txt",
            dir_data+gal+"_flux_14p0_20p0_no.txt",
            dir_data+gal+"_flux_16p0_20p0_no.txt",
            dir_data+gal+"_flux_18p0_20p0_no.txt",
            dir_data+gal+"_flux_20p0_20p0_no.txt"]

usecols = [[7], [6,7]]
keys = ["Tco21", "M21"]
limit = [-3.3,0.5]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 30
xlabel = "log $T_{CO(2-1)}$ (K)"
ylabel = "log $M_{21}$"
text = "b) log $I_{CO(2-1)}$ vs. log $M_{21}$ with \n    varying beam size"
title = "Beam Size (Fixed Aperture = 20\")"
c = "gnuplot"
variable="beam"
savefig = "/Users/saito/data/phangs/co_ratio/eps/fig05b_n4321_r21_v_co21_bm.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

