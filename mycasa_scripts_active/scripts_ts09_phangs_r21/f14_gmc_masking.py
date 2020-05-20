import os
import glob
import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord


#####################
### set keys
#####################
dir_fits = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_other/cprops/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
catalog_fits = ["ngc0628_12m+7m+tp_co21_120pc_props.fits",
				"ngc3627_12m+7m+tp_co21_120pc_props.fits",
				"ngc4321_12m+7m+tp_co21_120pc_props.fits"]
mom0_fits = ["../../ngc0628_r21/r21_04p0.moment0",
			 "../../ngc3627_r21/r21_08p0.moment0",
			 "../../ngc4321_r21/r21_04p0.moment0"]
output = ["../../ngc0628_r21/cprops_04p0.mask.fits",
		  "../../ngc3627_r21/cprops_08p0.mask.fits",
		  "../../ngc4321_r21/cprops_04p0.mask.fits"]
# output = "ngc1365_cprops_mask_1p38.fits"
snr = 5.0 # peak signal-to-noise ratio threshold to identify clouds
scales = [44/1.0,52/1.3,103/1.4] # parsec / arcsec
image_ra_cnt = ["01:36:41.790",
				"11:20:15.181",
				"12:22:54.961"]
image_decl_cnt = ["15.46.58.400",
				  "12.59.28.137",
				  "15.49.20.263"]
convolution_scale = [np.sqrt((44/1.0*4.0)**2-120**2),
					 np.sqrt((52/1.3*8.0)**2-120**2),
					 np.sqrt((103/1.4*4.0)**2-120**2),
					 ]

i=1


#####################
### Main Procedure
#####################
catalog_fits = catalog_fits[i]
mom0_fits = mom0_fits[i]
output = dir_fits + output[i]
image_ra_cnt = image_ra_cnt[i]
image_decl_cnt = image_decl_cnt[i]
scale = scales[i]
convolution_scale = convolution_scale[i]


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
gmc_radius_arcsec = np.sqrt((gmc_radius_pc[cut] / scale)**2 + (convolution_scale / scale)**2)
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
    area = float(majoraxis.replace("arcsec","")) * float(minoraxis.replace("arcsec","")) * np.pi * (4*np.log(2) * 4.007484905673586)
    cl.addcomponent(dir=direction,
                    flux=1.0,
                    fluxunit="Jy",
                    freq=str(obsfreq)+"GHz",
                    shape="disk",
                    majoraxis=majoraxis,
                    minoraxis=minoraxis,
                    positionangle=str(gmc_pa[i])+"deg")

ia.fromshape(output.replace(".fits",".im"),[size_x,size_y,1,1],overwrite=True)
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

immath(imagename=output.replace(".fits",".im"),
       expr="iif(IM0>0,1,0)",
       outfile=output.replace(".fits",".im2"))

exportfits(imagename=output.replace(".fits",".im2"),
           fitsimage=output,
           overwrite=True,
           dropstokes=True,
           dropdeg=True)

os.system("rm -rf " + output.replace(".fits",".im"))
os.system("rm -rf " + output.replace(".fits",".im2"))

#cl.close()
#cl.done()
#cs.done()
#a.close()

os.system("rm -rf *.last")
