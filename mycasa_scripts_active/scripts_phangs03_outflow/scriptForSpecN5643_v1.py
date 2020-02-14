import os
import sys
import glob
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
plt.ioff()

# import CASA
from taskinit import *
from imval import imval


#####################
### define functions
#####################
def easy_imval(imagename,region_file,savefile):
    """
    extract 1D spectrum using an apertuer defined
    by region_file. The region_file must be casa
    region format.
    """
    value = imval(imagename = imagename,
                  region = region_file)

    value_masked = value["data"] * value["mask"]
    data = value_masked.mean(axis = (0, 1))

    freq_obs = value['coords'][0,0,:,2] #Hz
    freq_rest = 230.53800 * 10 ** 9 # Hz
    c = 299792.458 # km/s
    vel = c * (freq_rest - freq_obs) / freq_rest
    product = np.c_[vel, value_masked.sum(axis = (0, 1))]

    np.savetxt(savefile, product, delimiter = " ")


def write_region(region_file,ra_dgr,dec_dgr,aperture):
    """
    create casa region format
    https://casaguides.nrao.edu/index.php/CASA_Region_Format
    """
    f = open(region_file, "w")
    f.write("#CRTFv0\n")
    f.write("global coord=J2000\n")
    f.write("\n")
    f.write("circle[[" + str(round(ra_dgr, 5)) + "deg, " \
            + str(round(dec_dgr, 7)) + "deg], " \
            + str(round(aperture/2., 3)) + "arcsec]")
    f.write("")
    f.close()


#####################
### Main Procedure
#####################
# specify data information
gal = "../data_v0/ngc5643_12m+7m+tp_co21_pbcorr_round_k.image"
ra_hms = "14h32m40.639s" # center right ascension
dec_dms = "-44d10m26.796s" # center declination


# create aperture for the central 5arcsec
region_center = "ngc5643_5arcsec.txt"
aperture = 5.0 # diameter in arcsec
c = SkyCoord(ra_hms, dec_dms)
ra_dgr = c.ra.degree
dec_dgr = c.dec.degree
write_region(region_center,ra_dgr,dec_dgr,aperture)


# create aperture for the central 100arcsec
region_galaxy = "ngc5643_100arcsec.txt"
aperture = 100.0 # diameter in arcsec
write_region(region_galaxy,ra_dgr,dec_dgr,aperture)


# do specsmooth
gal_tmp_ = gal
gal = gal_tmp_.replace(".image",".specsmooth")
os.system("rm -rf "+gal)
specsmooth(imagename=gal_tmp_,
           outfile=gal,
           width=5)

# do imval
spec_center = region_center.replace(".txt","_spectrum.txt")
easy_imval(gal, region_center, spec_center)
spec_galaxy = region_galaxy.replace(".txt","_spectrum.txt")
easy_imval(gal, region_galaxy, spec_galaxy)


# plot
data_center = np.loadtxt(spec_center)
plt.figure()
plt.plot(data_center[:,0],
         data_center[:,1] / max(data_center[:,1]),
         color = "purple",
         lw = 2,
         label = "central 5 arcsec")
data_galaxy = np.loadtxt(spec_galaxy)

plt.plot(data_galaxy[:,0],
         data_galaxy[:,1] / max(data_galaxy[:,1]),
         color = "grey",
         lw = 2,
         label = "central 100 arcsec")

plt.plot([min(data_center[:,0]),max(data_center[:,0])],
         [0,0],
         "black",
         linestyle = "dashed")

plt.title("NGC 5643 CO(2-1) Spectra")
plt.ylim([-0.1,1.1])
plt.xlabel("Velocity (km s$^{-1}$)")
plt.ylabel("Normalized Integrated Intensity")
plt.legend()
plt.savefig("ngc5643_specsmooth.png")

# zoom plot
plt.figure()

data_center = np.loadtxt(spec_center)
data_y_center = data_center[:,1] / max(data_center[:,1])
plt.plot(data_center[:,0],
         data_center[:,1] / max(data_center[:,1]),
         color = "purple",
         lw = 2,
         label = "central 5 arcsec") 

data_galaxy = np.loadtxt(spec_galaxy)
data_y_galaxy = data_galaxy[:,1] / max(data_galaxy[:,1])
plt.plot(data_galaxy[:,0],
         data_galaxy[:,1] / max(data_galaxy[:,1]),
         color = "grey", 
         lw = 2,
         label = "central 100 arcsec")

plt.plot([min(data_center[:,0]),max(data_center[:,0])],
         [0,0],  
         "black",
         linestyle = "dashed")

plt.plot(data_galaxy[:,0],
         data_y_center - data_y_galaxy,
         "red",
         lw = 4,
         label = "difference",
         alpha=0.4)

plt.title("NGC 5643 CO(2-1) Zoomed Spectra")
plt.ylim([-0.02,0.2])
plt.xlabel("Velocity (km s$^{-1}$)")
plt.ylabel("Normalized Integrated Intensity")
plt.legend()
plt.savefig("ngc5643_specsmooth_zoom.png")




