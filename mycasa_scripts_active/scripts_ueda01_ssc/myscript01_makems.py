import os
import glob
import numpy as np
sys.path.append(os.getcwd())
import toolsJu01Ssc as tl

##############################
### parameter setup
##############################
dir_proj = "/Users/saito/data/myproj_published/proj_ju01_ssc/"
#dir_proj = "../"

galaxy = ["am2038"]
#galaxy = ["am0956","am1158","am1255","am1300","am2038"
#          "am2055","arp230","ngc3597","ngc7135"]


##############################
### def
##############################
def eazy_mstransform(vis,outputvis,excludechans,array,nchan,start,width):
    os.system("rm -rf " + outputvis)
    os.system("cp -r " + vis + " " + outputvis)
    spw = str(tl.find_spw_co10(vis))
    statwt(vis = outputvis,
           spw = spw,
           excludechans = spw + ":" + excludechans,
           datacolumn = "data")

    regrid_array = dir_working + galname + "_"+array+".ms"
    print("# mstransform "+array+" ms")
    os.system("rm -rf " + regrid_array)
    mstransform(vis = outputvis,
                outputvis = regrid_array,
                spw = spw,
                regridms = True,
                mode = "velocity",
                nchan = nchan,
                start = start,
                width = width,
                restfreq = "115.27120GHz",
                outframe = "LSRK",
                datacolumn = "data")

    os.system("rm -rf " + outputvis + "*")

    return regrid_array


##############################
### main
##############################
dir_working = dir_proj + "data_msfiles/"
done = glob.glob(dir_working)
if not done:
    os.mkdir(dir_working)

### preparartion
for i in range(len(galaxy)):
    ### import keys
    galname = galaxy[i]
    tplinechans,tp2viswt_value,exclude_7m,exclude_12m = tl.know_makems_keys(galname)
    vis_12m, vis_7m, image_tp = tl.know_rawdata_keys(galname)
    nchan, start, width = tl.know_imaging_keys(galname)

    ### tp2vis part
    # measure noise rms per channel
    tpimage = dir_proj + "data_raw/" + image_tp
    chan_end = str(imhead(tpimage,"list")["shape"][3] - 2)
    chan_free_left = "1~" + tplinechans.split("~")[0]
    chan_free_right = tplinechans.split("~")[1] + "~" + chan_end
    chans = chan_free_left + ";" + chan_free_right
    rms = imstat(tpimage,chans=chans,axes=[0,1])["rms"].mean() # Jy/beam per channel

    # create pointing file for tp interferometer
    vis = dir_proj + "data_raw/" + vis_12m
    ptgfile, sciencetarget = tl.know_pointings(vis,galname)

    # execute tp2vis
    execfile("tp2vis.py")
    vis_tp = dir_working + galname + "_tp.ms_tmp"
    tp2vis(tpimage,vis_tp,ptgfile,nvgrp=5,rms=rms,winpix=3)
    tp2viswt(vis_tp,mode="multiply",value=tp2viswt_value)
    os.system("rm -rf " + ptgfile)

    ### mstransform and concat part
    # tp ms
    regrid_tp = dir_working + galname + "_tp.ms"
    print("# mstransform tp ms")
    os.system("rm -rf " + regrid_tp)
    mstransform(vis = vis_tp,
                outputvis = regrid_tp,
                spw = "",
                regridms = True,
                mode = "velocity",
                nchan = nchan,
                start = start,
                width = width,
                restfreq = "115.27120GHz",
                outframe = "LSRK",
                datacolumn = "corrected")

    # 7m ms
    vis = dir_proj + "data_raw/" + vis_7m
    outputvis = dir_working + vis_7m
    regrid_7m = eazy_mstransform(vis,outputvis,exclude_7m,"7m",nchan,start,width)

    # 12m ms
    vis = dir_proj + "data_raw/" + vis_12m
    outputvis = dir_working + vis_12m
    regrid_12m = eazy_mstransform(vis,outputvis,exclude_12m,"12m",nchan,start,width)

    # concat 12m+7m+tp
    concatvis = dir_working + galname + "_12m7mtp.ms"
    os.system("rm -rf " + concatvis)
    concat(vis = [regrid_12m,regrid_7m,regrid_tp],
           concatvis = concatvis,
           freqtol = "10MHz",
           dirtol = "5arcsec")

    # concat 12m+7m
    concatvis = dir_working + galname + "_12m7m.ms"
    os.system("rm -rf " + concatvis)
    concat(vis = [regrid_12m,regrid_7m],
           concatvis = concatvis,
           freqtol = "10MHz",
           dirtol = "5arcsec")

    # plot uv data
    tp2vispl([regrid_tp,regrid_7m,regrid_12m],
             outfig = dir_working + galname + "_tp2viswt.png")

    os.system("rm -rf " + vis_tp)
    os.system("rm -rf " + regrid_tp)
    os.system("rm -rf " + regrid_7m)

os.system("rm -rf *.last")
