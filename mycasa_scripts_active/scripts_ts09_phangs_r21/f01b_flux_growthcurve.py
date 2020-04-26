import os
import sys
import glob
import matplotlib.cm as cm
import matplotlib.pyplot as plt
plt.ioff()


#####################
### parameters
#####################
dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628", "ngc3627", "ngc4321"]
scales = [44/1.0, 52/1.3, 103/1.4]


#####################
### def
#####################
def get_beam_intensities(images,freq):
    """
    """
    beams = []
    fluxes = []
    for i in range(len(images)):
        # beam
        beamint = images[i].split("_")[-1].split(".")[0]
        beamfloat = float(beamint.replace("p","."))
        beams.append(beamfloat)
        # flux
        flux = imstat(images[i])["sum"][0] # Jy/beam.km/s
        #intensity = 1.222e6 / beamfloat**2 / freq**2 * flux # K.km/s
        fluxes.append(flux)

    l = np.c_[beams, fluxes, fluxes/fluxes[-1]]
    data = l[l[:,0].argsort(), :]

    return data


#####################
### Main Procedure
#####################
### co10
plt.figure(figsize=(10,10))
plt.rcParams["font.size"] = 22
plt.ylim([0,2])
plt.ylabel("Total CO(1-0) Flux Relative To EMPIRE")
plt.xlabel("Spatial Resolution (kpc)")
plt.legend(loc = "lower right")
plt.grid(color="grey")
#
for i in range(len(gals)):
    # get data
    images_co10 = glob.glob(dir_data + gals[i] + "_co10/*co10*.moment0")
    freq = 115.27120 # GHz
    data = get_beam_intensities(images_co10,freq)
    # plot
    plt.plot(data[:,0]*(scales[i]/1000), data[:,2], size=10, lw=5, alpha=0.4, c=cm.brg(i/2.5), label="NGC 0628")



plt.savefig(dir_data + "../eps/missingflux_co10.png", dpi=100)

## co21 plot
plt.figure(figsize=(10,10))
plt.rcParams["font.size"] = 22
i = 0
plt.errorbar(data_co21_n0628[:,0]*(scales[i]/1000),
             data_co21_n0628[:,1]/sd_co21_n0628,
             yerr=data_co21_n0628[:,1]/sd_co21_n0628*np.sqrt(0.1**2+0.08**2),
             lw=5,alpha=0.4,c=cm.brg(i/2.5),label="NGC 0628")
i = 1
plt.errorbar(data_co21_n3627[:,0]*(scales[i]/1000),
             data_co21_n3627[:,1]/sd_co21_n3627,
             yerr=data_co21_n3627[:,1]/sd_co21_n3627*np.sqrt(0.1**2+0.08**2),
             lw=5,alpha=0.4,c=cm.brg(i/2.5),label="NGC 3627")
"""
i = 2
plt.errorbar(data_co21_n4254[:,0]*(scales[i]/1000),
             data_co21_n4254[:,1]/sd_co21_n4254,
             yerr=data_co21_n4254[:,1]/sd_co21_n4254*np.sqrt(0.1**2+0.08**2),
             lw=5,alpha=0.4,c=cm.brg(i/2.5),label="NGC 4254")
"""
i = 3
plt.errorbar(data_co21_n4321[:,0]*(scales[i]/1000),
             data_co21_n4321[:,1]/sd_co21_n4321,
             yerr=data_co21_n4321[:,1]/sd_co21_n4321*np.sqrt(0.1**2+0.08**2),
             lw=5,alpha=0.4,c=cm.brg(i/2.5),label="NGC 4321")
plt.ylim([0,2])
plt.ylabel("Total CO(2-1) Flux Relative To HERACLES")
plt.xlabel("Spatial Resolution (kpc)")
plt.legend(loc = "lower right")
plt.grid(color="grey")
plt.savefig(dir_data + "../eps/missingflux_co21.png", dpi=100)

## R21 plot
plt.figure(figsize=(10,10))
plt.rcParams["font.size"] = 22
i = 0
y = (data_co21_n0628[:,1]/data_co10_n0628[:,1])/(sd_co21_n0628/sd_co10_n0628)
plt.errorbar(data_co21_n0628[:,0]*(scales[i]/1000),y,
             yerr=y * np.sqrt(0.05**2 + 0.08**2 + 0.1**2 + 0.08**2),
             lw=5,alpha=0.4,c=cm.brg(i/2.5),label="NGC 0628")
i = 1
y = (data_co21_n3627[:,1]/data_co10_n3627[:,1])/(sd_co21_n3627/sd_co10_n3627)
plt.errorbar(data_co21_n3627[:,0]*(scales[i]/1000),y,
             yerr=y * np.sqrt(0.15**2 + 0.08**2 + 0.1**2 + 0.08**2),
             lw=5,alpha=0.4,c=cm.brg(i/2.5),label="NGC 3627")
"""
i = 2
y = (data_co21_n4254[:,1]/data_co10_n4254[:,1])/(sd_co21_n4254/sd_co10_n4254)
plt.errorbar(data_co21_n4254[:,0]*(scales[i]/1000),y,
             yerr=y * np.sqrt(0.10**2 + 0.08**2 + 0.1**2 + 0.08**2),
             lw=5,alpha=0.4,c=cm.brg(i/2.5),label="NGC 4254")
"""
i = 3
y = (data_co21_n4321[:,1]/data_co10_n4321[:,1])/(sd_co21_n4321/sd_co10_n4321)
plt.errorbar(data_co21_n4321[:,0]*(scales[i]/1000),y,
             yerr=y * np.sqrt(0.05**2 + 0.08**2 + 0.1**2 + 0.08**2),
             lw=5,alpha=0.4,c=cm.brg(i/2.5),label="NGC 4321")
plt.ylim([0,2])
plt.ylabel("Total $R_{21}$ Relative To HERACLES/EMPIRE Ratio")
plt.xlabel("Spatial Resolution (kpc)")
plt.legend(loc = "lower right")
plt.grid(color="grey")
plt.savefig(dir_data + "../eps/missingflux_r21.png", dpi=100)
