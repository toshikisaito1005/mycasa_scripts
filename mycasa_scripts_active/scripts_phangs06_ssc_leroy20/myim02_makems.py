import numpy as np
import os
import glob
import pyfits
import shutil


dir_project = "/Users/saito/data/myproj_active/proj_phangs06_ssc/"


##############################
### main
##############################
dir_sim = dir_project + "sim_phangs/"
os.system("rm -rf " + dir_sim)
os.mkdir(dir_sim)

skymodels = glob.glob(dir_project + "v3p4_tpeak/*.skymodel")
tpmodels = glob.glob(dir_project + "v3p4_tpeak/*.jypb.smooth")
skymodels.sort()
tpmodels.sort()


#for i in range(len(skymodels)):
for i in [0]:
    galname = skymodels[i].split("/")[-1].split("_12m")[0]
    dir_this = "sim_" + galname
    os.system("rm -rf " + dir_this)
    print("### working on " + galname + ", "+str(i)+"/"+str(len(skymodels) - 1))
    default('simobserve')
    antennalist        =  "aca.cycle5.cfg"
    skymodel           =  skymodels[i]
    project            =  dir_this
    indirection        =  ""
    incell             =  ""
    mapsize            =  ["",""]
    incenter           =  ""
    inbright           =  ""
    setpointings       =  True
    integration        =  "10s"
    graphics           =  "none"
    obsmode            = "int"
    totaltime          =  "4h"
    #thermalnoise       =  ""
    pointingspacing    =  "0.4arcmin"
    overwrite          =  True
    simobserve()






    #
    dir_simobs = dir_this
    dir_product = dir_this

    infile = tpmodels[i]
    fitsimage = tpmodels[i] + ".fits"
    os.system("rm -rf " + fitsimage)
    exportfits(fitsimage = fitsimage,
               imagename = infile)

    os.system("rm -rf " + infile)
    importfits(fitsimage = fitsimage,
               imagename = infile,
	       defaultaxes = True,
               defaultaxesvalues=["","","","I"])
    os.system("rm -rf " + fitsimage)
      
    # get pointing positions
    txtdata = dir_simobs + "sim_" + galname + ".aca.cycle5.ptg.txt"

    f = open(txtdata)
    data1 = f.read()
    f.close()
    lines1 = data1.split('\n')
    lines1.pop()
    lines1.pop(0)
    lines2 = [s.split("  ")[0] for s in lines1]
    f = open(txtdata.replace(".txt",""), "w")
    for i in lines2:
        f.write(i + "\n")                      
    f.close()

    """
    ms_aca = dir_simobs + "sim_" + galname + ".aca.cycle5.ms"
    listobs(ms_aca, listfile=ms_aca+".listobs")
    f = open(ms_aca+".listobs")
    data1 = f.read()
    f.close()
    lines1 = data1.split('\n')
    for j in lines1:
        if "Fields:" in j:
            index_f = lines1.index(j)
    lines2 = lines1[index_f+2:index_f+int(lines1[index_f].split(": ")[1])+2]
    lines3 = ["J2000 "+s.split("*")[1].split(" J2000  ")[0] for s in lines2]
    os.system("rm -rf " + ms_aca.replace(".ms",".ptg"))
    f = open(ms_aca.replace(".ms",".ptg"), "w")
    for i in lines3:
        f.write(i + "\n")
    f.close()
    """

    execfile('tp2vis.py')
    outfile = dir_simobs +  "sim_" + galname + ".sd.ms"
    ptgfile = txtdata.replace(".txt","")
    tp2vis(infile,outfile,ptgfile,nvgrp=5,rms=0.1,winpix=3)
    tp2viswt(outfile,mode='const',value=0.5)#12.**4/7.**4)

    ms_aca = "sim_" + galname + ".aca.cycle5.ms"
    ms_tp2vis = outfile
    im_tp2vis = "sim_" + galname + ".sd.tp2vis.input"

    os.system("rm -rf " + dir_product)
    os.system("mkdir " + dir_product)

    os.system("mv "+dir_simobs + ms_aca + " " + dir_product)
    os.system("mv "+dir_simobs + ms_aca.replace(".ms",".noisy.ms") + " " + dir_product)
    os.system("mv "+ms_tp2vis + " " + dir_product)
    os.system("cp -r "+infile + " " + dir_product + im_tp2vis)
    os.system("rm -rf sim_" + galname)
