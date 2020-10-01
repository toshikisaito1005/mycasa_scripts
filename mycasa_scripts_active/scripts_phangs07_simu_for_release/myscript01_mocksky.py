import os
import sys
import glob
import numpy as np
from astropy.coordinates import SkyCoord


dir_project = "/Users/saito/data/myproj_active/proj_phangs07_simu_for_release/"
project_name = "sim_images"
tpbeam = "28.6arcsec"


##############################
### main
##############################
###
this_project = dir_project + project_name + "/"
os.system("rm -rf " + this_project)
os.system("rm -rf " + this_project + ".*")
os.system("mkdir " + this_project)


###
#
imagename = this_project + "simulated_sky.image"
#direction_center = "J2000 12h21m54.947s 4d28m15.258s"
direction_left   = "J2000 12h21m55.280s 4d28m15.258s"
direction_right  = "J2000 12h21m54.614s 4d28m15.258s"
#
os.system("rm -rf " + imagename)
os.system("rm -rf " + imagename.replace(".image",".fits"))
#
cl.done()
cl.addcomponent(dir=direction_left, flux= 0.07, fluxunit="Jy", freq="230.53800GHz", shape="point")
#cl.addcomponent(dir=direction_center, flux=0.05, fluxunit="Jy", freq="230.53800GHz", shape="point")
cl.addcomponent(dir=direction_right, flux=0.03, fluxunit="Jy", freq="230.53800GHz", shape="point")
ia.fromshape(imagename,[imsize,imsize,1,1],overwrite=True)
cs=ia.coordsys()
cs.setunits(['rad','rad','','Hz'])
cell_rad=qa.convert(qa.quantity("0.25arcsec"),"rad")['value']
cs.setincrement([-cell_rad,cell_rad],'direction')
cs.setreferencevalue([qa.convert("185.47894583deg",'rad')['value'],
                      qa.convert("4.47090500deg",'rad')['value']],
                     type="direction")
cs.setreferencevalue("230GHz",'spectral')
cs.setincrement('0.5GHz','spectral')
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
ia.done()
cl.done()
exportfits(imagename=imagename,fitsimage=imagename.replace(".image",".fits"),overwrite=True)
os.system("rm -rf " + imagename)
importfits(fitsimage=imagename.replace(".image",".fits"),imagename=imagename,overwrite=True)

os.system("rm -rf *.last")
