import numpy as np
import os
import glob
import pyfits
import shutil

dir_data = "../"
projects = ["test05"]

####################
### main
####################
os.system("rm -rf " + dir_data + "test00")
skymodel = glob.glob(dir_data+"data/*.skymodel")[0]
tpmodel = glob.glob(dir_data+"data/*.tpimage")[0]
galname = skymodel.split("/")[-1].split("_")[0]

for i in range(len(projects)):
    print("### working on " + projects[i])
    os.system("rm -rf " + projects[i] + " " + dir_data + projects[i])

    print("# 12m array...")
    ptgfile = projects[i] + ".alma.cycle5.1.ptg.txt"
    num_mosaic = len(np.loadtxt(ptgfile,dtype="S30")[:,0])
    totaltime = str(num_mosaic*10) + "s"
    simobserve(antennalist = "alma.cycle5.1.cfg",
               skymodel = skymodel,
               project = projects[i],
               indirection = "",
               incell = "",
               mapsize = ["",""],
               incenter = "",
               inbright = "",
               setpointings = False,
               ptgfile = ptgfile,
               graphics = "none",
               obsmode = "int",
               totaltime = totaltime,
               pointingspacing = "0.5PB",
               #thermalnoise = "",
               overwrite = True)

    print("# 7m array...")
    ptgfile = projects[i] + ".aca.cycle5.ptg.txt"
    num_mosaic = len(np.loadtxt(ptgfile,dtype="S30")[:,0])
    totaltime = str(num_mosaic*30) + "s"
    simobserve(antennalist = "aca.cycle5.cfg",
               skymodel = skymodel,
               project = projects[i],
               indirection = "",
               incell = "",
               mapsize = ["",""],
               incenter = "",
               inbright = "",
               setpointings = False,
               ptgfile = ptgfile,
               graphics = "none",
               obsmode = "int",
               totaltime = totaltime,
               pointingspacing = "0.4arcmin",
               #thermalnoise = "",
               overwrite = True)

    os.system("mv " + projects[i] + " " + dir_data)

os.system("rm -rf *.last")
