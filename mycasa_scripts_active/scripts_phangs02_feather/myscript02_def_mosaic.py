import numpy as np
import os
import glob
import pyfits
import shutil

dir_data = "../"
project = "test00"

####################
### main
####################
skymodel = glob.glob(dir_data+"data/*.skymodel")[0]
tpmodel = glob.glob(dir_data+"data/*.tpimage")[0]
galname = skymodel.split("/")[-1].split("_")[0]

os.system("rm -rf " + "sim_" + galname)
simobserve(antennalist = "aca.cycle5.cfg",
           skymodel = skymodel,
           project = project,
           indirection = "",
           incell = "",
           mapsize = ["",""],
           incenter = "",
           inbright = "",
           setpointings = True,
           integration = "10s",
           graphics = "none",
           obsmode = "int",
           totaltime = "4h",
           pointingspacing = "0.4arcmin",
           #thermalnoise = "",
           overwrite = True)

simobserve(antennalist = "alma.cycle5.1.cfg",
           skymodel = skymodel,
           project = project,
           indirection = "",
           incell = "",
           mapsize = ["",""],
           incenter = "",
           inbright = "",
           setpointings = True,
           integration = "10s",
           graphics = "none",
           obsmode = "int",
           totaltime = "1h",
           pointingspacing = "0.5PB",
           #thermalnoise = "",
           overwrite = True)

os.system("mv " + project + " " + dir_data)
os.system("rm -rf *.last")
