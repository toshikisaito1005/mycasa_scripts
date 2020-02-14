import os
import re
import sys
import glob
import numpy as np
import scipy.ndimage
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.patches as patches
from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord

# CASA imports
from taskinit import *
from importfits import importfits
from imregrid import imregrid
from imsmooth import imsmooth
from imval import imval
from immoments import immoments
from immath import immath
from makemask import makemask
from imhead import imhead
from imstat import imstat
from exportfits import exportfits
import analysisUtils as aU
mycl = aU.createCasaTool(cltool)
myia = aU.createCasaTool(iatool)
myrg = aU.createCasaTool(rgtool)



#####################
### Main Procedure
#####################
def w_median(data, weights):
    """
        Args:
        data (list or numpy.array): data
        weights (list or numpy.array): weights
        """
    data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
    s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
    midpoint = 0.5 * sum(s_weights)
    if any(weights > midpoint):
        w_median = (data[weights == np.max(weights)])[0]
    else:
        cs_weights = np.cumsum(s_weights)
        idx = np.where(cs_weights <= midpoint)[0][-1]
        if cs_weights[idx] == midpoint:
            w_median = np.mean(s_data[idx:idx+2])
        else:
            w_median = s_data[idx+1]
    return w_median


def w_avg_and_std(values, weights):
    """
        Return the weighted average and standard deviation.
        
        values, weights -- Numpy ndarrays with the same shape.
        """
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)  # Fast and numerically precise
    return (average, math.sqrt(variance))


def easy_imval(imagename,region_file,thres,S_bm):
    """
    - 1
    """
    value = imval(imagename = imagename,
                  region = region_file)
    value_masked = value["data"] * value["mask"]

    data = value_masked.mean(axis = (0, 1))

    if data < thres:
        data = 0.0
    
    return data


def easy_imval_w(imagename,region_file,thres,S_bm):
    """
    - 1
    """
    value = imval(imagename = imagename,
                  region = region_file)
    value_masked = value["data"] * value["mask"]

    data_1d_tmp = value_masked.ravel()
    data_1d = []
    for i in range(len(data_1d_tmp)):
        if data_1d_tmp[i] > 0:
            data_1d.append(data_1d_tmp[i])

    array_1d = np.array(data_1d)

    # weighted stats
    if len(data_1d) > 1:
        data = np.average(array_1d, weights = array_1d)
    else:
        data = 0

    if data < thres:
        data = 0.0

    return data


def easy_imval_iw(imagename,region_file,thres,S_bm):
    """
        - 1
        """
    value = imval(imagename = imagename,
                  region = region_file)
    value_masked = value["data"] * value["mask"]
                  
    data_1d_tmp = value_masked.ravel()
    data_1d = []
    for i in range(len(data_1d_tmp)):
        if data_1d_tmp[i] > 0:
            data_1d.append(data_1d_tmp[i])

    array_1d = np.array(data_1d)

    # weighted stats
    if len(data_1d) > 1:
        data = np.average(array_1d, weights = 1/array_1d)
    else:
        data = 0

    if data < thres:
        data = 0.0
    
    return data


def write_region(region_file,ra_dgr,dec_dgr,aperture):
    """
    - 2
    """
    f = open(region_file, "w")
    f.write("#CRTFv0\n")
    f.write("global coord=J2000\n")
    f.write("\n")
    f.write("circle[[" + str(round(ra_dgr, 5)) + "deg, " \
            + str(round(dec_dgr, 7)) + "deg], " \
            + str(round(aperture/2.)) + "arcsec]")
    f.write("")
    f.close()



def def_step(aperture,fov):
    """
    - 3
    hexagonal Nyquist sampling
    """
    stp_ra = aperture / 60. / 60. # degree
    stp_dec = aperture / 60. / 60. * np.sqrt(3) # degree
    rng_ra = int(fov / aperture)
    rng_dec = int(fov / 2. / aperture)

    return stp_ra, stp_dec, rng_ra, rng_dec



def def_step2(aperture,fov):
    """
    - 3
    hexagonal Nyquist sampling
    """
    stp_ra = aperture / 60. / 60. # degree
    stp_dec = aperture / 60. / 60. * np.sqrt(3) # degree
    rng_ra = int(fov / aperture)
    rng_dec = int(fov / 2. / aperture * 1.9)
    
    return stp_ra, stp_dec, rng_ra, rng_dec



def def_area(imagename,aperture,beam):
    """
    - 4
    """
    pixsize_tmp = imhead(imagename, mode="list")["cdelt1"]
    pixsize = round(abs(pixsize_tmp) * 3600 * 180 / np.pi, 2)
    S_ap = (aperture/2.) ** 2 * np.pi / pixsize ** 2 # aperture area
    S_bm = (beam/2.) ** 2 * np.pi / pixsize ** 2 # beam area

    return S_ap, S_bm



def hexa_sampling(aperture,
                  imagenames,
                  thress,
                  ra_dgr,
                  dec_dgr_org,
                  rng_ra,
                  rng_dec,
                  stp_ra,
                  stp_dec,
                  S_bms,
                  dir_casa_region,
                  product_file):
    """
    - 5
    """
    for i in range(rng_ra):
        ra_dgr = ra_dgr - stp_ra
        ra_dgr2 = ra_dgr - stp_ra / 2.
        
        dec_dgr = dec_dgr_org
        for j in range(rng_dec):
            if dec_dgr > 0:
                dec_dgr = dec_dgr + stp_dec
                dec_dgr2 = dec_dgr + stp_dec/2.
            else:
                dec_dgr = dec_dgr - stp_dec
                dec_dgr2 = dec_dgr - stp_dec/2.
            
            # region R (full beam sampling)
            name_r = "R_"+str(i)+"_"+str(j)+".region"
            region_r = dir_casa_region + name_r
            write_region(region_r,ra_dgr,dec_dgr,aperture)

            # region H (full beam sampling sifted by aperture/2)
            name_h = "H_"+str(i)+"_"+str(j)+".region"
            region_h = dir_casa_region + name_h
            write_region(region_h,ra_dgr2,dec_dgr2,aperture)

            # photometry and output
            f = open(product_file, "a")
            R, R2, R3 = [], [], []
            H, H2, H3 = [], [], []
            for k in range(len(imagenames)):
                Rtmp=easy_imval(imagenames[k],
                                region_r,
                                thress[k],
                                S_bms[k])
                Htmp=easy_imval(imagenames[k],
                                region_h,
                                thress[k],
                                S_bms[k])
                R2tmp=easy_imval_w(imagenames[k],
                                   region_r,
                                   thress[k],
                                   S_bms[k])
                H2tmp=easy_imval_w(imagenames[k],
                                   region_h,
                                   thress[k],
                                   S_bms[k])
                R3tmp=easy_imval_iw(imagenames[k],
                                    region_r,
                                    thress[k],
                                    S_bms[k])
                H3tmp=easy_imval_iw(imagenames[k],
                                    region_h,
                                    thress[k],
                                    S_bms[k])
                R.append(str(Rtmp))
                H.append(str(Htmp))
                R2.append(str(R2tmp))
                H2.append(str(H2tmp))
                R3.append(str(R3tmp))
                H3.append(str(H3tmp))

            f.write(str(ra_dgr)+" "+str(dec_dgr)+" "\
                    +str(" ".join(R))+" "\
                    +str(" ".join(R2))+" "\
                    +str(" ".join(R3))+"\n")
            f.write(str(ra_dgr2)+" "+str(dec_dgr2)+" "\
                    +str(" ".join(H))+" "\
                    +str(" ".join(H2))+" "\
                    +str(" ".join(H3))+"\n")
            f.close()


