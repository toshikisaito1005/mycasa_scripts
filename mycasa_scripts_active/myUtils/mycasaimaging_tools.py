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

# CASA imports
from taskinit import *
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
def createmask(dir_data,
        imagename,
        thres,
        outmask = "mask1.image",
        pixelmin = 5.
        ):
    #create mask with thres
    outfile = dir_data + outmask
    os.system("rm -rf " + outfile)
    immath(imagename = dir_data + imagename,
        mode = "evalexpr",
        expr = "iif(IM0 >= " + str(thres) + ", 1.0, 0.0)",
        outfile = outfile)
    imhead(imagename = outfile,
        mode = "del",
        hdkey = "beammajor")
    makemask(mode = "copy",
        inpimage = outfile,
        inpmask = outfile,
        output = outfile + ":mask0",
        overwrite = True)



def moment_maps(dir_data,
        imagename,
        chans,
        mask,
        thres
        ):
    #modify the header of the mask
    maskname = dir_data + "mask2.image"
    os.system("rm -rf " + maskname)
    os.system("cp -r " + dir_data + mask + " " + maskname)
    bmaj = imhead(imagename = imagename,
               mode = "list")["beammajor"]["value"]
    bmin = imhead(imagename = imagename,
               mode = "list")["beamminor"]["value"]
    bpa = imhead(imagename = imagename,
              mode = "list")["beampa"]["value"]
    imhead(imagename = maskname,
        mode = "put",
        hdkey = "beammajor",
        hdvalue = str(bmaj) + "arcsec")
    imhead(imagename = maskname,
        mode = "put",
        hdkey = "beamminor",
        hdvalue = str(bmin) + "arcsec")
    imhead(imagename = maskname,
        mode = "put",
        hdkey = "beampa",
        hdvalue = str(bpa) + "deg")
    #create masked cube
    outfile = imagename + ".masked"
    os.system("rm -rf " + outfile)
    immath(imagename = [imagename, maskname],
        mode = "evalexpr",
        expr = "iif(IM1 >= 1.0, IM0, 0.0)",
        outfile = outfile)
    #create moment maps using the masked cube
    outfile = imagename + ".moment0"
    os.system("rm -rf " + outfile)
    immoments(imagename = imagename + ".masked",
        moments = [0],
        chans = chans,
        includepix = [thres, 100000.],
        outfile = outfile)
    outfile = imagename + ".moment1"
    os.system("rm -rf " + outfile)
    immoments(imagename = imagename + ".masked",
        moments = [1],
        chans = chans,
        includepix = [thres, 100000.],
        outfile = outfile)
    outfile = imagename + ".moment2"
    os.system("rm -rf " + outfile)
    immoments(imagename = imagename + ".masked",
        moments = [2],
        chans = chans,
        includepix = [thres, 100000.],
        outfile = outfile)
    outfile = imagename + ".moment8"
    os.system("rm -rf " + outfile)
    immoments(imagename = imagename + ".masked",
        moments = [8],
        chans = chans,
        includepix = [thres, 100000.],
        outfile = outfile)
    #os.system("rm -rf " + imagename + ".masked")



def line_ratio(dir_data,
        im1,
        im2,
        outfile,
        diff,
        mask = []):
    os.system("rm -rf " + dir_data + outfile)
    os.system("rm -rf " + dir_data + outfile + ".beforemask")
    if not mask:
        immath(imagename = [dir_data + im1, dir_data + im2],
            mode = "evalexpr",
            expr = "IM0/IM1/" + diff,
            outfile = dir_data + outfile)
    else:
        #modify the header of the mask
        maskname = dir_data + mask
        bmaj = imhead(imagename = dir_data + im1,
                   mode = "list")["beammajor"]["value"]
        bmin = imhead(imagename = dir_data + im1,
                   mode = "list")["beamminor"]["value"]
        bpa = imhead(imagename = dir_data + im1,
                   mode = "list")["beampa"]["value"]
        imhead(imagename = maskname,
            mode = "put",
            hdkey = "beammajor",
            hdvalue = str(bmaj) + "arcsec")
        imhead(imagename = maskname,
            mode = "put",
            hdkey = "beamminor",
            hdvalue = str(bmin) + "arcsec")
        imhead(imagename = maskname,
            mode = "put",
            hdkey = "beampa",
            hdvalue = str(bpa) + "deg")
        immath(imagename = [dir_data + im1, dir_data + im2],
            mode = "evalexpr",
            expr = "IM0/IM1/" + diff,
            outfile = dir_data + outfile + ".beforemask")
        immath(imagename = [dir_data + outfile + ".beforemask",
                            maskname],
               mode= "evalexpr",
               expr = "iif(IM1 >= 1.0, IM0, 0.0)",
               outfile = dir_data + outfile)
        os.system("rm -rf " + dir_data + outfile + ".beforemask")



def fits2eps(dir_data, imagename_color, imagename_contour, ra_center,
        dec_center, title, colorbar_label, output, colorscale,
        colorlog = False, value = None, colorbar = False,
        contour = [0.1], color_contour = "k", color_beam = "b",
        xlim = ([-30, 30]), ylim = ([30, -30]), clim = None, nucleus=None, showbeam=True):
    """
    test
    """
    ra_center_define = (float(ra_center.split(":")[0]) \
                       + float(ra_center.split(":")[1]) / 60. \
                       + float(ra_center.split(":")[2]) / 3600. ) \
                       * 15.
    if dec_center.split(".")[0][0] == "-":
        dec_center_define = float(dec_center.split(".")[0]) \
                            - float(dec_center.split(".")[1]) / 60. \
                            - float(dec_center.split(".")[2] + "." + dec_center.split(".")[3]) / 3600.
    else:
        dec_center_define = float(dec_center.split(".")[0]) \
                            + float(dec_center.split(".")[1]) / 60. \
                            + float(dec_center.split(".")[2] + "." + dec_center.split(".")[3]) / 3600.
    image_file = dir_data + imagename_color
    datamax = imhead(image_file, "list")["datamax"]
    hdu_list = fits.open(image_file)
    ra_imagecenter = hdu_list[0].header["CRVAL1"]
    dec_imagecenter = hdu_list[0].header["CRVAL2"]
    ra_pixsize = abs(hdu_list[0].header["CDELT1"]) * 3600
    dec_pixsize = abs(hdu_list[0].header["CDELT2"]) * 3600
    print(ra_pixsize, dec_pixsize)
    ra_pixcenter = hdu_list[0].header["CRPIX1"]
    dec_pixcenter = hdu_list[0].header["CRPIX2"]
    dec_newcenter_offset = (dec_imagecenter - dec_center_define) \
                           * 3600 / dec_pixsize
    ra_newcenter_offset = (ra_imagecenter - ra_center_define) \
                           * 3600 / ra_pixsize
    ra_newcenter = ra_pixcenter - ra_newcenter_offset
    dec_newcenter = dec_pixcenter - dec_newcenter_offset
    ra_size = hdu_list[0].header["NAXIS1"]
    dec_size = hdu_list[0].header["NAXIS2"]
    image_data = hdu_list[0].data[0,0,:,:] # .data[:,:]
    xmin_col = (+ 0.5 - ra_newcenter) * ra_pixsize
    xmax_col = (ra_size + 0.5 - ra_newcenter) * ra_pixsize
    ymin_col = (+ 1.5 - dec_newcenter) * dec_pixsize
    ymax_col = (dec_size + 1.5 - dec_newcenter) * dec_pixsize
    xmin_cnt = (+ 1.0 - ra_newcenter) * ra_pixsize
    xmax_cnt = (ra_size + 1.0 - ra_newcenter) * ra_pixsize
    ymin_cnt = (+ 1.0 - dec_newcenter) * dec_pixsize
    ymax_cnt = (dec_size + 1.0 - dec_newcenter) * dec_pixsize
    plt.figure()
    plt.rcParams["font.size"] = 14
    if colorlog == True:
        plt.imshow(image_data,
                   norm = LogNorm(vmin = 0.02 * datamax,
                                  vmax = datamax),
                   cmap = colorscale,
                   extent = [xmin_col, xmax_col, ymin_col, ymax_col])
    else:
        plt.imshow(image_data,
                   cmap = colorscale,
                   extent = [xmin_col, xmax_col, ymin_col, ymax_col])
    plt.xlim(xlim)
    plt.ylim(ylim)
    if clim != None:
        plt.clim(clim)
    plt.title(title)
    plt.xlabel("x-offset (arcsec)")
    plt.ylabel("y-offset (arcsec)")
    if colorbar == True:
        cbar = plt.colorbar()
        cbar.set_label(colorbar_label)
    contour_file = dir_data + imagename_contour
    hdu_contour = fits.open(contour_file)
    contour_data = hdu_contour[0].data[0,0,:,:] # .data[:,:]
    if value != None:
        value_contour = value
    else:
        value_contour = imhead(contour_file, "list")["datamax"]
    contour2 = map(lambda x: x * value_contour, contour)
    plt.contour(contour_data, levels = contour2,
                extent = [xmin_cnt, xmax_cnt, ymax_cnt, ymin_cnt],
                colors = color_contour, linewidths = [0.5])
    if showbeam==True:
        bmaj = imhead(image_file, "list")["beammajor"]["value"]
        bmin = imhead(image_file, "list")["beamminor"]["value"]
        bpa = imhead(image_file, "list")["beampa"]["value"]
        ax = plt.axes()
        e = patches.Ellipse(xy = (min(xlim) * 0.8,
                                  max(ylim) * 0.8),
                            width = bmin,
                            height = bmaj,
                            angle = bpa * -1,
                            fc = color_beam)
        ax.add_patch(e)
    if nucleus!=None:
        e2 = patches.Ellipse(xy = (0, 0),
                             width = nucleus,
                             height = nucleus,
                             angle = 0,
                             fill = False,
                             edgecolor = "black",
                             alpha = 0.5,
                             #ls = ":",
                             lw = 5)
        ax.add_patch(e2)
    plt.grid()
    plt.savefig(dir_data + output, dpi = 100)


def fits2eps_phangs(dir_data, imagename_color, imagename_contour, ra_center,
        dec_center, title, colorbar_label, output, colorscale,
        colorlog = False, value = None, colorbar = False,
        contour = [0.1], color_contour = "k", color_beam = "b",
        xlim = ([-30, 30]), ylim = ([30, -30]), clim = None, nucleus=None, showbeam=True):
    """
    test
    """
    ra_center_define = (float(ra_center.split(":")[0]) \
                       + float(ra_center.split(":")[1]) / 60. \
                       + float(ra_center.split(":")[2]) / 3600. ) \
                       * 15.
    if dec_center.split(".")[0][0] == "-":
        dec_center_define = float(dec_center.split(".")[0]) \
                            - float(dec_center.split(".")[1]) / 60. \
                            - float(dec_center.split(".")[2] + "." + dec_center.split(".")[3]) / 3600.
    else:
        dec_center_define = float(dec_center.split(".")[0]) \
                            + float(dec_center.split(".")[1]) / 60. \
                            + float(dec_center.split(".")[2] + "." + dec_center.split(".")[3]) / 3600.
    image_file = dir_data + imagename_color
    datamax = imhead(image_file, "list")["datamax"]
    hdu_list = fits.open(image_file)
    ra_imagecenter = hdu_list[0].header["CRVAL1"]
    dec_imagecenter = hdu_list[0].header["CRVAL2"]
    ra_pixsize = abs(hdu_list[0].header["CDELT1"]) * 3600
    dec_pixsize = abs(hdu_list[0].header["CDELT2"]) * 3600
    print(ra_pixsize, dec_pixsize)
    ra_pixcenter = hdu_list[0].header["CRPIX1"]
    dec_pixcenter = hdu_list[0].header["CRPIX2"]
    dec_newcenter_offset = (dec_imagecenter - dec_center_define) \
                           * 3600 / dec_pixsize
    ra_newcenter_offset = (ra_imagecenter - ra_center_define) \
                           * 3600 / ra_pixsize
    ra_newcenter = ra_pixcenter - ra_newcenter_offset
    dec_newcenter = dec_pixcenter - dec_newcenter_offset
    ra_size = hdu_list[0].header["NAXIS1"]
    dec_size = hdu_list[0].header["NAXIS2"]
    image_data = hdu_list[0].data[:,:] # .data[0,0,:,:] # .data[:,:]
    xmin_col = (+ 0.5 - ra_newcenter) * ra_pixsize
    xmax_col = (ra_size + 0.5 - ra_newcenter) * ra_pixsize
    ymin_col = (+ 1.5 - dec_newcenter) * dec_pixsize
    ymax_col = (dec_size + 1.5 - dec_newcenter) * dec_pixsize
    xmin_cnt = (+ 1.0 - ra_newcenter) * ra_pixsize
    xmax_cnt = (ra_size + 1.0 - ra_newcenter) * ra_pixsize
    ymin_cnt = (+ 1.0 - dec_newcenter) * dec_pixsize
    ymax_cnt = (dec_size + 1.0 - dec_newcenter) * dec_pixsize
    plt.figure()
    plt.rcParams["font.size"] = 14
    if colorlog == True:
        plt.imshow(image_data,
                   norm = LogNorm(vmin = 0.02 * datamax,
                                  vmax = datamax),
                   cmap = colorscale,
                   extent = [xmin_col, xmax_col, ymin_col, ymax_col])
    else:
        plt.imshow(image_data,
                   cmap = colorscale,
                   extent = [xmin_col, xmax_col, ymin_col, ymax_col])
    plt.xlim(xlim)
    plt.ylim(ylim)
    if clim != None:
        plt.clim(clim)
    plt.title(title)
    plt.xlabel("x-offset (arcsec)")
    plt.ylabel("y-offset (arcsec)")
    if colorbar == True:
        cbar = plt.colorbar()
        cbar.set_label(colorbar_label)
    contour_file = dir_data + imagename_contour
    hdu_contour = fits.open(contour_file)
    contour_data = hdu_contour[0].data[:,:] # .data[0,0,:,:] # .data[:,:]
    if value != None:
        value_contour = value
    else:
        value_contour = imhead(contour_file, "list")["datamax"]
    contour2 = map(lambda x: x * value_contour, contour)
    plt.contour(contour_data, levels = contour2,
                extent = [xmin_cnt, xmax_cnt, ymax_cnt, ymin_cnt],
                colors = color_contour, linewidths = [0.5])
    if showbeam==True:
        bmaj = imhead(image_file, "list")["beammajor"]["value"]
        bmin = imhead(image_file, "list")["beamminor"]["value"]
        bpa = imhead(image_file, "list")["beampa"]["value"]
        ax = plt.axes()
        e = patches.Ellipse(xy = (min(xlim) * 0.8,
                                  max(ylim) * 0.8),
                            width = bmin,
                            height = bmaj,
                            angle = bpa * -1,
                            fc = color_beam)
        ax.add_patch(e)
    if nucleus!=None:
        e2 = patches.Ellipse(xy = (0, 0),
                             width = nucleus,
                             height = nucleus,
                             angle = 0,
                             fill = False,
                             edgecolor = "black",
                             alpha = 0.5,
                             #ls = ":",
                             lw = 5)
        ax.add_patch(e2)
    #plt.grid()
    plt.savefig(dir_data + output, dpi = 100)

"""
def pv_rotate(dir_data, imagename, pa):
    myia.close()
    myia.summary()
    output = dir_data + imagename + ".rotated"
    os.system("rm -rf " + output)
    myia.open(dir_data + imagename)
    myia.summary()
    myia.rotate(pa = "40deg", outfile = output)
    myia.close()
    myia.summary()



def pv_slice(dir_data, imagename, blc, trc):
    myia.close()
    myia.summary()
    mybox = myrg.box(blc = blc, trc = trc)
    output = dir_data + imagename + ".pv"
    os.system("rm -rf " + output)
    myia.open(dir_data + imagename)
    myia.summary()
    rebin_bin = [trc[0] - blc[0] + 1, 1, 1, 1]
    myia.rebin(region = mybox,
               outfile = output,
               bin = rebin_bin,
               dropdeg = True)
    myia.close()
    myia.summary()
"""


