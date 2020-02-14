import glob
sys.path.append(os.getcwd())
import scripts_phangs_r21_plot as r21_plot



### setup
gal = "ngc0628" # "ngc4321"
dir_data = "../../phangs/co_ratio/"+gal+"_co/"
xlog=True
ylog=True



### figure 3
txtfiles = [dir_data+gal+"_flux_4p0_20p0_no.txt",
            dir_data+gal+"_flux_6p0_20p0_no.txt",
            dir_data+gal+"_flux_8p0_20p0_no.txt",
            dir_data+gal+"_flux_10p0_20p0_no.txt",
            dir_data+gal+"_flux_12p0_20p0_no.txt",
            dir_data+gal+"_flux_14p0_20p0_no.txt",
            dir_data+gal+"_flux_16p0_20p0_no.txt",
            dir_data+gal+"_flux_18p0_20p0_no.txt",
            dir_data+gal+"_flux_20p0_20p0_no.txt"]

# figure 3a
usecols = [[2], [3]]
keys = ["Ico10", "Ico21"]
limit = [-1.9,1.99]
limit2 = [-1.9,1.99]
bins = 20
xlabel = "log $I_{CO(1-0)}$ (K km s$^{-1}$)"
ylabel = "log $I_{CO(2-1)}$ (K km s$^{-1}$)"
text = "a) log $I_{CO(1-0)}$ vs log $I_{CO(2-1)}$ with \n    varying beam size"
title = "Beam Size (Aperture Beam = 20\")"
c = "gnuplot"
variable="beam"
savefig = "/Users/saito/data/phangs/co_ratio/eps/fig04a_n4321_m0_bm.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 3b
usecols = [[6], [7]]
keys = ["Tco10", "Tco21"]
limit = [-3.3,0.5]
limit2 = [-3.3,0.5]
bins = 20
xlabel = "log $T_{CO(1-0)}$ (K)"
ylabel = "log $T_{CO(2-1)}$ (K)"
text = "b) log $T_{CO(1-0)}$ vs log $T_{CO(2-1)}$ with \n    varying beam size"
title = "Beam Size (Aperture Beam = 20\")"
c = "gnuplot"
variable="beam"
savefig = "/Users/saito/data/phangs/co_ratio/eps/fig04b_n4321_m8_bm.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)


"""
### figure 3w
txtfiles = [dir_data + "ngc4321_flux_4p0_20p0_w.txt",
            dir_data + "ngc4321_flux_6p0_20p0_w.txt",
            dir_data + "ngc4321_flux_8p0_20p0_w.txt",
            dir_data + "ngc4321_flux_10p0_20p0_w.txt",
            dir_data + "ngc4321_flux_12p0_20p0_w.txt",
            dir_data + "ngc4321_flux_14p0_20p0_w.txt",
            dir_data + "ngc4321_flux_16p0_20p0_w.txt",
            dir_data + "ngc4321_flux_18p0_20p0_w.txt",
            dir_data + "ngc4321_flux_20p0_20p0_w.txt"]

# figure 3wa
usecols = [[2], [3]]
keys = ["Ico10", "Ico21"]
limit = [-1.9,1.99]
limit2 = [-1.9,1.99]
bins = 20
xlabel = "log $I_{CO(1-0),w}$ (K km s$^{-1}$)"
ylabel = "log $I_{CO(2-1),w}$ (K km s$^{-1}$)"
text = "a) log $I_{CO(1-0),w}$ vs log $I_{CO(2-1),w}$ with \n    varying beam size"
title = "Beam Size (Aperture Beam = 20\")"
c = "gnuplot"
variable="beam"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figw04a_n4321_m0_bm.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 3wb
usecols = [[6], [7]]
keys = ["Tco10", "Tco21"]
limit = [-3.3,0.5]
limit2 = [-3.3,0.5]
bins = 20
xlabel = "log $T_{CO(1-0),w}$ (K)"
ylabel = "log $T_{CO(2-1),w}$ (K)"
text = "b) log $T_{CO(1-0),w}$ vs log $T_{CO(2-1),w}$ with \n    varying beam size"
title = "Beam Size (Aperture Beam = 20\")"
c = "gnuplot"
variable="beam"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figw04b_n4321_m8_bm.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)



### figure 3w
txtfiles = [dir_data + "ngc4321_flux_4p0_20p0_iw.txt",
            dir_data + "ngc4321_flux_6p0_20p0_iw.txt",
            dir_data + "ngc4321_flux_8p0_20p0_iw.txt",
            dir_data + "ngc4321_flux_10p0_20p0_iw.txt",
            dir_data + "ngc4321_flux_12p0_20p0_iw.txt",
            dir_data + "ngc4321_flux_14p0_20p0_iw.txt",
            dir_data + "ngc4321_flux_16p0_20p0_iw.txt",
            dir_data + "ngc4321_flux_18p0_20p0_iw.txt",
            dir_data + "ngc4321_flux_20p0_20p0_iw.txt"]

# figure 3iwa
usecols = [[2], [3]]
keys = ["Ico10", "Ico21"]
limit = [-1.9,1.99]
limit2 = [-1.9,1.99]
bins = 20
xlabel = "log $I_{CO(1-0),1/w}$ (K km s$^{-1}$)"
ylabel = "log $I_{CO(2-1),1/w}$ (K km s$^{-1}$)"
text = "a) log $I_{CO(1-0),1/w}$ vs log $I_{CO(2-1),1/w}$ with \n    varying beam size"
title = "Beam Size (Aperture Beam = 20\")"
c = "gnuplot"
variable="beam"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figiw04a_n4321_m0_bm.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 3wb
usecols = [[6], [7]]
keys = ["Tco10", "Tco21"]
limit = [-3.3,0.5]
limit2 = [-3.3,0.5]
bins = 20
xlabel = "log $T_{CO(1-0),1/w}$ (K)"
ylabel = "log $T_{CO(2-1),1/w}$ (K)"
text = "b) log $T_{CO(1-0),1/w}$ vs log $T_{CO(2-1),1/w}$ with \n    varying beam size"
title = "Beam Size (Aperture Beam = 20\")"
c = "gnuplot"
variable="beam"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figiw04b_n4321_m8_bm.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)
"""

