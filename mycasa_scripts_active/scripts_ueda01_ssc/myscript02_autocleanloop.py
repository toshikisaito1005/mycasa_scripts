import os
import glob
sys.path.append(os.getcwd())
import toolsJu01Ssc as tl


##############################
### parameter setup
##############################
dir_ms = "/Users/saito/data/myproj_published/proj_ju01_ssc/data_msfiles/"
#dir_ms = "../data_msfiles/"

galaxy = ["am2038"]
#galaxy = ["am0956","am1158","am1255","am1300","am2038"
#          "am2055","arp230","ngc3597","ngc7135"]


##############################
### main
##############################
for i in range(len(galaxy)):
    ### import keys
    galname = galaxy[i]
    nchan, start, width, imsize, cell, pblimit, robust, rms \
        = tl.know_imaging_keys2(galname)

    ### auto msclean loop
    dirname_work = dir_ms + "../" + galname + "/"
    os.system("rm -rf " + dirname_work)
    os.mkdir(dirname_work)
    vislist = glob.glob(dir_ms + galname + "*.ms")

    # common imaging parameters
    field = ""
    spw = ""
    restfreq = "115.27120GHz"
    outframe = "LSRK"
    phasecenter = ""
    scales = [0,8,20]
    smallscalebias = 0.6
    deconvolver = "multiscale"
    gridder = "mosaic"
    uvtaper=[]

    for j in range(len(vislist)):
        vis = vislist[j]
        imagename = vis.split("/")[-1].replace(".ms","")

        print("### imaging " + imagename)
        execfile("scriptForAutoTclean.py")

#tp2vistweak

os.system("rm -rf *.last")
