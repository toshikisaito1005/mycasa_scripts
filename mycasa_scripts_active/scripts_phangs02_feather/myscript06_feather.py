import numpy as np
import os
import glob
sys.path.append(os.getcwd())
import toolsPhangs02Feather as tl

dir_data = "/Users/saito/data/myproj_published/proj_phangs02_feather/" # laptop
#dir_data = "../" # astro-node7
projects = ["test06","test07"]
beamsize = "2.5arcsec"
tpbeam = "28.615arcsec"


###############################
### main
###############################
for i in range(len(projects)):
    dir_current = dir_data + projects[i] + "/"
    intimage_tmp = glob.glob(dir_current + projects[i] + "*_12m+7m_br.image")[0]
    intpbimage = glob.glob(dir_current + projects[i] + "*_12m+7m_br.pb")[0]
    tpimage_tmp = glob.glob(dir_data + "data_model/*tpimage*")[0]
    skymodel_tmp=glob.glob(dir_current+projects[i]+".alma.cycle5.1.skymodel.flat")[0]

    # regrid tp image
    tpimage_tmp2 = dir_current + tpimage_tmp.split("/")[-1] + ".regrid_tmp"
    os.system("rm -rf " + tpimage_tmp2)
    imregrid(imagename=tpimage_tmp,template=intimage_tmp,output=tpimage_tmp2)
    
    tpimage = dir_current + tpimage_tmp.split("/")[-1] + ".regrid"
    os.system("rm -rf " + tpimage)
    imtrans(imagename=tpimage_tmp2,outfile=tpimage,order="0132")
    os.system("rm -rf " + tpimage_tmp2)
    
    # cut tp image at pb = 0.25
    tpimage_cut = tpimage + ".cut"
    os.system("rm -rf " + tpimage_cut)
    immath(imagename = [intpbimage,tpimage],
           expr = "iif(IM0>=0.25,IM1,0.0)",
           outfile = tpimage_cut)

    tl.addbeamheader_round(tpimage_cut,tpbeam)

    # round the INT beam
    intimage_tmp2 = intimage_tmp.replace(".image",".smooth_tmp")
    os.system("rm -rf " + intimage_tmp2)
    imsmooth(imagename = intimage_tmp,
             targetres = True,
             major = beamsize,
             minor = beamsize,
             pa = "0deg",
             outfile = intimage_tmp2)

    intimage = intimage_tmp.replace(".image",".smooth")
    os.system("rm -rf " + intimage)
    immath(imagename = [intpbimage,intimage_tmp2],
           expr = "iif(IM0>=0.25,IM1,0.0)",
           outfile = intimage)
    os.system("rm -rf " + intimage_tmp2)

    tl.addbeamheader_round(intimage,beamsize)

    # skymodel
    skymodel = skymodel_tmp.replace(".flat",".smooth_tmp")
    os.system("rm -rf " + skymodel)
    imsmooth(imagename = skymodel_tmp,
             targetres = True,
             major = beamsize,
             minor = beamsize,
             pa = "0deg",
             outfile = skymodel)

    os.system("rm -rf " + skymodel + ".fits")
    exportfits(imagename=skymodel,fitsimage=skymodel+".fits")

    os.system("rm -rf " + skymodel)
    importfits(fitsimage = skymodel + ".fits",
               imagename = skymodel,
               defaultaxes=True,
               defaultaxesvalues=["RA","Dec","100GHz","Stokes"])
    os.system("rm -rf " + skymodel + ".fits")

    skymodel2 = skymodel_tmp.replace(".flat",".smooth_tmp2")
    os.system("rm -rf " + skymodel2)
    imregrid(imagename = skymodel,
             template = intpbimage,
             output = skymodel2)

    skymodel3 = skymodel_tmp.replace(".flat",".smooth")
    os.system("rm -rf " + skymodel3)
    immath(imagename = [skymodel2,intpbimage],
           expr = "iif(IM1>=0.25,IM0,0.0)",
           outfile = skymodel3)
    os.system("rm -rf " + skymodel + " " + skymodel2)
    
    imhead(imagename = skymodel3,
           mode = "put",
           hdkey = "beammajor",
           hdvalue= beamsize)
        
    imhead(imagename = skymodel3,
           mode = "put",
           hdkey = "beamminor",
           hdvalue= beamsize)
    
    makemask(mode="delete", inpmask=skymodel3+":mask0")

    # add stokes axes to the tpimage
    os.system("rm -rf " + tpimage + ".fits")
    exportfits(imagename=tpimage,fitsimage=tpimage+".fits")

    os.system("rm -rf " + tpimage)
    importfits(fitsimage = tpimage + ".fits",
               imagename = tpimage,
               defaultaxes=True,
               defaultaxesvalues=["RA","Dec","Frequency","Stokes"])
    os.system("rm -rf " + tpimage + ".fits")

    # FeatherFirst and PbcorrFirst with full TP
    output_ff = tl.FeatherFirst(intimage_tmp,
                                intimage,
                                tpimage,
                                intpbimage,
                                beamsize,
                                tpbeam,
                                1.0,
                                -1,
                                "sd1p0")
    output_pf = tl.PbcorrFirst(intimage_tmp,
                               intimage,
                               tpimage,
                               intpbimage,
                               beamsize,
                               1.0,
                               -1,
                               "sd1p0")

    # FeatherFirst and PbcorrFirst with cut TP
    output_ff_cut = tl.FeatherFirst(intimage_tmp,
                                    intimage,
                                    tpimage_cut,
                                    intpbimage,
                                    beamsize,
                                    tpbeam,
                                    1.0,
                                    -1,
                                    "sd1p0_tpcut")
    output_pf_cut = tl.PbcorrFirst(intimage_tmp,
                                   intimage,
                                   tpimage_cut,
                                   intpbimage,
                                   beamsize,
                                   1.0,
                                   -1,
                                   "sd1p0_tpcut")

    # compare with convolved model
    outfile0 = intimage + ".pbcor.diff" # intimage diff
    os.system("rm -rf " + outfile0)
    immath(imagename = [intimage+".pbcor",skymodel3,intpbimage],
           expr = "iif(IM2>=0.25,IM0-IM1,0.0)",
           outfile = outfile0)
    
    makemask(mode="delete", inpmask=output_ff+":mask0")
    outfile1 = output_ff.replace(".image",".diff")
    os.system("rm -rf " + outfile1)
    immath(imagename = [output_ff,skymodel3,intpbimage],
           expr = "iif(IM2>=0.25,IM0-IM1,0.0)",
           outfile = outfile1)

    makemask(mode="delete", inpmask=output_pf+":mask0")
    outfile2 = output_pf.replace(".image",".diff")
    os.system("rm -rf " + outfile2)
    immath(imagename = [output_pf,skymodel3,intpbimage],
           expr = "iif(IM2>=0.25,IM0-IM1,0.0)",
           outfile = outfile2)

    makemask(mode="delete", inpmask=output_pf_cut+":mask0")
    outfile3 = output_pf_cut.replace(".image",".diff")
    os.system("rm -rf " + outfile3)
    immath(imagename = [output_pf_cut,skymodel3,intpbimage],
           expr = "iif(IM2>=0.25,IM0-IM1,0.0)",
           outfile = outfile3)

    #os.system("rm -rf " + tpimage + " " + tpimage_cut)

os.system("rm -rf *.last")
