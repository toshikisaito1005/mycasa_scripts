import os
import sys
import glob
import numpy as np


# CASA imports
from taskinit import *
from immoments import immoments
from immath import immath
from makemask import makemask
from imhead import imhead
from imstat import imstat
from feather import feather
from exportfits import exportfits
import analysisUtils as aU


###############################
### def
###############################
def addbeamheader(imagename,major,minor,pa):
    imhead(imagename = imagename,
           mode = "put",
           hdkey = "beammajor",
           hdvalue= major)
        
    imhead(imagename = imagename,
           mode = "put",
           hdkey = "beamminor",
           hdvalue= minor)

    imhead(imagename = imagename,
           mode = "put",
           hdkey = "beampa",
           hdvalue= pa)


def addbeamheader_round(imagename,beamsize):
    imhead(imagename = imagename,
           mode = "put",
           hdkey = "beammajor",
           hdvalue= beamsize)
        
    imhead(imagename = imagename,
           mode = "put",
           hdkey = "beamminor",
           hdvalue= beamsize)


def FeatherFirst(intimage_tmp,
                 intimage,
                 tpimage,
                 intpbimage,
                 beamsize,
                 tpbeam,
                 sdfactor,
                 effdishdiam,
                 suffix):
    """
    Classical Feather
    """
    # FeatherFirst 1/3: depb tp image
    tpimage_depb = intimage_tmp.replace(".image",".tpimage.depb")
    os.system("rm -rf " + tpimage_depb)
    immath(imagename = [tpimage,intpbimage],
           expr = "iif(IM1>=0.25,IM0*IM1,0.0)",
           outfile = tpimage_depb)

    addbeamheader_round(tpimage_depb,tpbeam)

    # FeatherFirst 2/3: feather
    featherimage = intimage_tmp.replace(".image",".feather")
    feather(imagename = featherimage,
            highres = intimage,
            lowres = tpimage_depb,
            sdfactor = sdfactor,
            effdishdiam = effdishdiam,
            lowpassfiltersd = False)
    os.system("rm -rf " + tpimage_depb)

    # FeatherFirst 3/3: pbcorr feather image
    productimage = intimage_tmp.replace("12m+7m","featherfirst_"+suffix)
    os.system("rm -rf " + productimage)
    immath(imagename = [featherimage,intpbimage],
           expr = "iif(IM1>=0.25,IM0/IM1,0.0)",
           outfile = productimage)
    os.system("rm -rf " + featherimage)

    addbeamheader_round(productimage,beamsize)

    return productimage


def PbcorrFirst(intimage_tmp,
                intimage,
                tpimage,
                intpbimage,
                beamsize,
                sdfactor,
                effdishdiam,
                suffix):
    """
    Chris' feather
    """
    # PbcorrFirst 1/3: pbcorr int image
    intimage_pbcor = intimage + ".pbcor"
    os.system("rm -rf " + intimage_pbcor)
    immath(imagename = [intimage,intpbimage],
           expr = "iif(IM1>=0.25,IM0/IM1,0.0)",
           outfile = intimage_pbcor)

    addbeamheader_round(intimage_pbcor,beamsize)

    # PbcorrFirst 2/3: feather
    featherimage = intimage_tmp.replace(".image",".pbcorrfirst_tmp")
    feather(imagename = featherimage,
            highres = intimage_pbcor,
            lowres = tpimage,
            sdfactor = sdfactor,
            effdishdiam = effdishdiam,
            lowpassfiltersd = False)
   
    # PbcorrFirst 3/3: cut at 0.25 pb
    featherimage2 = intimage_tmp.replace("12m+7m","pbcorrfirst_"+suffix)
    os.system("rm -rf " + featherimage2)
    immath(imagename = [featherimage,intpbimage],
           expr = "iif(IM1>=0.25,IM0,0.0)",
           outfile = featherimage2)
    os.system("rm -rf " + featherimage)

    addbeamheader_round(featherimage2,beamsize)

    return featherimage2


def import_data(dir_working,dir_data,project,featherduffix="sd1p0"):
    """
    """
    featherfirst = glob.glob(dir_data+project+"/*featherfirst_"+featherduffix+"_br.image")[0]
    pbcorrfirst = glob.glob(dir_data+project+"/*pbcorrfirst_"+featherduffix+"_br.image")[0]
    intpb = glob.glob(dir_data+project+"/*.pb")[0]

    os.system("cp -r "+featherfirst+" "+dir_working)
    os.system("cp -r "+pbcorrfirst+" "+dir_working)
    os.system("cp -r "+intpb+" "+dir_working)

    featherfirst = glob.glob(dir_working + featherfirst.split("/")[-1])[0]
    pbcorrfirst = glob.glob(dir_working + pbcorrfirst.split("/")[-1])[0]
    intpb = glob.glob(dir_working + intpb.split("/")[-1])[0]

    #makemask(mode="delete", inpmask=featherfirst+":mask0")
    #makemask(mode="delete", inpmask=pbcorrfirst+":mask0")
    makemask(mode="delete", inpmask=intpb+":mask0")

    return featherfirst, pbcorrfirst, intpb

def merge_pbcored_mosaic(image_south,image_north,intpb_south,intpb_north,output):
    # make overlap mask
    mergemask = output + "_mask.merge"
    immath(imagename = [intpb_south,intpb_north],
           expr = "iif(IM0>=0.25,iif(IM1>=0.25,1.0,0.0),0.0)",
           outfile = mergemask)
        
    # merge overlap and south
    outfile1 = output + "_merge.image_tmp"
    expr_merge = "(IM3*IM3*IM1 + IM4*IM4*IM2) / (IM3*IM3 + IM4*IM4)"
    immath(imagename = [mergemask,
                        image_south,
                        image_north,
                        intpb_south,
                        intpb_north],
           expr = "iif(IM0>=1.0," + expr_merge + ",IM1)",
           outfile = outfile1)
           
    # subtract overlap from north
    outfile2 = output + "_merge.image_tmp2"
    immath(imagename = [mergemask,
                        image_south,
                        image_north],
           expr = "iif(IM0>=1.0,0.0,IM2)",
           outfile = outfile2)
           
    immath(imagename = [mergemask,outfile1,outfile2],
           expr = "iif(IM0>=0.0,IM1+IM2,0.0)",
           outfile = output)
           
    os.system("rm -rf " + outfile1 + " " + outfile2 + " " + mergemask)

def merge_mosaic(image_south,image_north,intpb_south,intpb_north,output):
    # make overlap mask
    mergemask = output + "_mask.merge"
    immath(imagename = [intpb_south,intpb_north],
           expr = "iif(IM0>=0.25,iif(IM1>=0.25,1.0,0.0),0.0)",
           outfile = mergemask)
           
    # merge overlap and south
    outfile1 = output + "_merge.image_tmp"
    expr_merge = "(IM3*IM1 + IM4*IM2) / (IM3*IM3 + IM4*IM4)"
    immath(imagename = [mergemask,
                        image_south,
                        image_north,
                        intpb_south,
                        intpb_north],
           expr = "iif(IM0>=1.0," + expr_merge + ",IM1)",
           outfile = outfile1)
           
    # subtract overlap from north
    outfile2 = output + "_merge.image_tmp2"
    immath(imagename = [mergemask,
                        image_south,
                        image_north],
           expr = "iif(IM0>=1.0,0.0,IM2)",
           outfile = outfile2)
           
    immath(imagename = [mergemask,outfile1,outfile2],
           expr = "iif(IM0>=0.0,IM1+IM2,0.0)",
           outfile = output)
           
    os.system("rm -rf " + outfile1 + " " + outfile2 + " " + mergemask)

def import_data2(dir_working,dir_data,project):
    """
    """
    image = glob.glob(dir_data+project+"/*12m+7m*_br.smooth")[0]
    intpb = glob.glob(dir_data+project+"/*.pb")[0]

    os.system("cp -r "+image+" "+dir_working)
    os.system("cp -r "+intpb+" "+dir_working)

    image = glob.glob(dir_working + image.split("/")[-1])[0]
    intpb = glob.glob(dir_working + intpb.split("/")[-1])[0]

    makemask(mode="delete", inpmask=image+":mask0")
    makemask(mode="delete", inpmask=intpb+":mask0")

    return image, intpb

def createmask(imagename,thres,outmask):
    os.system("rm -rf " + outmask)
    immath(imagename = imagename,
           mode = "evalexpr",
           expr = "iif(IM0 >= " + str(thres) + ", 1.0, 0.0)",
           outfile = outmask)
    imhead(imagename = outmask,
           mode = "del",
           hdkey = "beammajor")

"""
# do not use this! calculating pb renopnse at the overlap region is wrong!
def merge_pb(intpb_south,intpb_north,output):
    # merge overlap and south
    outfile1 = output + "_merge.image_tmp"
    numer = "1"
    denom = "(sqrt(1/sqrt(IM0)) + sqrt(1/sqrt(IM1)))"
    expr1 = "sqrt(" + numer + "/" + denom + ")"
    immath(imagename = [intpb_south,intpb_north],
           expr = "iif(IM0+IM1>1.0,"+expr1+",IM0)",
           outfile = outfile1)
           
    # subtract overlap from north
    outfile2 = output + "_merge.image_tmp2"
    immath(imagename = [intpb_south,intpb_north],
           expr = "iif(IM0+IM1>1.0,0.0,IM1)",
           outfile = outfile2)

    outfile3 = output + "_merge.image_tmp3"
    immath(imagename = [outfile1,outfile2],
           expr = "iif(IM0+IM1>0.0,IM0+IM1,0.0)",
           outfile = outfile3)
    
    max = imstat(outfile3)["max"][0]
    immath(imagename = outfile3,
               expr = "IM0/"+str(max),
               outfile = output)
           
    os.system("rm -rf " + outfile1 + " " + outfile2 + " " + outfile3)
"""
