import os
import sys
import glob
import datetime

a=datetime.datetime.now()


##############################
### main
##############################
# get systemic velocity definition
mosaic_def = np.loadtxt("mosaic_definitions.txt",dtype="S20",usecols=(0,3))
mosaic_def = np.c_[[s.split("_")[0] for s in mosaic_def[:,0]],mosaic_def[:,1]]

mosaic_def2 = np.loadtxt("multipart_fields.txt",dtype="S20",usecols=(0,1,2))
mosaic_def2 = np.r_[np.loadtxt("mosaic_definitions.txt",dtype="S20",usecols=(0,1,2)),mosaic_def2]
