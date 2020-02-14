import glob
sys.path.append(os.getcwd())
import scripts_phangs_r21_plot as r21_plot



### setup
gal = "ngc0628" #ngc4321"
dir_data = "../../phangs/co_ratio/"+gal+"_co/"
xlog=True
ylog=True



### figure 2
txtfiles = [dir_data+gal+"_flux_4p0_4p0_no.txt",
            dir_data+gal+"_flux_4p0_6p0_no.txt",
            dir_data+gal+"_flux_4p0_8p0_no.txt",
            dir_data+gal+"_flux_4p0_10p0_no.txt",
            dir_data+gal+"_flux_4p0_12p0_no.txt",
            dir_data+gal+"_flux_4p0_14p0_no.txt",
            dir_data+gal+"_flux_4p0_16p0_no.txt",
            dir_data+gal+"_flux_4p0_18p0_no.txt",
            dir_data+gal+"_flux_4p0_20p0_no.txt"]

# figure 2a
usecols = [[2], [3]]
keys = ["Ico10", "Ico21"]
limit = [-1.5,2.49]
limit2 = [-1.5,2.49]
bins = 20
xlabel = "log $I_{CO(1-0)}$ (K km s$^{-1}$)"
ylabel = "log $I_{CO(2-1)}$ (K km s$^{-1}$)"
text = "a) log $I_{CO(1-0)}$ vs log $I_{CO(2-1)}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c="rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/fig03a_n4321_m0_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 2b
usecols = [[6], [7]]
keys = ["Tco10", "Tco21"]
limit = [-2.8,0.8]
limit2 = [-2.8,0.8]
bins = 20
xlabel = "log $T_{CO(1-0)}$ (K)"
ylabel = "log $T_{CO(2-1)}$ (K)"
text = "b) log $T_{CO(1-0)}$ vs log $T_{CO(2-1)}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c="rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/fig03b_n4321_m8_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)



### figure 2w
txtfiles = [dir_data+gal+"_flux_4p0_4p0_w.txt",
            dir_data+gal+"_flux_4p0_6p0_w.txt",
            dir_data+gal+"_flux_4p0_8p0_w.txt",
            dir_data+gal+"_flux_4p0_10p0_w.txt",
            dir_data+gal+"_flux_4p0_12p0_w.txt",
            dir_data+gal+"_flux_4p0_14p0_w.txt",
            dir_data+gal+"_flux_4p0_16p0_w.txt",
            dir_data+gal+"_flux_4p0_18p0_w.txt",
            dir_data+gal+"_flux_4p0_20p0_w.txt"]

# figure 2wa
usecols = [[2], [3]]
keys = ["Ico10", "Ico21"]
limit = [-1.5,2.49]
limit2 = [-1.5,2.49]
bins = 20
xlabel = "log $I_{CO(1-0),w}$ (K km s$^{-1}$)"
ylabel = "log $I_{CO(2-1),w}$ (K km s$^{-1}$)"
text = "a) log $I_{CO(1-0)}$ vs log $I_{CO(2-1)}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c="rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figw03a_n4321_m0_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 2wb
usecols = [[6], [7]]
keys = ["Tco10", "Tco21"]
limit = [-2.8,0.8]
limit2 = [-2.8,0.8]
bins = 20
xlabel = "log $T_{CO(1-0),w}$ (K)"
ylabel = "log $T_{CO(2-1),w}$ (K)"
c = "rainbow"
text = "b) $T_{CO(1-0),w}$ vs $T_{CO(2-1),w}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figw03b_n4321_m8_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)


"""
### figure 2iw
txtfiles = [dir_data+gal+"_flux_4p0_4p0_iw.txt",
            dir_data+gal+"_flux_4p0_6p0_iw.txt",
            dir_data+gal+"_flux_4p0_8p0_iw.txt",
            dir_data+gal+"_flux_4p0_10p0_iw.txt",
            dir_data+gal+"_flux_4p0_12p0_iw.txt",
            dir_data+gal+"_flux_4p0_14p0_iw.txt",
            dir_data+gal+"_flux_4p0_16p0_iw.txt",
            dir_data+gal+"_flux_4p0_18p0_iw.txt",
            dir_data+gal+"_flux_4p0_20p0_iw.txt"]

# figure 2iwa
usecols = [[2], [3]]
keys = ["Ico10", "Ico21"]
limit = [-1.5,2.49]
limit2 = [-1.5,2.49]
bins = 20
xlabel = "log $I_{CO(1-0),1/w}$ (K km s$^{-1}$)"
ylabel = "log $I_{CO(2-1),1/w}$ (K km s$^{-1}$)"
text = "a) log $I_{CO(1-0),1/w}$ vs log $I_{CO(2-1),1/w}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c="rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figiw03a_n4321_m0_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 2iwb
usecols = [[6], [7]]
keys = ["Tco10", "Tco21"]
limit = [-2.8,0.8]
limit2 = [-2.8,0.8]
bins = 20
xlabel = "log $T_{CO(1-0),1/w}$ (K)"
ylabel = "log $T_{CO(2-1),1/w}$ (K)"
text = "b) log $T_{CO(1-0),1/w}$ vs log $T_{CO(2-1),1/w}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c="rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figiw03b_n4321_m8_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)
"""
