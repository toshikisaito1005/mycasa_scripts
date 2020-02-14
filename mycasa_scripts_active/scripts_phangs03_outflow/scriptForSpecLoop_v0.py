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


def easy_plotter(spec_peak, spec_center, spec_galaxy,
                 gal_name, ylim, suffix):
    """
    plot spectra toward central 10 arcsec and 100 arcsec regions.
    """
    plt.figure()

    data_galaxy = np.loadtxt(spec_galaxy)
    plt.plot(data_galaxy[:,0],
             data_galaxy[:,1] / max(data_galaxy[:,1]),
             color = "grey",
             lw = 1,
             label = "central 100 arcsec")

    data_center = np.loadtxt(spec_center)
    plt.plot(data_center[:,0],
             data_center[:,1] / max(data_center[:,1]),
             color = "pink",
             lw = 1, 
             label = "central 10 arcsec")

    data_peak = np.loadtxt(spec_peak)
    plt.plot(data_peak[:,0],
             data_peak[:,1] / max(data_peak[:,1]),
             color = "blue",
             lw = 1, 
             label = "central 2 arcsec")

    plt.plot([min(data_center[:,0]),max(data_center[:,0])],
             [0,0],
             "grey",
             linestyle = "dashed")

    plt.title(gal_name +" CO(2-1) Spectra")
    plt.ylim(ylim)
    plt.xlabel("Velocity (km s$^{-1}$)")
    plt.ylabel("Normalized Integrated Intensity")
    plt.legend()
    plt.savefig(spec_center.split("_")[0] + "_" + suffix + ".png")



#####################
### Main Procedure
#####################
### specify datacubes
gals_tmp0 = glob.glob("../data_v0/*12m+7m+tp*.image")
gals_tmp1 = [s for s in gals_tmp0 if not "north" in s]
gals_tmp2 = [s for s in gals_tmp1 if not "south" in s]
gals_tmp3 = [s for s in gals_tmp2 if not "_1_" in s]
gals_tmp4 = [s for s in gals_tmp3 if not "_2_" in s]
gals = [s for s in gals_tmp4 if not "_3_" in s]


### import coordinate information
dir_phangs_tmp = "/data/beegfs/astro-storage/groups/schinnerer/PHANGS/"
dir_phangs = dir_phangs_tmp + "ALMA/By_Project/imaging/scripts/"
pos_center_tmp0 = np.loadtxt(dir_phangs + "mosaic_definitions.txt", dtype = "S30")
pos_center_tmp1 = np.loadtxt(dir_phangs + "multipart_fields.txt", dtype = "S30")
pos_center_tmp2 = np.r_[pos_center_tmp0,pos_center_tmp1[:,0:5]]

delete_list = []
for i in range(len(pos_center_tmp2)):
    if "_" in pos_center_tmp2[i][0]:
        delete_list.append(i)

pos_center = np.delete(pos_center_tmp2, delete_list, axis=0)


### extract spectra
os.system("rm -rf casa_region/")
os.system("mkdir casa_region/")
done = glob.glob("products/")
if not done:
    os.system("mkdir products/")

for i in range(len(gals)):
    # get ra and dec of the center position
    gal_name = gals[i].split("_12m")[0].split("/")[-1]
    gal_info = pos_center[np.where(pos_center[:,0] == gal_name)[0][0]]
    print("# processing " + gal_name)

    ra_hms, dec_dms = gal_info[1], gal_info[2]
    if not "h" in ra_hms:
        c = SkyCoord(ra_hms, dec_dms, unit="deg")
    else:
        c = SkyCoord(ra_hms, dec_dms)

    ra_dgr = c.ra.degree
    dec_dgr = c.dec.degree

    # create aperture for the central 2arcsec
    peak_output = "casa_region/" + gal_name + "_2arcsec.txt"
    aperture = 2.0 # diameter in arcsec
    write_region(peak_output,ra_dgr,dec_dgr,aperture)

    # create aperture for the central 10arcsec
    center_output = "casa_region/" + gal_name + "_10arcsec.txt"
    aperture = 10.0 # diameter in arcsec
    write_region(center_output,ra_dgr,dec_dgr,aperture)

    # create aperture for the central 100arcsec
    galaxy_output = "casa_region/" + gal_name + "_100arcsec.txt"
    aperture = 100.0 # diameter in arcsec
    write_region(galaxy_output,ra_dgr,dec_dgr,aperture)

    # do imval
    spec_peak_tmp = peak_output.replace(".txt","_spec.txt")
    spec_peak = spec_peak_tmp.replace("casa_region","products")
    easy_imval(gals[i], peak_output, spec_peak)

    spec_center_tmp = center_output.replace(".txt","_spec.txt")
    spec_center = spec_center_tmp.replace("casa_region","products")
    easy_imval(gals[i], center_output, spec_center)

    spec_gaalxy_tmp = galaxy_output.replace(".txt","_spec.txt")
    spec_galaxy = spec_gaalxy_tmp.replace("casa_region","products")
    easy_imval(gals[i], galaxy_output, spec_galaxy)

    # plot
    easy_plotter(spec_peak,
                 spec_center,
                 spec_galaxy,
                 gal_name,
                 [-0.1,1.1],
                 "spec")

    easy_plotter(spec_peak,
                 spec_center,
                 spec_galaxy,
                 gal_name,
                 [-0.02,0.2],
                 "spec_zoom")


os.system("rm -rf *.last")

