import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.ioff()

# gal caf_fid cdf_fid 7m_fid circ_diameter model_flux caf_flux cdf_flux 7m_flux

txtname = "phangs_fidelity.txt"
data = np.loadtxt(txtname,dtype="S10")
galname = data[:,0]

caf_fid = data[:,1].astype(np.float32)
cdf_fid = data[:,2].astype(np.float32)
aca_fid = data[:,3].astype(np.float32)
cdaf_fid = data[:,9].astype(np.float32)
cbf_fid = data[:,11].astype(np.float32)

circ_diameter = data[:,4].astype(np.float32)

model_flux = data[:,5].astype(np.float32)
caf_flux = data[:,6].astype(np.float32)
cdf_flux = data[:,7].astype(np.float32)
aca_flux = data[:,8].astype(np.float32)
cdaf_flux = data[:,10].astype(np.float32)
cbf_flux = data[:,12].astype(np.float32)

model_max = data[:,13].astype(np.float32)
caf_max = data[:,14].astype(np.float32)
cdf_max = data[:,15].astype(np.float32)
aca_max = data[:,17].astype(np.float32)
cdaf_max = data[:,16].astype(np.float32)
cbf_max = data[:,18].astype(np.float32)

diff_caf = (model_flux - caf_flux) / model_flux
diff_cdf = (model_flux - cdf_flux) / model_flux
diff_cdaf = (model_flux - cdaf_flux) / model_flux
diff_aca = (model_flux - aca_flux) / model_flux
diff_cbf = (model_flux - cbf_flux) / model_flux

diff_max_caf = (model_max - caf_max) / model_max
diff_max_cdf = (model_max - cdf_max) / model_max
diff_max_cdaf = (model_max - cdaf_max) / model_max
diff_max_aca = (model_max - aca_max) / model_max
diff_max_cbf = (model_max - cbf_max) / model_max

fig = plt.figure(figsize=(12,4))
plt.rcParams["font.size"] = 14

aca_med = np.round(np.median(aca_fid),1)
caf_med = np.round(np.median(caf_fid),1)
cdf_med = np.round(np.median(cdf_fid),1)
cdaf_med = np.round(np.median(cdaf_fid),1)
cbf_med = np.round(np.median(cbf_fid),1)

aca_disp = np.round(np.std(aca_fid[circ_diameter>30]),1)
caf_disp = np.round(np.std(caf_fid[circ_diameter>30]),1)
cdf_disp = np.round(np.std(cdf_fid[circ_diameter>30]),1)
cdaf_disp = np.round(np.std(cdaf_fid[circ_diameter>30]),1)
cbf_disp = np.round(np.std(cbf_fid[circ_diameter>30]),1)

plt.scatter(circ_diameter,
            aca_fid,
            color = "black",
            s = 50,
            alpha = 0.4,
            label = "7m-only ("+str(aca_med)+"+/-"+str(aca_disp)+")")

plt.scatter(circ_diameter,
            cbf_fid,
            color = "orange",
            s = 50,
            alpha = 0.4,
            label = "tp2vis ("+str(cbf_med)+"+/-"+str(cbf_disp)+")")

plt.scatter(circ_diameter,
            cdf_fid,
            color = "green",
            s = 50,
            alpha = 0.4,
            label = "TPmodel ("+str(cdf_med)+"+/-"+str(cdf_disp)+")")

plt.scatter(circ_diameter,
            cdaf_fid,
            color = "magenta",
            s = 50,
            alpha = 0.4,
            label = "TPmodel + feather ("+str(cdaf_med)+"+/-"+str(cdaf_disp)+")")

plt.scatter(circ_diameter,
            caf_fid,
            color = "blue",
            s = 50,
            alpha = 0.4,
            label = "feather ("+str(caf_med)+"+/-"+str(caf_disp)+")")

plt.plot([0,300],[aca_med,aca_med],"--",c="black",lw=2)
plt.plot([0,300],[cbf_med,cbf_med],"--",c="orange",lw=2)
plt.plot([0,300],[cdf_med,cdf_med],"--",c="green",lw=2)
plt.plot([0,300],[cdaf_med,cdaf_med],"--",c="magenta",lw=2)
plt.plot([0,300],[caf_med,caf_med],"--",c="blue",lw=2)


plt.legend()
plt.xlabel("CO(2-1) Size Diamter (arcsec)")
plt.ylabel("Fidelity Median")
plt.xlim([0,300])
plt.ylim([0,55])
#plt.yscale("log")
plt.savefig("fig_fidelity_vs_circ_diameter.png")

# plot 2
fig = plt.figure(figsize=(12,4))
plt.rcParams["font.size"] = 14

aca_med = np.round(np.median(aca_fid),1)
caf_med = np.round(np.median(caf_fid),1)
cdf_med = np.round(np.median(cdf_fid),1)
cdaf_med = np.round(np.median(cdaf_fid),1)
cbf_med = np.round(np.median(cbf_fid),1)

plt.scatter(model_flux / (np.pi*circ_diameter**2),
            aca_fid,
            color = "black",
            s = 50,
            alpha = 0.4,
            label = "7m-only ("+str(aca_med)+")")

plt.scatter(model_flux / (np.pi*circ_diameter**2),
            cbf_fid,
            color = "orange",
            s = 50,
            alpha = 0.4,
            label = "tp2vis ("+str(cbf_med)+")")

plt.scatter(model_flux / (np.pi*circ_diameter**2),
            cdf_fid,
            color = "green",
            s = 50,
            alpha = 0.4,
            label = "TPmodel ("+str(cdf_med)+")")

plt.scatter(model_flux / (np.pi*circ_diameter**2),
            cdaf_fid,
            color = "magenta",
            s = 50,
            alpha = 0.4,
            label = "TPmodel + feather ("+str(cdaf_med)+")")

plt.scatter(model_flux / (np.pi*circ_diameter**2),
            caf_fid,
            color = cm.rainbow(1./4.),
            s = 50,
            alpha = 0.4,
            label = "feather ("+str(caf_med)+")")

plt.plot([0.0005,0.0045],[aca_med,aca_med],"--",c="black",lw=2)
plt.plot([0.0005,0.0045],[cbf_med,cbf_med],"--",c="orange",lw=2)
plt.plot([0.0005,0.0045],[cdf_med,cdf_med],"--",c="green",lw=2)
plt.plot([0.0005,0.0045],[cdaf_med,cdaf_med],"--",c="magenta",lw=2)
plt.plot([0.0005,0.0045],[caf_med,caf_med],"--",c="blue",lw=2)

#plt.legend()
plt.xlabel("CO(2-1) Model Flux Density (Jy/arcsec^2)")
plt.ylabel("Fidelity Median")
plt.xlim([0.0005,0.0045])
plt.ylim([0,55])
#plt.yscale("log")
plt.savefig("fig_fidelity_vs_flux.png")

# plot 3
fig = plt.figure(figsize=(12,4))
plt.rcParams["font.size"] = 14

aca_med = np.round(np.median(diff_aca),2)
caf_med = np.round(np.median(diff_caf),2)
cdf_med = np.round(np.median(diff_cdf),2)
cdaf_med = np.round(np.median(diff_cdaf),2)
cbf_med = np.round(np.median(diff_cbf),2)

aca_disp = np.round(np.std(diff_aca[circ_diameter>30]),2)
caf_disp = np.round(np.std(diff_caf[circ_diameter>30]),2)
cdf_disp = np.round(np.std(diff_cdf[circ_diameter>30]),2)
cdaf_disp = np.round(np.std(diff_cdaf[circ_diameter>30]),2)
cbf_disp = np.round(np.std(diff_cbf[circ_diameter>30]),2)

plt.scatter(circ_diameter,
            diff_aca,
            color = "black",
            s = 50,
            alpha = 0.4,
            label = "7m-only ("+str(aca_med)+"+/-"+str(aca_disp)+")")

plt.scatter(circ_diameter,
            diff_cbf,
            color = "orange",
            s = 50,
            alpha = 0.4,
            label = "tp2vis ("+str(cbf_med)+"+/-"+str(cbf_disp)+")")

plt.scatter(circ_diameter,
            diff_cdf,
            color = "green",
            s = 50,
            alpha = 0.4,
            label = "TPmodel ("+str(cdf_med)+"+/-"+str(cdf_disp)+")")

plt.scatter(circ_diameter,
            diff_cdaf,
            color = "magenta",
            s = 50,
            alpha = 0.4,
            label = "TPmodel + feather ("+str(cdaf_med)+"+/-"+str(cdaf_disp)+")")

plt.scatter(circ_diameter,
            diff_caf,
            color = "blue",
            s = 50,
            alpha = 0.4,
            label = "feather ("+str(caf_med)+"+/-"+str(caf_disp)+")")

plt.plot([0,1000],[aca_med,aca_med],"--",c="black",lw=2)
plt.plot([0,1000],[cbf_med,cbf_med],"--",c="orange",lw=2)
plt.plot([0,1000],[cdf_med,cdf_med],"--",c="green",lw=2)
plt.plot([0,1000],[cdaf_med,cdaf_med],"--",c="magenta",lw=2)
plt.plot([0,1000],[caf_med,caf_med],"--",c="blue",lw=2)

plt.legend()
plt.xlabel("CO(2-1) Size Diamter (arcsec)")
plt.ylabel("Flux Difference from Model")
plt.xlim([0,300])
plt.ylim([-0.3,1.1])
#plt.yscale("log")
plt.savefig("fig_fidelity_vs_diff.png")


# plot 4
fig = plt.figure(figsize=(12,4))
plt.rcParams["font.size"] = 14

aca_med = np.round(np.median(diff_max_aca),2)
caf_med = np.round(np.median(diff_max_caf),2)
cdf_med = np.round(np.median(diff_max_cdf),2)
cdaf_med = np.round(np.median(diff_max_cdaf),2)
cbf_med = np.round(np.median(diff_max_cbf),2)

aca_disp = np.round(np.std(diff_max_aca[circ_diameter>30]),2)
caf_disp = np.round(np.std(diff_max_caf[circ_diameter>30]),2)
cdf_disp = np.round(np.std(diff_max_cdf[circ_diameter>30]),2)
cdaf_disp = np.round(np.std(diff_max_cdaf[circ_diameter>30]),2)
cbf_disp = np.round(np.std(diff_max_cbf[circ_diameter>30]),2)

plt.scatter(circ_diameter,
            diff_max_aca,
            color = "black",
            s = 50,
            alpha = 0.4,
            label = "7m-only ("+str(aca_med)+"+/-"+str(aca_disp)+")")

plt.scatter(circ_diameter,
            diff_max_cbf,
            color = "orange",
            s = 50,
            alpha = 0.4,
            label = "tp2vis ("+str(cbf_med)+"+/-"+str(cbf_disp)+")")

plt.scatter(circ_diameter,
            diff_max_cdf,
            color = "green",
            s = 50,
            alpha = 0.4,
            label = "TPmodel ("+str(cdf_med)+"+/-"+str(cdf_disp)+")")

plt.scatter(circ_diameter,
            diff_max_cdaf,
            color = "magenta",
            s = 50,
            alpha = 0.4,
            label = "TPmodel + feather ("+str(cdaf_med)+"+/-"+str(cdaf_disp)+")")

plt.scatter(circ_diameter,
            diff_max_caf,
            color = "blue",
            s = 50,
            alpha = 0.4,
            label = "feather ("+str(caf_med)+"+/-"+str(caf_disp)+")")

plt.plot([0,1000],[aca_med,aca_med],"--",c="black",lw=2)
plt.plot([0,1000],[cbf_med,cbf_med],"--",c="orange",lw=2)
plt.plot([0,1000],[cdf_med,cdf_med],"--",c="green",lw=2)
plt.plot([0,1000],[cdaf_med,cdaf_med],"--",c="magenta",lw=2)
plt.plot([0,1000],[caf_med,caf_med],"--",c="blue",lw=2)

plt.legend()
plt.xlabel("CO(2-1) Size Diamter (arcsec)")
plt.ylabel("Peak Flux Difference from Model")
plt.xlim([0,300])
plt.ylim([-0.3,1.1])
#plt.yscale("log")
plt.savefig("fig_fidelity_vs_diff_max.png")

