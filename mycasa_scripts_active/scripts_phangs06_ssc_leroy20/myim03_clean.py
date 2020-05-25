import os
import sys
import glob
import datetime
a=datetime.datetime.now()


dir_proj = "/Users/saito/data/myproj_active/proj_phangs06_ssc/sim_phangs/"


##############################
### def
##############################
def get_info(dir_sim,mosaic_def2,robust):
    galname = dir_sim.split("/")[-1]
    start = "" #mosaic_def[:,1][np.where(mosaic_def[:,0]==galname)[0][0]] + "km/s"
    ra = mosaic_def2[:,1][np.where(mosaic_def2[:,0]==galname)[0][0]]
    dec = mosaic_def2[:,2][np.where(mosaic_def2[:,0]==galname)[0][0]]
    if "h" not in ra:
        ra = ra + "deg"
    if "d" not in dec:
        dec = dec + "deg"

    if robust == 2.0:
        weighting = "natural"
        wt = "na"
    elif robust == -2.0:
        weighting = "uniform"
        wt = "un"
    else:
        weighting = "briggs"
        wt = "br"

    return galname, start, ra, dec, weighting, wt


##############################
### main
##############################
# get systemic velocity definition
mosaic_def = np.loadtxt("mosaic_definitions.txt",dtype="S20",usecols=(0,3))
mosaic_def = np.c_[[s.split("_")[0] for s in mosaic_def[:,0]],mosaic_def[:,1]]
mosaic_def2 = np.loadtxt("multipart_fields.txt",dtype="S20",usecols=(0,1,2))
mosaic_def2 = np.r_[np.loadtxt("mosaic_definitions.txt",dtype="S20",usecols=(0,1,2)),mosaic_def2]

#
dir_sim = glob.glob(dir_proj + "*")
dir_mask = dir_proj + "v3p3_hybridmask/"

#for i in range(len(dir_sim)):
for i in [0]:
    # define name
    galname,start,ra,dec,weighting,wt = def_name(dir_sim[i],mosaic_def2,robust)

