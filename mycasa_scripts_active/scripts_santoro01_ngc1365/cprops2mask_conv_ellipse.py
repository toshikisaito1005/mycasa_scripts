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
output = "ngc1365_cprops_progressive_mask_1p38.fits"
# output = "ngc1365_cprops_mask_1p38.fits"
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
gmc_radius_pc = data["RAD_NODC_NOEX"] # the radius without deconvolution or extrapolation in parsecs
gmc_sn_ratio = data["S2N"]            # the peak signal-to-noise ratio in the cloud
gmc_pa = data["POSANG"] * 180 / np.pi
gmc_num = data["CLOUDNUM"]
gmc_npix = data["NPIX"]

dx = np.sqrt(2*np.pi/(8*np.log(2)) * data["BEAMMAJ_PC"]**2 / data["PPBEAM"])
gmc_major = np.sqrt((data['MOMMAJPIX_NOEX'] * dx)**2 - (data['BEAMMAJ_PC']**2/8/np.log(2)))
gmc_minor = np.sqrt((data['MOMMINPIX_NOEX'] * dx)**2 - (data['BEAMMIN_PC']**2/8/np.log(2)))

cut = (gmc_radius_pc > 0.) & (gmc_sn_ratio > snr) & (gmc_minor > 0.) & (gmc_major > 0.)

gmc_ra_dgr = gmc_ra_dgr[cut]
gmc_decl_dgr = gmc_decl_dgr[cut]
gmc_radius_arcsec = gmc_radius_pc[cut] / scale
gmc_pa = gmc_pa[cut]
gmc_major_arcsec = gmc_major[cut] / scale
gmc_minor_arcsec = gmc_minor[cut] / scale



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

for i in range(len(gmc_ra_dgr)):
    majoraxis = str(gmc_radius_arcsec[i])+"arcsec"
    minoraxis = str(gmc_minor_arcsec[i] * gmc_radius_arcsec[i]/gmc_major_arcsec[i]) + "arcsec"
    direction = "J2000 " + str(gmc_ra_dgr[i])+"deg " + str(gmc_decl_dgr[i])+"deg"
    area = float(majoraxis.replace("arcsec","")) * float(minoraxis.replace("arcsec","")) * np.pi
    cl.addcomponent(dir=direction,
                    flux=int(float(gmc_num[i])*area*(4*np.log(2))),
                    # flux=1.0,
                    fluxunit="Jy",
                    freq=str(obsfreq)+"GHz",
                    shape="disk",
                    majoraxis=majoraxis,
                    minoraxis=minoraxis,
                    positionangle=str(gmc_pa[i])+"deg")

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
       expr="iif(IM0>0,IM0,0)",
       # expr="iif(IM0>0,1,0)",
       outfile=dir_product+output.replace(".fits",".im2"))

exportfits(imagename=dir_product+output.replace(".fits",".im2"),
           fitsimage=dir_product+output,
           overwrite=True,
           dropstokes=True,
           dropdeg=True)

os.system("rm -rf " + dir_product + output.replace(".fits",".im"))
os.system("rm -rf " + dir_product + output.replace(".fits",".im2"))

#cl.close()
#cl.done()
#cs.done()
#a.close()

os.system("rm -rf *.last")
