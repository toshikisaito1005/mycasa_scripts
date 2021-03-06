import os
import glob
import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord


#####################
### set keys
#####################
dir_fits = "/Users/saito/data/myproj_active/proj_santoro01_ngc1365/data_raw/"
dir_product = "/Users/saito/data/myproj_active/proj_santoro01_ngc1365/products/"
catalog_fits = "ngc1365_co21_v1p0_props.fits"
mom0_fits = "ngc1365_12m+7m+tp_co21_broad_mom0.fits"
output = "ngc1365_cprops_mask_1p38_deconv.fits"
snr = 5.0 # peak signal-to-noise ratio threshold to identify clouds
scale = 120.0 / 1.378 # parsec / arcsec
image_ra_cnt = "03:33:36.406"
image_decl_cnt = "-36.08.24.023"


#####################
### Main Procedure
#####################
done = glob.glob(dir_product)
if not done:
    os.mkdir(dir_product)

hdu_list = fits.open(dir_fits + catalog_fits, memmap=True)
data = Table(hdu_list[1].data)

gmc_ra_dgr = data["XCTR_DEG"]         # center ra position of the cloud in decimal degrees
gmc_decl_dgr = data["YCTR_DEG"]       # center decl position of the cloud in decimal degrees
gmc_radius_pc = data["RAD_NOEX"]      # the deconvolved radius without extrapolation in parsecs
gmc_sn_ratio = data["S2N"]            # the peak signal-to-noise ratio in the cloud
#gmc_maj = data["FWHM_MAJ_DC"]
#gmc_min = data["FWHM_MAJ_DC"]
#gmc_pa = data["POSANG"] * 180 / np.pi

cut = (gmc_radius_pc > 0.) & (gmc_sn_ratio > snr)

gmc_ra_dgr = gmc_ra_dgr[cut]
gmc_decl_dgr = gmc_decl_dgr[cut]
gmc_radius_arcsec = gmc_radius_pc[cut] / scale

# get native grid information
num_x_pix = imhead(dir_fits+mom0_fits,mode="list")["shape"][0]
num_y_pix = imhead(dir_fits+mom0_fits,mode="list")["shape"][1]
pix_radian = imhead(dir_fits+mom0_fits,mode="list")["cdelt2"]
obsfreq = imhead(dir_fits+mom0_fits,mode="list")["restfreq"][0]/1e9
pix_arcsec = round(pix_radian * 3600 * 180 / np.pi, 3)

# create image
# create template image
blc_ra_tmp = imstat(dir_fits+mom0_fits)["blcf"].split(", ")[0]
blc_dec_tmp = imstat(dir_fits+mom0_fits)["blcf"].split(", ")[1]
blc_ra = blc_ra_tmp.replace(":","h",1).replace(":","m",1)+"s"
blc_dec = blc_dec_tmp.replace(".","d",1).replace(".","m",1)+"s"
beamsize = round(imhead(dir_fits+mom0_fits,"list")["beammajor"]["value"], 2)
pix_size = round(beamsize/4.53, 2)
size_x = num_x_pix # int(image_length / pix_size)
size_y = num_y_pix # size_x
c = SkyCoord(blc_ra, blc_dec)
ra_dgr = str(c.ra.degree)
dec_dgr = str(c.dec.degree)
cl.done()

for i in range(len(gmc_radius_arcsec)):
    direction = "J2000 " + str(gmc_ra_dgr[i])+"deg " + str(gmc_decl_dgr[i])+"deg"
    cl.addcomponent(dir=direction,
                    flux=1.0,
                    fluxunit="Jy",
                    freq=str(obsfreq)+"GHz",
                    shape="disk",
                    majoraxis=str(gmc_radius_arcsec[i])+"arcsec",
                    minoraxis=str(gmc_radius_arcsec[i])+"arcsec",
                    positionangle="0deg")

ia.fromshape(dir_product+output.replace(".fits",".im"),[size_x,size_y,1,1],overwrite=True)
cs=ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad=qa.convert(qa.quantity(str(pix_size)+"arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert(image_ra_cnt,"rad")["value"],
                      qa.convert(image_decl_cnt,"rad")["value"]],
                     type="direction")
cs.setreferencevalue(str(obsfreq)+"GHz","spectral")
cs.setincrement("1GHz","spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)

immath(imagename=dir_product+output.replace(".fits",".im"),
       expr="iif(IM0>0,1,0)",
       outfile=dir_product+output.replace(".fits",".im2"))

exportfits(imagename=dir_product+output.replace(".fits",".im2"),
           fitsimage=dir_product+output,
           overwrite=True)

os.system("rm -rf " + dir_product + output.replace(".fits",".im"))
os.system("rm -rf " + dir_product + output.replace(".fits",".im2"))

cl.close()

os.system("rm -rf *.last")
