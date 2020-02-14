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
suffix = "Halpha"
apertures = apertures_halpha
beam = beam_halpha
rms_co10 = rms_co21_halpha
rms_co21 = rms_co21_halpha
header_output = "#ra_dgr dec_dgr m0_co10 m0_co21 m2_co10 m2_co21 m8_co10 m8_co21"


#####################
### Main Procedure
#####################
ch_end = int(chans.split("~")[1])
ch_start = int(chans.split("~")[0])
nchan = ch_end - ch_start + 1
dir_data1 = dir_data + galname + "/"

### maskin
# Initial setup
m0_co10 = glob.glob(dir_data1+galname+"_co10*"+suffix+"*t0*maskin")[0]
m0_co21 = glob.glob(dir_data1+galname+"_co21*"+suffix+"*t0*maskin")[0]
m2_co10 = glob.glob(dir_data1+galname+"_co10*"+suffix+"*t2*maskin")[0]
m2_co21 = glob.glob(dir_data1+galname+"_co21*"+suffix+"*t2*maskin")[0]
m8_co10 = glob.glob(dir_data1+galname+"_co10*"+suffix+"*t8*maskin")[0]
m8_co21 = glob.glob(dir_data1+galname+"_co21*"+suffix+"*t8*maskin")[0]
c = SkyCoord(ra, decl)
ra_dgr = c.ra.degree
dec_dgr = c.dec.degree
dec_dgr_org = dec_dgr

dir_casa_region = dir_data1 + "casa_region/"
done = glob.glob(dir_casa_region)
if not done:
    os.mkdir(dir_casa_region)



# Nyquist sampling with varying aperture size
for i in range(len(apertures)):
    print("##### sampling with aperture = " + str(apertures[i]))
    # define sampling grid at the given aperture size
    stp_ra,stp_dec,rng_ra,rng_dec=Nyq.def_step(apertures[i],fov)
    #ra_dgr = ra_dgr + stp_ra
    #dec_dgr = dec_dgr - stp_dec

    # rms calculation at the given aperture size
    Sa_co,Sb_co = Nyq.def_area(m0_co21,apertures[i],beam)
    rms_apt_co10 = rms_co10*velres*sqrt(nchan)/sqrt(Sa_co) #average
    rms_apt_co21 = rms_co21*velres*sqrt(nchan)/sqrt(Sa_co) #average

    # setup for imval txt output
    if type(apertures[i]) == int:
        name_size = "{0:02d}".format(apertures[i])
    elif type(apertures[i]) == float:
        name_size = str(apertures[0]).replace(".","p")

    product_file = dir_data1+galname+"_fluxin_"+suffix+"_"\
        +str(name_size)+".txt"
    os.system("rm -rf "+product_file)
    f = open(product_file,"a")
    f.write(header_output+"\n")
    f.close()

    # sampling
    sampling_images = [m0_co10,
                       m0_co21,
                       m2_co10,
                       m2_co21,
                       m8_co10,
                       m8_co21]
    sampling_thress = [rms_apt_co10*sn_ratio,
                       rms_apt_co21*sn_ratio,
                       0,
                       0,
                       rms_co10/sqrt(Sa_co)*sn_ratio,
                       rms_co21/sqrt(Sa_co)*sn_ratio]
    S_bms = [Sb_co,
             Sb_co,
             -1,
             -1,
             -1,
             -1
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



### maskout
# Initial setup
m0_co10 = glob.glob(dir_data1+galname+"_co10*"+suffix+"*maskout")[0]
m0_co21 = glob.glob(dir_data1+galname+"_co21*"+suffix+"*maskout")[0]
c = SkyCoord(ra, decl)
ra_dgr = c.ra.degree
dec_dgr = c.dec.degree
dec_dgr_org = dec_dgr

dir_casa_region = dir_data1 + "casa_region/"
done = glob.glob(dir_casa_region)
if not done:
    os.mkdir(dir_casa_region)



# Nyquist sampling with varying aperture size
for i in range(len(apertures)):
    # define sampling grid at the given aperture size
    stp_ra,stp_dec,rng_ra,rng_dec=Nyq.def_step(apertures[i],fov)
    #ra_dgr = ra_dgr + stp_ra
    #dec_dgr = dec_dgr - stp_dec
    
    # rms calculation at the given aperture size
    S_ap,S_bm = Nyq.def_area(m0_co21,apertures[i],beam)
    rms_apt_co10 = rms_co10*velres*sqrt(nchan)/sqrt(Sa_co) #average
    rms_apt_co21 = rms_co21*velres*sqrt(nchan)/sqrt(Sa_co) #average
    
    # setup for imval txt output
    if type(apertures[i]) == int:
        name_size = "{0:02d}".format(apertures[i])
    elif type(apertures[i]) == float:
        name_size = str(apertures[0]).replace(".","p")

    product_file = dir_data1+galname+"_fluxout_"+suffix+"_"\
        +str(name_size)+".txt"
    os.system("rm -rf "+product_file)
    f = open(product_file,"a")
    f.write(header_output+"\n")
    f.close()

    # sampling
    sampling_images = [m0_co10,
                       m0_co21,
                       m2_co10,
                       m2_co21,
                       m8_co10,
                       m8_co21]
    sampling_thress = [rms_apt_co10*sn_ratio,
                       rms_apt_co21*sn_ratio,
                       0,
                       0,
                       rms_co10/sqrt(S_ap)*sn_ratio,
                       rms_co21/sqrt(S_ap)*sn_ratio]
    S_bms = [Sb_co, Sb_co, -1, -1, -1, -1]
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


