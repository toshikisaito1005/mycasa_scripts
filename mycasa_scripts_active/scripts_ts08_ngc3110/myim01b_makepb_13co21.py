import os
import glob
import numpy as np
from astropy.coordinates import SkyCoord

dir_data = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/data/"
cube_13co21 = "ngc3110_alma_13co21_l20_na.cube.regrid"
chans = ""
project = "product_simobs"
pointing1 = "J2000 10:04:02.392 -6.28.45.039"
pointing2 = "J2000 10:04:02.077 -6.28.32.140"
pointing3 = "J2000 10:04:01.762 -6.28.19.241"
redshift = 0.016858
restfreq = 220.39868420 # GHz
productname = "ngc3110_alma_13co21_l20_na.flux.regrid"

#####################
### Main Procedure
#####################
# create ptg file
ptgfile = "ngc3110_band6_13co21.ptg"
os.system("rm -rf " + ptgfile)
f = open(ptgfile, "a")
f.write(pointing1 + "\n")
f.write(pointing2 + "\n")
f.write(pointing3 + "\n")
f.close()

# working directory
dir_working = dir_data + "../sim_13co21/"
os.system("rm -rf " + dir_working)
os.mkdir(dir_working)

# one channel extraction
cubename = glob.glob(dir_data + cube_13co21)[0]
channame = dir_working + "ngc3110_13co21.chan"
os.system("rm -rf " + channame)
immath(imagename = cubename,
       expr = "IM0",
       outfile = channame,
       chans = chans)

# simobserve
simobserve(antennalist = "alma.cycle5.1.cfg",
           skymodel = channame,
           project = project,
           indirection = "",
           incell = "",
           mapsize = ["",""],
           incenter = str(restfreq/(1 + redshift))+"GHz",
           inbright = "",
           setpointings = False,
           ptgfile = ptgfile,
           integration = "60s",
           graphics = "none",
           obsmode = "int",
           totaltime = "180s",
           #thermalnoise = "",
           overwrite = True)

os.system("rm -rf " + dir_working + project)
os.system("mv " + project + " " + dir_working)

# dirty map
vis = glob.glob(dir_working + project + "/*.ms")[0]
imagename = dir_working + "dirty_13co21"
os.system("rm -rf " + imagename + "*")
tclean(vis = vis,
       imagename = imagename,
       field = "",
       specmode = "cube",
       width = 1,
       start = "",
       niter = 0,
       interactive = False,
       imsize = 800,
       cell = "0.2arcsec",
       weighting = "briggs",
       robust = 0.5,
       gridder = "mosaic",
       deconvolver = "multiscale",
       scales = [0,2,5],
       nchan = -1,
       cycleniter = 50,
       usemask = "user",
       pblimit = 0.20)

imagename = dir_working + "dirty_13co21.pb"
output = dir_working + "dirty_13co21.pb.regrid"
imregrid(imagename = imagename,
         template = cubename,
         output = output,
         axes = [0,1])

os.system("rm -rf " + dir_data + productname)
os.system("mv " + dir_working + "dirty_13co21.pb.regrid " + dir_data + productname)

os.system("rm -rf *.last")
os.system("rm -rf " + dir_working)
