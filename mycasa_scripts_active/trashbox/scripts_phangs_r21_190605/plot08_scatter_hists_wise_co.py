import glob
sys.path.append(os.getcwd())
import scripts_phangs_r21_plot as r21_plot


### setup
dir_data = "../../phangs/co_ratio/ngc4321_wise/"
xlog=True
ylog=False
#8, 9, 10

### figure 4
# figure 4a
txtfiles = [dir_data + "ngc4321_flux_8p0_8p0_no.txt",
            dir_data + "ngc4321_flux_8p0_10p0_no.txt",
            dir_data + "ngc4321_flux_8p0_12p0_no.txt",
            dir_data + "ngc4321_flux_8p0_14p0_no.txt",
            dir_data + "ngc4321_flux_8p0_16p0_no.txt",
            dir_data + "ngc4321_flux_8p0_18p0_no.txt",
            dir_data + "ngc4321_flux_8p0_20p0_no.txt",
            dir_data + "ngc4321_flux_8p0_22p0_no.txt",
            dir_data + "ngc4321_flux_8p0_24p0_no.txt"]


# figure 4c
usecols = [[5,10], [2,3]]
keys = ["W3/Tco21", "R21"]
limit = [-5.0,-2.0]
limit2 = [0.0,2.0]
bins = 20
xlabel = "log W3/$T_{CO(2-1)}$"
ylabel = "$R_{21}$"
text = "c) W3/$T_{CO(2-1)}$ vs. $R_{21}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "cool"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/fig07c_n4321_w3co21_v_r21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)
