import numpy as np
import os
import glob
sys.path.append(os.getcwd())
import toolsPhangs02Feather as tl


dir_data = "/Users/saito/data/myproj_published/proj_phangs02_feather/"
#dir_data = "../"
projects = ["test06", "test07", "test0607_feather2merge", "test0607_merge2feather"]
beamsize = "2.5arcsec"


###############################
### main
###############################
dir_product = dir_data + "products/"
os.system("rm -rf " + dir_product)
os.mkdir(dir_product)

for i in range(len(projects)):
    dir_current = dir_data + projects[i] + "/"
    name_proj = projects[i].split("_")[0]
    
    intimage = glob.glob(dir_current + projects[i].split("_")[0] + "_*12m+7m*.pbcor")
    intdiff = glob.glob(dir_current + projects[i].split("_")[0] + "_*12m+7m*.diff")
    skymodel = glob.glob(dir_current + projects[i].split("_")[0] + "*skymodel.smooth")
    ffimages = glob.glob(dir_current + projects[i].split("_")[0] + "_*featherfirst*")
    pfimages = glob.glob(dir_current + projects[i].split("_")[0] + "_*pbcorrfirst*")
    intpb = glob.glob(dir_current + projects[i].split("_")[0] + "_*12m+7m*.pb")
    imagenames = np.r_[intimage,intdiff,ffimages,pfimages,skymodel,intpb]

    tl.createmask(intpb[0],0.25,dir_product+"test.mask")
    tl.createmask(skymodel,0.009,dir_product+"model.mask")
    makemask(mode="copy",
             inpimage=dir_product+"model.mask",
             inpmask=dir_product+"model.mask",
             output=dir_product+"model.mask:mask0")

    for j in range(len(imagenames)):
        productfile1 = dir_product + imagenames[j].split("/")[-1].replace(".pbcor","")
        productfile2 = productfile1.replace(".image","").replace(".alma.cycle5.1.","_")
        productfile = productfile2.replace(".smooth","_2p5") + ".image"

        os.system("rm -rf " + productfile)
        immath(imagename = [imagenames[j],dir_product+"test.mask"],
               expr = "iif(IM1>=0.5,IM0,0.0)",
               outfile = productfile)
        
        tl.addbeamheader_round(productfile,beamsize)

        os.system("rm -rf " + productfile.replace(".image",".image.clip"))
        immath(imagename = [imagenames[j],dir_product+"model.mask"],
               expr = "iif(IM1>=0.5,IM0,0.0)",
               outfile = productfile.replace(".image",".image.clip"))
               
        tl.addbeamheader_round(productfile.replace(".image",".image.clip"),beamsize)

        os.system("rm -rf " + productfile.replace(".image","_clip.fits"))
        exportfits(imagename = productfile.replace(".image",".image.clip"),
                   fitsimage = productfile.replace(".image","_clip.fits"))
    
        os.system("rm -rf " + productfile.replace(".image",".fits"))
        exportfits(imagename = productfile,
                   fitsimage = productfile.replace(".image",".fits"))

    os.system("rm -rf "+dir_product+"test.mask")
    os.system("rm -rf "+dir_product+"model.mask")

os.system("rm -rf *.last")
