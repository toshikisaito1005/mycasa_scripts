import os
import sys
import glob
import scipy
import numpy as np


# CASA imports
from taskinit import *
from plotms import plotms
from listobs import listobs
from immoments import immoments
from immath import immath
from imstat import imstat
from statwt import statwt
from makemask import makemask
from imhead import imhead
from imstat import imstat
from feather import feather
from exportfits import exportfits
import analysisUtils as aU
mycl = aU.createCasaTool(cltool)
myia = aU.createCasaTool(iatool)
myrg = aU.createCasaTool(rgtool)
mymsmd = aU.createCasaTool(msmdtool)


###############################
### def
###############################
def eazy_plotms(vis,spw,plotfile,xaxis):
    os.system("rm -rf " + plotfile)
    if xaxis=="freq":
        avgchannel = "0"
    else:
        avgchannel = ""

    plotms(vis = vis,
           customsymbol = True,
           symbolshape = "square",
           symbolsize = 5,
           spw = spw,
           xaxis = xaxis,
           yaxis = "amp",
           avgchannel = avgchannel,
           avgtime = "1e8",
           avgscan = True,
           avgfield = True,
           avgbaseline = True,
           showmajorgrid = True,
           showminorgrid = True,
           showgui = False,
           plotfile = plotfile,
           showatm = True)


def find_spw_co10(vis):
    mymsmd.open(vis)
    spws = mymsmd.spwsforintent("OBSERVE_TARGET#ON_SOURCE")
    freq_diffs = []
    for j in range(len(spws)):
        freq_diffs.append(abs(mymsmd.meanfreq(spws[j])-115.27120e+9))
    mymsmd.done()
    spw_co10 = spws[np.argmin(freq_diffs)]

    return spw_co10


def know_makems_keys(galaxy):
    keys = np.loadtxt("key_makems.txt",dtype="S100")
    index = np.where(keys[:,0]==galaxy)[0][0]

    tplinechans = keys[:,1][index]
    tp2viswt_value = float(keys[:,2][index])
    exclude_7m = keys[:,3][index]
    exclude_12m = keys[:,4][index]

    return tplinechans, tp2viswt_value, exclude_7m, exclude_12m


def know_rawdata_keys(galaxy):
    keys = np.loadtxt("key_rawdata.txt",dtype="S100")
    index_12m = np.where((keys[:,0]==galaxy) & (keys[:,1]=="12m"))[0][0]
    index_7m = np.where((keys[:,0]==galaxy) & (keys[:,1]=="7m"))[0][0]
    index_tp = np.where((keys[:,0]==galaxy) & (keys[:,1]=="tp"))[0][0]

    vis_12m = keys[:,2][index_12m]
    vis_7m = keys[:,2][index_7m]
    image_tp = keys[:,2][index_tp]

    return vis_12m, vis_7m, image_tp


def know_imaging_keys(galaxy):
    keys = np.loadtxt("key_imaging.txt",dtype="S100")
    index = np.where(keys[:,0]==galaxy)[0][0]

    nchan = int(keys[:,1][index])
    start = str(keys[:,2][index]) + "km/s"
    width = str(keys[:,3][index]) + "km/s"

    return nchan, start, width


def know_pointings(vis,galname):
    listobs(vis, listfile="int.listobs")
    ld = open("int.listobs")
    lines = ld.readlines()
    ld.close()
    os.system("rm -rf int.listobs")
    
    num = 0
    for line in lines:
        num += 1
        if line.find("Fields:") >= 0:
            listobs_l = num
        elif line.find("Spectral Windows:") >= 0:
            listobs_r = num

    mymsmd.open(vis)
    sciencetarget = mymsmd.fieldsforintent("OBSERVE_TARGET#ON_SOURCE",True)[0]
    mymsmd.close()

    array_list_tmp = lines[listobs_l:listobs_r]
    array_list = ["J2000 "+k[27:].split("J2000")[0] for k in array_list_tmp if sciencetarget in k]
    ptgfile = galname+"_tp.ptg"
    np.savetxt(ptgfile,array_list,fmt="%s")

    return ptgfile, sciencetarget

"""
def eazy_mstransform(vis,outputvis,excludechans,array,nchan,start,width):
    os.system("rm -rf " + outputvis)
    os.system("cp -r " + vis + " " + outputvis)
    spw = str(find_spw_co10(vis))
    statwt(vis = outputvis,
           spw = spw,
           excludechans = spw + ":" + excludechans,
           datacolumn = "data")

    regrid_array = dir_working + galname + "_"+array+".ms"
    print("# mstransform "+array+" ms")
    os.system("rm -rf " + regrid_array)
    mstransform(vis = outputvis,
                outputvis = regrid_array,
                spw = spw,
                regridms = True,
                mode = "velocity",
                nchan = nchan,
                start = start,
                width = width,
                restfreq = "115.27120GHz",
                outframe = "LSRK",
                datacolumn = "data")

    os.system("rm -rf " + outputvis + "*")

    return regrid_array
"""


def know_imaging_keys2(galaxy):
    keys = np.loadtxt("key_imaging.txt",dtype="S100")
    index = np.where(keys[:,0]==galaxy)[0][0]
    
    nchan = int(keys[:,1][index])
    start = str(keys[:,2][index]) + "km/s"
    width = str(keys[:,3][index]) + "km/s"
    imsize = int(keys[:,4][index])
    cell = str(keys[:,5][index]) + "arcsec"
    pblimit = float(keys[:,6][index])
    robust = float(keys[:,7][index])
    rms = float(keys[:,8][index])
    
    return nchan, start, width, imsize, cell, pblimit, robust, rms


def createmask(imagename,thres,outmask):
    """
    """
    os.system("rm -rf " + outmask)
    immath(imagename = imagename,
           mode = "evalexpr",
           expr = "iif(IM0 >= " + str(thres) + ", 1.0, 0.0)",
           outfile = outmask)
    imhead(imagename = outmask,
           mode = "del",
           hdkey = "beammajor")


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


def removesmallmasks(maskim,beamarea,pixelmin=0.3):
    os.system("rm -rf "+maskim+".min")
    os.system("cp -r "+maskim+" "+maskim+".min")
    maskfile=maskim+".min"
    myia.open(maskfile)
    mask=myia.getchunk()
    labeled,j=scipy.ndimage.label(mask)
    myhistogram=scipy.ndimage.measurements.histogram(labeled,0,j+1,j+1)
    object_slices=scipy.ndimage.find_objects(labeled)
    threshold_area=beamarea*pixelmin
    for i in range(j):
        if myhistogram[i+1]<threshold_area:
            mask[object_slices[i]]=0

    myia.putchunk(mask)
    myia.done()


def know_imaging_keys3(galaxy):
    keys = np.loadtxt("key_imaging.txt",dtype="S100")
    index = np.where(keys[:,0]==galaxy)[0][0]
    
    rms = float(keys[:,8][index])
    snr = float(keys[:,9][index])
    pbcut = float(keys[:,10][index])
    
    return rms, snr, pbcut
