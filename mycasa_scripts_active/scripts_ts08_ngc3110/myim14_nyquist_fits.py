import os
import sys
import re
import glob
import numpy as np
import scipy
import matplotlib.pyplot as plt


#####################
### function
#####################
def createfits(direction,data,data_ra,data_dec,output,pix,mode="Gauss"):
    cl.done()
    for i in range(len(data)):
        cl.addcomponent(dir=str(data_ra[i])+"deg, "+str(data_dec[i])+"deg",
                        flux=data[i],
                        fluxunit="Jy",
                        freq="234.6075GHz",
                        shape=mode,
                        majoraxis="3.00arcsec",
                        minoraxis="3.00arcsec",
                        positionangle="0.0deg")

    ia.fromshape(output,
                 [50,50,1,1],
                 overwrite = True)
    cs=ia.coordsys()
    cs.setunits(["rad","rad","","Hz"])
    cell_rad=qa.convert(qa.quantity(pix),"rad")["value"]
    cs.setincrement([-cell_rad,cell_rad],"direction")
    cs.setreferencevalue([qa.convert("151.008708deg", "rad")["value"],
                          qa.convert("-6.474890deg","rad")["value"]],
                         type = "direction")
    cs.setreferencevalue("234.6075GHz", "spectral")
    cs.setincrement("1GHz", "spectral")
    ia.setcoordsys(cs.torecord())
    ia.setbrightnessunit("Jy/pixel")
    ia.modify(cl.torecord(),subtract=False)
    ia.close()
    cl.done()


#####################
### Main Procedure
#####################
direction="J2000 10:04:02.090 -6.28.29.604"
pixel = "1.5arcsec"
dir_data = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/image_nyquist/"
txt_data = "ngc3110_params.txt"
data = np.loadtxt(dir_data + txt_data)
data_ra = data[:,0]
data_dec = data[:,1]
data_index = data[:,2]
data_sfr = data[:,3]
data_ssc = data[:,4]
data_columi = data[:,5]
data_sfe = data[:,6]

output = dir_data + "ngc3110_nyquist_index.image"
createfits(direction,data_index,data_ra,data_dec,output,pixel)

output = dir_data + "ngc3110_nyquist_sfr_density.image"
createfits(direction,data_sfr,data_ra,data_dec,output,pixel)

output = dir_data + "ngc3110_nyquist_ssc_density.image"
createfits(direction,data_ssc,data_ra,data_dec,output,pixel)

output = dir_data + "ngc3110_nyquist_co10_luminosity.image"
createfits(direction,data_columi,data_ra,data_dec,output,pixel)

output = dir_data + "ngc3110_nyquist_sfe.image"
createfits(direction,data_sfe,data_ra,data_dec,output,pixel)

#
txt_data = "ngc3110_radex_nH2.txt"
data = np.loadtxt(dir_data + txt_data)
data_radex = data[:,5]
output = dir_data + "ngc3110_nyquist_nH2.image"
createfits(direction,data_radex,data_ra,data_dec,output,pixel,mode="point")

#
txt_data = "ngc3110_radex_tkin.txt"
data = np.loadtxt(dir_data + txt_data)
data_radex = data[:,5]
output = dir_data + "ngc3110_nyquist_Tkin.image"
createfits(direction,data_radex,data_ra,data_dec,output,pixel,mode="point")

#
txt_data = "ngc3110_alpha_lte.txt"
data = np.loadtxt(dir_data + txt_data)
data_radex = data[:,3]
output = dir_data + "ngc3110_nyquist_alpha_lte_Trot.image"
createfits(direction,data_radex,data_ra,data_dec,output,pixel)

imagenames = glob.glob(dir_data + "*.image")
for i in range(len(imagenames)):
    imhead(imagename = imagenames[i],
           mode = "add",
           hdkey = "beammajor",
           hdvalue = "3.0arcsec")
    imhead(imagename = imagenames[i],
           mode = "add",
           hdkey = "beamminor",
           hdvalue = "3.0arcsec")
    os.system("rm -rf " + imagenames[i].replace(".image",".fits"))
    exportfits(imagename = imagenames[i],
               fitsimage = imagenames[i].replace(".image",".fits"))
    os.system("rm -rf " + imagenames[i])

os.system("rm -rf *.last")
