import os
import sys
import glob
import numpy as np
from astropy.coordinates import SkyCoord


dir_project = "/Users/saito/data/myproj_active/proj_phangs07_simu_for_release/"
project_name = "sim01"
tpbeam = "28.6arcsec"


##############################
### main
##############################
this_project = dir_project + this_project_name


os.system("rm -rf " + project)
os.system("rm -rf " + project + ".*")

imsize = 256
os.system("mkdir " + project)
imagename = project + "/disk_model1.image"
os.system("rm -rf " + imagename)
os.system("rm -rf " + imagename.replace(".image",".fits"))
direction = "ICRS 12h21m54.947s 4d28m15.258s"
cl.done()
cl.addcomponent(dir = direction,
                flux = 0.1 / 67. * float(imsize**2),
	    fluxunit = "Jy",
	    freq = "230.53800GHz",
	    shape = "Gaussian", 
                majoraxis = "5arcsec",
	    minoraxis = "5arcsec",
	    positionangle = "45.0deg")

cl.addcomponent(dir = direction,
                flux = 0.5 / 67. * float(imsize**2),
	    fluxunit = "Jy",
	    freq = "230.53800GHz",
	    shape = "Gaussian", 
                majoraxis = "30arcsec",
	    minoraxis = "10arcsec",
	    positionangle = "45.0deg")

cl.addcomponent(dir = direction,
                flux = 2.5 / 67. * float(imsize**2),
	    fluxunit = "Jy",
	    freq = "230.53800GHz",
	    shape = "Gaussian", 
                majoraxis = "120arcsec",
	    minoraxis = "40arcsec",
	    positionangle = "45.0deg")


ia.fromshape(imagename,[imsize,imsize,1,1],overwrite=True)
cs=ia.coordsys()
cs.setunits(['rad','rad','','Hz'])
cell_rad=qa.convert(qa.quantity("1.0arcsec"),"rad")['value']
cs.setincrement([-cell_rad,cell_rad],'direction')
cs.setreferencevalue([qa.convert("185.47894583deg",'rad')['value'],
                      qa.convert("4.47090500deg",'rad')['value']],
                     type="direction")
cs.setreferencevalue("230GHz",'spectral')
cs.setincrement('1GHz','spectral')
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
ia.done()
cl.done()
exportfits(imagename=imagename,fitsimage=imagename.replace(".image",".fits"),overwrite=True)
os.system("rm -rf " + imagename)
importfits(fitsimage=imagename.replace(".image",".fits"),imagename=imagename,overwrite=True)
