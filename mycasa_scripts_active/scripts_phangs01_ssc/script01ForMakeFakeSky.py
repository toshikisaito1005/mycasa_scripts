import os
import sys
import glob
import numpy as np

project = "../sim04"
project_name = "sim04"
do_steps = [1,2]

os.system("rm -rf " + project)
os.system("rm -rf " + project + ".*")

if 0 in do_steps:
    imagename = "ngc4303_caf/ngc4303_7m+tp+caf_co21_na.image_Jyperpixel"

if 1 in do_steps:
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

if 2 in do_steps:

    default(simalma)
    project            =  "sim02"
    dryrun             =  False
    skymodel           =  "../"+project_name+"/disk_model1.image"
    inbright           =  ""
    indirection        =  ""
    incell             =  ""
    incenter           =  ""
    inwidth            =  ""
    complist           =  ""
    compwidth          =  "8GHz"
    setpointings       =  True
    ptgfile            =  "$project.ptg.txt"
    integration        =  "10s"
    direction          =  ""
    mapsize            =  ""
    antennalist        =  "aca.cycle5.cfg"
    hourangle          =  "transit"
    totaltime          =  "4h"
    tpnant             =  4
    tptime             =  "8h"
    pwv                =  0.5
    image              =  True
    imsize             =  0
    imdirection        =  ""
    cell               =  ""
    niter              =  0
    threshold          =  "0.1mJy"
    graphics           =  "file"
    verbose            =  False
    overwrite          =  True
    simalma()

    imagename = project+"/"+project+".aca.tp.skymodel"
    bmaj = imhead(project+"/"+project+".sd.image",mode="list")["beammajor"]["value"]
    os.system("rm -rf " + imagename + ".smooth")
    imsmooth(imagename = imagename,
             major = str(bmaj)+"arcsec",
	     minor = str(bmaj)+"arcsec",
	     pa = "0deg",
	     outfile = imagename + ".smooth")

    # tp2vis
    execfile("tp2vis.py")
    tp2vis(project+"/"+project+".aca.tp.skymodel.smooth",
           "../"+project_name+"/"+project_name+".tp.sd.ms",
	   "7m.ptg",
	   rms=0.1)

    os.system("mv "+project+"/sim02.aca.cycle5.ms ../"+project_name+"/"+project_name+".aca.cycle5.ms")
    os.system("mv "+project+"/sim02.aca.cycle5.noisy.ms ../"+project_name+"/"+project_name+".aca.cycle5.noisy.ms")
    os.system("mv "+project+"/"+project+".aca.tp.skymodel.smooth"+" ../"+project_name+"/"+project_name+".sd.skymodel")

