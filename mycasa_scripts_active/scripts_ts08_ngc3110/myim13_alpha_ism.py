import os
import sys
import re
import glob
import numpy as np
import scipy
from astropy.coordinates import SkyCoord
sys.path.append(os.getcwd() + "/../")
import mycasaanalysis_tools3 as myana


#####################
### parameters
#####################
dir_data = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/image_nyquist/"
txt_flux = "ngc3110_all_sum.txt"
ra = "10h04m02.090s"
decl = "-6d28m29.604s"
redshift = 0.016858

repimage = dir_data + "../image_12co10/12co10.moment0"
txt_tkin = dir_data+"ngc3110_radex_tkin.txt"


#####################
### def
#####################
def degcoord(ra,decl):
    c = SkyCoord(ra, decl)
    ra_dgr = str(c.ra.degree)
    dec_dgr = str(c.dec.degree)

    return ra_dgr, dec_dgr

def distance_kpc(x1,y1,ra,decl,pa=171.,incl=65.,scale=0.325):
    ra_cnt, decl_cnt = degcoord(ra,decl)
    x2 = x1 - float(ra_cnt)
    y2 = y1 - float(decl_cnt)
    
    pa2 = pa * np.pi/180.
    incl2 = incl * np.pi/180.

    x3 = (x2*cos(pa2) - y2*sin(pa2)) / np.cos(incl2)
    y3 = x2*sin(pa2) + y2*cos(pa2)
    distance = np.sqrt(x3**2 + y3**2) * 3600. * scale

    return distance

def factor_b2m(Td):
    """
    """
    z = 0.016858
    h = 6.626e-27 # erg.s
    k = 1.38e-16 # erg/K
    nu_obs = 234.6075e+9 / (1 + z) #GHz
    alpha_850 = 6.7e+19
    
    factor = h * nu_obs * (1+z) / (k * Td)
    factor_0 = h * 352.6970094e+9 * (1+0) / (k * Td)
    gamma_rj = factor / (np.exp(factor) - 1)
    gamma_0 = factor_0 / (np.exp(factor_0) - 1)
    factor_b2m_tmp1 = 1.78 * (1+z)**-4.8 * (352.6970094/234.6075)**3.8
    factor_b2m_tmp2 = (69.4/1000.)**2 * 10.e+10
    factor_b2m_tmp3 = factor_b2m_tmp1 * factor_b2m_tmp2
    factor_b2m = factor_b2m_tmp3 * (6.7e+19/alpha_850) * gamma_0/gamma_rj
    
    return factor_b2m

def beam(imagename):
    """
    for moment map creation
    """
    major = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beammajor")["value"]
    minor = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beamminor")["value"]
                   
    return major, minor

def beam_area(imagename):
    """
    """
    major = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beammajor")["value"]
    minor = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beamminor")["value"]
    pix = abs(imhead(imagename = imagename,
                     mode = "list")["cdelt1"])
                   
    pixelsize = pix * 3600 * 180 / np.pi
    beamarea_arcsec = major * minor * np.pi/(4 * np.log(2))
    beamarea_pix = beamarea_arcsec / (pixelsize ** 2)
                   
    return beamarea_pix

#####################
### Main Procedure
#####################
# import data
data = np.loadtxt(dir_data + txt_flux)
x1 = data[:,0]
y1 = data[:,1]
fl_12co10 = data[:,2] # Jy/beam.km/s
fl_band6 = data[:,9] # Jy/beam

# import Tkin
Tkin = np.loadtxt(txt_tkin,usecols=(2,3))[:,0]

# convert Jy/beam.km/s to K.km/s
major, minor = beam(repimage)
nu_obs_co10 = 115.27120 / (1 + redshift)
beta_co10 = 1.222e6 / major / minor / nu_obs_co10**2
kelvin_12co10 = fl_12co10 * beta_co10

# convert Jy/beam to Jy
beamarea_pix = beam_area(repimage)
fl_band6_Jy = fl_band6 / beamarea_pix

# radial distance
r = distance_kpc(x1,y1,ra,decl)


"""
# measure column density using rotation diagram for 13CO
product1 = dir_data + "ngc3110_alpha_lte.txt"
os.system("rm -rf " + product1)
f = open(product1, "w")
f.write("# x y distance alpha_lte(Trot) alpha_lte(Tkin)\n")
f.close()
for i in range(len(kelvin_13co21)):
    logN_rot, Qrot = myana.rot0_13co(15.0, kelvin_13co21[i], data = "../Qrot_CDMS.txt")
    logN_kin, Qrot = myana.rot0_13co(Tkin[i], kelvin_13co21[i], data = "../Qrot_CDMS.txt")
    
    if fl_12co10[i] > 0:
        #
        NH2 = 10**logN_rot / X13co
        X_co = NH2 / kelvin_12co10[i]
        alpha_lte_Trot = 4.3 * X_co / 2e+20
        #
        NH2 = 10**logN_kin / X13co
        X_co = NH2 / kelvin_12co10[i]
        alpha_lte_Tkin = 4.3 * X_co / 2e+20
    else:
        alpha_lte_Trot = 0.0
        alpha_lte_Tkin = 0.0
    
    if Tkin[i]==0:
        alpha_lte_Tkin = 0.0
    
    f = open(product1, "a")
    f.write(str(x1[i]) + " " + str(y1[i]) + " " + str(r[i]) \
            + " " + str(alpha_lte_Trot) + " " + str(alpha_lte_Tkin) + "\n")
    f.close()
"""
