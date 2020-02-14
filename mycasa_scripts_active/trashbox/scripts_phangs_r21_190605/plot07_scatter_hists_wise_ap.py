import glob
sys.path.append(os.getcwd())
import scripts_phangs_r21_plot as r21_plot


### setup
dir_data = "../../phangs/co_ratio/ngc4321_wise/"
xlog=True
ylog=True # False


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

usecols = [[8], [2,3]]
keys = ["W1", "R21"]
limit = [-4.0,-1.49]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 20
xlabel = "log W1 (Jy beam$^{-1}$)"
ylabel = "log $R_{21}$"
text = "a) W1 vs. $R_{21}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/fig07a_n4321_w1_v_r21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 4b
usecols = [[9], [2,3]]
keys = ["W2", "R21"]
limit = [-4.0,-1.49]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 20
xlabel = "log W2 (Jy beam$^{-1}$)"
ylabel = "log $R_{21}$"
text = "b) W2 vs. $R_{21}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/fig07b_n4321_w2_v_r21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 4c
usecols = [[10], [2,3]]
keys = ["W3", "R21"]
limit = [-3.5,-0.99]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 20
xlabel = "log W3 (Jy beam$^{-1}$)"
ylabel = "log $R_{21}$"
text = "c) W3 vs. $R_{21}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/fig07c_n4321_w3_v_r21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)



### figure 4w
# figure 4aw
txtfiles = [dir_data + "ngc4321_flux_8p0_8p0_w.txt",
            dir_data + "ngc4321_flux_8p0_10p0_w.txt",
            dir_data + "ngc4321_flux_8p0_12p0_w.txt",
            dir_data + "ngc4321_flux_8p0_14p0_w.txt",
            dir_data + "ngc4321_flux_8p0_16p0_w.txt",
            dir_data + "ngc4321_flux_8p0_18p0_w.txt",
            dir_data + "ngc4321_flux_8p0_20p0_w.txt",
            dir_data + "ngc4321_flux_8p0_22p0_w.txt",
            dir_data + "ngc4321_flux_8p0_24p0_w.txt"]

usecols = [[8], [2,3]]
keys = ["W1", "R21"]
limit = [-4.0,-1.49]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 20
xlabel = "log W1$_w$ (Jy beam$^{-1}$)"
ylabel = "log $R_{21,w}$"
text = "a) W1$_w$ vs. $R_{21,w}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figw07a_n4321_w1_v_r21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 4bw
usecols = [[9], [2,3]]
keys = ["W2", "R21"]
limit = [-4.0,-1.49]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 20
xlabel = "log W2$_w$ (Jy beam$^{-1}$)"
ylabel = "log $R_{21,w}$"
text = "b) W2$_w$ vs. $R_{21,w}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figw07b_n4321_w2_v_r21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 4cw
usecols = [[10], [2,3]]
keys = ["W3", "R21"]
limit = [-3.5,-0.99]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 20
xlabel = "log W3$_w$ (Jy beam$^{-1}$)"
ylabel = "log $R_{21,w}$"
text = "c) W3$_w$ vs. $R_{21,w}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figw07c_n4321_w3_v_r21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)




### figure 4iw
# figure 4aiw
txtfiles = [dir_data + "ngc4321_flux_8p0_8p0_iw.txt",
            dir_data + "ngc4321_flux_8p0_10p0_iw.txt",
            dir_data + "ngc4321_flux_8p0_12p0_iw.txt",
            dir_data + "ngc4321_flux_8p0_14p0_iw.txt",
            dir_data + "ngc4321_flux_8p0_16p0_iw.txt",
            dir_data + "ngc4321_flux_8p0_18p0_iw.txt",
            dir_data + "ngc4321_flux_8p0_20p0_iw.txt",
            dir_data + "ngc4321_flux_8p0_22p0_iw.txt",
            dir_data + "ngc4321_flux_8p0_24p0_iw.txt"]

usecols = [[8], [2,3]]
keys = ["W1", "R21"]
limit = [-4.0,-1.49]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 20
xlabel = "log W1$_{1/w}$ (Jy beam$^{-1}$)"
ylabel = "log $R_{21,1/w}$"
text = "a) W1$_{1/w}$ vs. $R_{21,1/w}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figiw07a_n4321_w1_v_r21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 4biw
usecols = [[9], [2,3]]
keys = ["W2", "R21"]
limit = [-4.0,-1.49]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 20
xlabel = "log W2$_{1/w}$ (Jy beam$^{-1}$)"
ylabel = "log $R_{21,1/w}$"
text = "b) W2$_{1/w}$ vs. $R_{21,1/w}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figiw07b_n4321_w2_v_r21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)

# figure 4ciw
usecols = [[10], [2,3]]
keys = ["W3", "R21"]
limit = [-3.5,-0.99]
limit2 = [-1.3,0.7] # [0.0,2.0]
bins = 20
xlabel = "log W3$_{1/w}$ (Jy beam$^{-1}$)"
ylabel = "log $R_{21,1/w}$"
text = "c) W3$_{1/w}$ vs. $R_{21,1/w}$ with \n    varying aperture size"
title = "Aperture Size (Fixed Beam = 4\")"
c = "rainbow"
variable="aperture"
savefig = "/Users/saito/data/phangs/co_ratio/eps/figiw07c_n4321_w3_v_r21_ap.png"

r21_plot.scatter_hists(txtfiles, usecols,keys,limit,limit2,bins,xlabel,
                       ylabel,text,title,xlog,ylog,c,variable,savefig)
