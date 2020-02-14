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

def tco_abundance(Xco=3e-4,Rcotco=70):
    """
    13CO abundance relative to H2
    Rcotco = 70-200
    Xco = 1e-4 - 3e-4
    """
    Xtco = Xco / Rcotco

    return Xtco

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


#####################
### Main Procedure
#####################
# import data
data = np.loadtxt(dir_data + txt_flux)
x1 = data[:,0]
y1 = data[:,1]
fl_12co10 = data[:,2] # Jy/beam.km/s
fl_13co21 = data[:,5] # Jy/beam.km/s

# import Tkin
Tkin = np.loadtxt(txt_tkin,usecols=(2,3))[:,0]

# convert Jy/beam.km/s to K.km/s
major, minor = beam(repimage)
nu_obs_co10 = 115.27120 / (1 + redshift)
beta_co10 = 1.222e6 / major / minor / nu_obs_co10**2
nu_obs_13co21 = 220.39868420 / (1 + redshift)
beta_13co21 = 1.222e6 / major / minor / nu_obs_13co21**2
kelvin_12co10 = fl_12co10 * beta_co10
kelvin_13co21 = fl_13co21 * beta_13co21

# radial distance
r = distance_kpc(x1,y1,ra,decl)

# 13CO abundance relative to H2
X13co = tco_abundance()

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


