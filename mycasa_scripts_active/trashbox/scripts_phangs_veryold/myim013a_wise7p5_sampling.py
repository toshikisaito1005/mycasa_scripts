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
suf_wise = "wise7p5"
apertures = [apertures_wise7p5] # diameter in arcsec
beam_co = beam_size
beam_wise = 7.5
rms_w1 = rms_w1_7p5
rms_w2 = rms_w2_7p5
rms_w3 = rms_w2_7p5
header_output = "#ra_dgr dec_dgr m0_co10 m0_co21 f_w1 f_w2 f_w3 m2_co10 m2_co21 m8_co10 m8_co21 ha+co_mask"



#####################
### Main Procedure
#####################
ch_end = int(chans.split("~")[1])
ch_start = int(chans.split("~")[0])
nchan = ch_end - ch_start + 1
dir_wise = dir_data + "wise/"
dir_data1 = dir_data + galname + "/"
dir_mask = dir_data + "galmasks/"



### Initial setup
suf_wise_head = suf_wise.replace("wise","")
image_w1 = glob.glob(dir_wise+galname+"*w1*"+suf_wise_head+"*")[0]
image_w2 = glob.glob(dir_wise+galname+"*w2*"+suf_wise_head+"*")[0]
image_w3 = glob.glob(dir_wise+galname+"*w3*"+suf_wise_head+"*")[0]
m0_co10 = glob.glob(dir_data1+galname+"_co10*"+suffix+"*ent0")[0]
m0_co21 = glob.glob(dir_data1+galname+"_co21*"+suffix+"*ent0")[0]
m2_co10 = glob.glob(dir_data1+galname+"_co10*"+suffix+"*ent2")[0]
m2_co21 = glob.glob(dir_data1+galname+"_co21*"+suffix+"*ent2")[0]
m8_co10 = glob.glob(dir_data1+galname+"_co10*"+suffix+"*ent8")[0]
m8_co21 = glob.glob(dir_data1+galname+"_co21*"+suffix+"*ent8")[0]
im_mask = glob.glob(dir_mask+galname+"*")[0]
c = SkyCoord(ra, decl)
ra_dgr = c.ra.degree
dec_dgr = c.dec.degree
dec_dgr_org = dec_dgr

dir_casa_region = dir_data1 + "casa_region/"
done = glob.glob(dir_casa_region)
if not done:
    os.mkdir(dir_casa_region)



### Nyquist sampling with varying aperture size
for i in range(len(apertures)):
    print("##### sampling with aperture = " + str(apertures[i]))
    # define sampling grid at the given aperture size
    if galname == "ngc3627":
        stp_ra,stp_dec,rng_ra,rng_dec=Nyq.def_step2(apertures[i],fov)
    else:
        stp_ra,stp_dec,rng_ra,rng_dec=Nyq.def_step(apertures[i],fov)
    
    # rms calculation at the given aperture size
    Sa_co,Sb_co = Nyq.def_area(m0_co21,apertures[i],beam_co)
    rms_apt_co10 = rms_co10*velres*sqrt(nchan)/sqrt(Sa_co) #average
    rms_apt_co21 = rms_co21*velres*sqrt(nchan)/sqrt(Sa_co) #average
    Sa_wise,Sb_wise = Nyq.def_area(image_w3,apertures[i],beam_wise)
    rms_apt_w1 = rms_w1/sqrt(Sa_wise) #average
    rms_apt_w2 = rms_w2/sqrt(Sa_wise) #average
    rms_apt_w3 = rms_w3/sqrt(Sa_wise) #average
    
    # setup for imval txt output
    if type(apertures[i]) == int:
        name_size = "{0:02d}".format(apertures[i])
    elif type(apertures[i]) == float:
        name_size = str(apertures[i]).replace(".","p").replace("0","")

    product_file = dir_data1+galname+"_flux_"+suf_wise+"_"\
        +str(name_size)+".txt"
    os.system("rm -rf "+product_file)
    f = open(product_file,"a")
    f.write(header_output+"\n")
    f.close()

    # sampling
    sampling_images = [m0_co10,
                       m0_co21,
                       image_w1,
                       image_w2,
                       image_w3,
                       m2_co10,
                       m2_co21,
                       m8_co10,
                       m8_co21,
                       im_mask]
    sampling_thress = [rms_apt_co10*sn_ratio,
                       rms_apt_co21*sn_ratio,
                       rms_apt_w1*sn_ratio,
                       rms_apt_w2*sn_ratio,
                       rms_apt_w3*sn_ratio,
                       0,
                       0,
                       rms_co10/sqrt(Sa_co)*sn_ratio,
                       rms_co21/sqrt(Sa_co)*sn_ratio,
                       0]
    S_bms = [Sb_co,
             Sb_co,
             Sb_wise,
             Sb_wise,
             Sb_wise,
             -1,
             -1,
             -1,
             -1,
             -1]
    Nyq.hexa_sampling(apertures[i],
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

