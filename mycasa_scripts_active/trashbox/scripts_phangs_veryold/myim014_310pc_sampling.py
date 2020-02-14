import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
sys.path.append(os.getcwd() + "/../../")
import mycasaimaging_tools as myim
import mycasaimaging_tools2 as myim2
import mycasaimaging_Nyquist as Nyq
from astropy import units as u
from astropy.coordinates import SkyCoord



#####################
### Define Parameters
#####################
header_output = "#ra_dgr dec_dgr m0_co10 m0_co21 m2_co10 m2_co21 m8_co10 m8_co21"



#####################
### Main Procedure
#####################
ch_end = int(chans.split("~")[1])
ch_start = int(chans.split("~")[0])
nchan = ch_end - ch_start + 1
dir_data = dir_data + galname + "/"

### Initial setup
image_co10 = glob.glob(dir_data+galname+"_co10*"+suffix+"*moment0")[0]
image_co21 = glob.glob(dir_data+galname+"_co21*"+suffix+"*moment0")[0]
mom2_co10 = glob.glob(dir_data+galname+"_co10*"+suffix+"*moment2")[0]
mom2_co21 = glob.glob(dir_data+galname+"_co21*"+suffix+"*moment2")[0]
mom8_co10 = glob.glob(dir_data+galname+"_co10*"+suffix+"*moment8")[0]
mom8_co21 = glob.glob(dir_data+galname+"_co21*"+suffix+"*moment8")[0]
c = SkyCoord(ra, decl)
ra_dgr = c.ra.degree
dec_dgr = c.dec.degree
dec_dgr_org = dec_dgr

dir_casa_region = dir_data + "casa_region/"
done = glob.glob(dir_casa_region)
if not done:
    os.mkdir(dir_casa_region)



### Nyquist sampling with varying aperture size
for i in range(len(aperture_310pc)):
    print("##### sampling with aperture = " + str(aperture_310pc[i]))
    # define sampling grid at the given aperture size
    if galname == "ngc3627":
        stp_ra,stp_dec,rng_ra,rng_dec=Nyq.def_step2(aperture_310pc[i],fov)
    else:
        stp_ra,stp_dec,rng_ra,rng_dec=Nyq.def_step(aperture_310pc[i],fov)

    # rms calculation at the given aperture size
    Sa_co,Sb_co = Nyq.def_area(image_co21,aperture_310pc[i],beam_size)
    rms_apt_co10 = rms_co10*velres*sqrt(nchan)/sqrt(Sa_co) #average
    rms_apt_co21 = rms_co21*velres*sqrt(nchan)/sqrt(Sa_co) #average

    # setup for imval txt output
    if type(aperture_310pc[i]) == int:
        name_size = "{0:02d}".format(aperture_310pc[i])
    elif type(aperture_310pc[i]) == float:
        name_size = str(aperture_310pc[0]).replace(".","p")

    product_file = dir_data+galname+"_flux_320pc_"\
                   +str(name_size)+".txt"
    os.system("rm -rf "+product_file)
    f = open(product_file,"a")
    f.write(header_output+"\n")
    f.close()

    # sampling
    sampling_images = [image_co10,
                       image_co21,
                       mom2_co10,
                       mom2_co21,
                       mom8_co10,
                       mom8_co21]
    sampling_thress = [rms_apt_co10*sn_ratio,
                       rms_apt_co21*sn_ratio,
                       0,
                       0,
                       rms_co10/sqrt(Sa_co)*sn_ratio,
                       rms_co21/sqrt(Sa_co)*sn_ratio]
    S_bms = [Sb_co, Sb_co, -1, -1, -1, -1]
    Nyq.hexa_sampling(aperture_310pc[i],
                      sampling_images,
                      sampling_thress,
                      ra_dgr,
                      dec_dgr_org,
                      rng_ra,
                      rng_dec,
                      stp_ra,
                      stp_dec,
                      S_bms,
                      dir_casa_region,
                      product_file)

