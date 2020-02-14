import os
import re
import sys
import glob
import scipy
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.patches as patches
from astropy.io import fits
import analysisUtils as aU
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim

dir_data = "../../ngc3110/ana/product/fits/"
ra_center = "10:04:02.090"
dec_center = "-6.28.29.604"
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
xlim = [-30, 30]
ylim = [30, -30]
value = None
imagename_contour = "line_12co10_contsub_clean20_nat.regrid.immath.moment0.fits"
imagename_color = "line_12co10_contsub_clean20_nat.regrid.immath.moment0.fits"
contour = contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "Aperture Positions on $^{12}$CO (1-0) Map"
colorscale = "PuBu"
color_contour = "lightgrey"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/12co10_m0_ann.eps"

ann_aperture = "../../other/region23.txt"

#####################
### Main Procedure
#####################

def fits2eps_ann(dir_data, imagename_color, imagename_contour,
                 ra_center, dec_center, title, colorbar_label,
                 output, colorscale, colorlog = False, value = None, colorbar = False, contour = [0.1],
                 color_contour = "k", color_beam = "b",
                 xlim = ([-30, 30]), ylim = ([30, -30]),
                 clim = None, ann_aperture = ann_aperture):
    """
    test
    """
    ra_center_define = (float(ra_center.split(":")[0]) \
                        + float(ra_center.split(":")[1]) / 60. \
                        + float(ra_center.split(":")[2]) / 3600. ) \
        * 15.
    if float(dec_center.split(".")[0]) < 0:
        dec_center_define = float(dec_center.split(".")[0]) \
            - float(dec_center.split(".")[1]) / 60. \
            - float(dec_center.split(".")[2]) / 3600.
    else:
        dec_center_define = float(dec_center.split(".")[0]) \
            + float(dec_center.split(".")[1]) / 60. \
            + float(dec_center.split(".")[2]) / 3600.
    image_file = dir_data + imagename_color
    datamax = imhead(image_file, "list")["datamax"]
    hdu_list = fits.open(image_file)
    ra_imagecenter = hdu_list[0].header["CRVAL1"]
    dec_imagecenter = hdu_list[0].header["CRVAL2"]
    ra_pixsize = round(abs(hdu_list[0].header["CDELT1"]) * 3600, 2)
    dec_pixsize = round(abs(hdu_list[0].header["CDELT2"]) * 3600, 2)
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
    image_data = hdu_list[0].data[0,0,:,:]
    xmin = -ra_newcenter * ra_pixsize
    xmax = (ra_size - 1 - ra_newcenter) * ra_pixsize
    ymin = -dec_newcenter * dec_pixsize
    ymax = (dec_size - 1 - dec_newcenter) * dec_pixsize
    plt.figure()
    plt.rcParams["font.size"] = 14
    if colorlog == True:
        plt.imshow(image_data,
                   norm = LogNorm(vmin = 0.02 * datamax,
                                  vmax = datamax),
                   cmap = colorscale,
                   extent = [xmin, xmax, ymin, ymax])
    else:
        plt.imshow(image_data,
                   cmap = colorscale,
                   extent = [xmin, xmax, ymin, ymax])
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
    contour_data = hdu_contour[0].data[0,0,:,:]
    if value != None:
        value_contour = value
    else:
        value_contour = imhead(contour_file, "list")["datamax"]
    contour2 = map(lambda x: x * value_contour, contour)
    plt.contour(contour_data, levels = contour2,
                extent = [xmin, xmax, ymax, ymin],
                colors = color_contour)
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
    # annotation
    anns = []
    apertures = np.loadtxt(dir_data + ann_aperture,dtype = "S10")
    for i in range(len(apertures)):
        ra_ann = (float(apertures[:,1][i].split(":")[0]) \
                  + float(apertures[:,1][i].split(":")[1]) / 60. \
                  + float(apertures[:,1][i].split(":")[2]) / 3600. ) \
                  * 15.
        if float(apertures[:,2][i].split(".")[0]) < 0:
            dec_ann = float(apertures[:,2][i].split(".")[0]) \
                - float(apertures[:,2][i].split(".")[1]) / 60. \
                - float(apertures[:,2][i].split(".")[2]) / 3600.
        else:
            dec_ann = float(apertures[:,2][i].split(".")[0]) \
                + float(apertures[:,2][i].split(".")[1]) / 60. \
                + float(apertures[:,2][i].split(".")[2]) / 3600.
        ra_ann_rel = (ra_center_define - ra_ann) * 3600.
        dec_ann_rel = (dec_center_define - dec_ann) * 3600.
        anns.append([ra_ann_rel, dec_ann_rel])
    ax2 = plt.axes()
    c1 = patches.Circle(xy = (anns[0][0], anns[0][1]),
                        radius = 1.5, fc = "pink")
    c2 = patches.Circle(xy = (anns[1][0], anns[1][1]),
                        radius = 1.5, fc = "pink")
    c3 = patches.Circle(xy = (anns[2][0], anns[2][1]),
                        radius = 1.5, fc = "pink")
    c4 = patches.Circle(xy = (anns[3][0], anns[3][1]),
                        radius = 1.5, fc = "pink")
    c5 = patches.Circle(xy = (anns[4][0], anns[4][1]),
                        radius = 1.5, fc = "pink")
    c6 = patches.Circle(xy = (anns[5][0], anns[5][1]),
                        radius = 1.5, fc = "pink")
    c7 = patches.Circle(xy = (anns[6][0], anns[6][1]),
                        radius = 1.5, fc = "pink")
    c8 = patches.Circle(xy = (anns[7][0], anns[7][1]),
                        radius = 1.5, fc = "pink")
    c9 = patches.Circle(xy = (anns[8][0], anns[8][1]),
                        radius = 1.5, fc = "pink")
    c10 = patches.Circle(xy = (anns[9][0], anns[9][1]),
                        radius = 1.5, fc = "pink")
    c11 = patches.Circle(xy = (anns[10][0], anns[10][1]),
                        radius = 1.5, fc = "pink")
    c10 = patches.Circle(xy = (anns[9][0], anns[9][1]),
                        radius = 1.5, fc = "pink")
    c11 = patches.Circle(xy = (anns[10][0], anns[10][1]),
                        radius = 1.5, fc = "pink")
    c12 = patches.Circle(xy = (anns[11][0], anns[11][1]),
                        radius = 1.5, fc = "pink")
    c13 = patches.Circle(xy = (anns[12][0], anns[12][1]),
                        radius = 1.5, fc = "pink")
    c14 = patches.Circle(xy = (anns[13][0], anns[13][1]),
                        radius = 1.5, fc = "pink")
    c15 = patches.Circle(xy = (anns[14][0], anns[14][1]),
                        radius = 1.5, fc = "pink")
    c16 = patches.Circle(xy = (anns[15][0], anns[15][1]),
                        radius = 1.5, fc = "pink")
    c17 = patches.Circle(xy = (anns[16][0], anns[16][1]),
                        radius = 1.5, fc = "pink")
    c18 = patches.Circle(xy = (anns[17][0], anns[17][1]),
                        radius = 1.5, fc = "pink")
    c19 = patches.Circle(xy = (anns[18][0], anns[18][1]),
                        radius = 1.5, fc = "pink")
    c20 = patches.Circle(xy = (anns[19][0], anns[19][1]),
                        radius = 1.5, fc = "pink")
    c21 = patches.Circle(xy = (anns[20][0], anns[20][1]),
                        radius = 1.5, fc = "pink")
    c22 = patches.Circle(xy = (anns[21][0], anns[21][1]),
                        radius = 1.5, fc = "pink")
    c23 = patches.Circle(xy = (anns[22][0], anns[22][1]),
                        radius = 1.5, fc = "pink")
    ax2.add_patch(c1)
    ax2.add_patch(c2)
    ax2.add_patch(c3)
    ax2.add_patch(c4)
    ax2.add_patch(c5)
    ax2.add_patch(c6)
    ax2.add_patch(c7)
    ax2.add_patch(c8)
    ax2.add_patch(c9)
    ax2.add_patch(c10)
    ax2.add_patch(c11)
    ax2.add_patch(c12)
    ax2.add_patch(c13)
    ax2.add_patch(c14)
    ax2.add_patch(c15)
    ax2.add_patch(c16)
    ax2.add_patch(c17)
    ax2.add_patch(c18)
    ax2.add_patch(c19)
    ax2.add_patch(c20)
    ax2.add_patch(c21)
    ax2.add_patch(c22)
    ax2.add_patch(c23)
    plt.text(anns[0][0] + 2., anns[0][1], "1")
    plt.text(anns[1][0] + 2., anns[1][1], "2")
    plt.text(anns[2][0] + 2., anns[2][1] + 0.5, "3")
    plt.text(anns[3][0] + 2., anns[3][1] + 0.5, "4")
    plt.text(anns[4][0] + 2., anns[4][1] + 0.5, "5")
    plt.text(anns[5][0] + 2., anns[5][1] + 0.5, "6")
    plt.text(anns[6][0] + 2., anns[6][1] + 1., "7")
    plt.text(anns[7][0] + 2., anns[7][1] + 1., "8")
    plt.text(anns[8][0] + 2., anns[8][1] + 1., "9")
    plt.text(anns[9][0] - 1., anns[9][1] + 3.5, "10")
    plt.text(anns[10][0] + 1., anns[10][1] - 1., "11")
    plt.text(anns[11][0] + 1., anns[11][1] - 1., "12")
    plt.text(anns[12][0] - 1., anns[12][1] - 2.5, "13")
    plt.text(anns[13][0] - 3.5, anns[13][1] - 1.5, "14")
    plt.text(anns[14][0] - 4.5, anns[14][1] - 0.5, "15")
    plt.text(anns[15][0] - 4.5, anns[15][1] - 0.5, "16")
    plt.text(anns[16][0] - 4.5, anns[16][1] - 0.5, "17")
    plt.text(anns[17][0] - 4.5, anns[17][1] - 0.5, "18")
    plt.text(anns[18][0] - 4.5, anns[18][1] - 0.5, "19")
    plt.text(anns[19][0] - 4.5, anns[19][1] - 0.5, "20")
    plt.text(anns[20][0] - 4.5, anns[20][1] + 2., "21")
    plt.text(anns[21][0] - 4.5, anns[21][1] + 2., "22")
    plt.text(anns[22][0] - 4.5, anns[22][1] + 2., "23")
    plt.savefig(dir_data + output, dpi = 30)



fits2eps_ann(dir_data = dir_data,
             imagename_color = imagename_color,
             imagename_contour = imagename_contour,
             ra_center = ra_center,
             dec_center = dec_center,
             title = title,
             colorbar_label = colorbar_label,
             output = output,
             colorscale = colorscale,
             colorlog = colorlog,
             color_contour = color_contour,
             color_beam = color_beam,
             colorbar = colorbar,
             value = value,
             contour = contour,
             xlim = xlim,
             ylim = ylim)

