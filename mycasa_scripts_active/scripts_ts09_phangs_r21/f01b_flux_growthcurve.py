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

def get_beam_ratios(co10images,co21images):
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
        co10flux = imstat(co10images[i])["sum"][0] # Jy/beam.km/s
        co21flux = imstat(co21images[i])["sum"][0] # Jy/beam.km/s
        ratio.append(co21flux/co10flux/4.)

    l = np.c_[beams, ratio, ratio/ratio[-1]]
    data = l[l[:,0].argsort(), :]

    return data


#####################
### Main Procedure
#####################
### co10
plt.figure(figsize=(10,10))
plt.rcParams["font.size"] = 22
plt.ylim([0.0,1.2])
plt.ylabel("CO(1-0) Flux Recovery")
plt.xlabel("Spatial Resolution (kpc)")
plt.legend(loc = "lower right")
plt.grid(color="grey")
#
for i in range(len(gals)):
    # get data
    galanme = gals[i].replace("ngc","NGC ")
    images_co10 = glob.glob(dir_data + gals[i] + "_co10/co10*.moment0")
    freq = 115.27120 # GHz
    data = get_beam_intensities(images_co10,freq)
    # plot
    plt.plot(data[:,0]*(scales[i]/1000), data[:,2], "o", markersize=15, markeredgewidth=0, lw=0, c=cm.brg(i/2.5), label=galanme)
    plt.plot(data[:,0]*(scales[i]/1000), data[:,2], "-", lw=5, c=cm.brg(i/2.5), alpha=0.5)
    #
plt.legend(loc="lower right")
plt.savefig(dir_data + "eps/missingflux_co10.png", dpi=100)


### co21
plt.figure(figsize=(10,10))
plt.rcParams["font.size"] = 22
plt.ylim([0.0,1.2])
plt.ylabel("CO(2-1) Flux Recovery")
plt.xlabel("Spatial Resolution (kpc)")
plt.legend(loc = "lower right")
plt.grid(color="grey")
#
for i in range(len(gals)):
    # get data
    galanme = gals[i].replace("ngc","NGC ")
    images_co21 = glob.glob(dir_data + gals[i] + "_co21/co21*.moment0")
    freq = 230.53800 # GHz
    data = get_beam_intensities(images_co21,freq)
    # plot
    plt.plot(data[:,0]*(scales[i]/1000), data[:,2], "o", markersize=15, markeredgewidth=0, lw=0, c=cm.brg(i/2.5), label=galanme)
    plt.plot(data[:,0]*(scales[i]/1000), data[:,2], "-", lw=5, c=cm.brg(i/2.5), alpha=0.5)
    #
plt.legend(loc="lower right")
plt.savefig(dir_data + "eps/missingflux_co21.png", dpi=100)


### r21
plt.figure(figsize=(10,10))
plt.rcParams["font.size"] = 22
plt.ylim([0.0,1.2])
plt.ylabel("CO(2-1) Flux Recovery")
plt.xlabel("Spatial Resolution (kpc)")
plt.legend(loc = "lower right")
plt.grid(color="grey")
#
for i in range(len(gals)):
    # get data
    galanme = gals[i].replace("ngc","NGC ")
    images_co10 = glob.glob(dir_data + gals[i] + "_co10/co10*.moment0")
    images_co21 = glob.glob(dir_data + gals[i] + "_co21/co21*.moment0")
    data = get_beam_ratios(images_co10,images_co21)
    # plot
    plt.plot(data[:,0]*(scales[i]/1000), data[:,2], "o", markersize=15, markeredgewidth=0, lw=0, c=cm.brg(i/2.5), label=galanme)
    plt.plot(data[:,0]*(scales[i]/1000), data[:,2], "-", lw=5, c=cm.brg(i/2.5), alpha=0.5)
    #
plt.legend(loc="lower right")
plt.savefig(dir_data + "eps/missingflux_co21.png", dpi=100)


