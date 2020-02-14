import os
import sys
import glob
import datetime

galname = "model"
suffix = "sim04"
dir_data = "/home/saito/Desktop/ssc_test/"
wt="br"

im_model="../"+suffix+"/"+suffix+".aca.skymodel"
im_7m=glob.glob(dir_data+galname+"_7m_"+suffix+"/*"+wt+".smooth.pbcor")
im_cbf=glob.glob(dir_data+galname+"_cbf_"+suffix+"/*"+wt+".smooth.pbcor")
im_caf=glob.glob(dir_data+galname+"_caf_"+suffix+"/*"+wt+".smooth.pbcor")
im_cdf=glob.glob(dir_data+galname+"_cdf_"+suffix+"/*"+wt+".smooth.pbcor")
im_cdaf=glob.glob(dir_data+galname+"_cdf_"+suffix+"/*"+wt+".feather.smooth.pbcor")

os.system("rm -rf " + im_model + ".regrid")
imregrid(imagename = im_model,
         template = im_7m[0],
	 output = im_model + ".regrid")
im_model = im_model + ".regrid"

expr = "iif(IM1>0.05*8,abs(IM1)/abs(IM0-IM1),0.0)"

if im_7m:
    outfile=im_7m[0].replace(".smooth.pbcor",".accuracy")
    os.system("rm -rf " + outfile)
    immath(imagename = [im_7m[0],im_model],
        mode = "evalexpr",
	expr = expr,
        outfile = outfile)

if im_cbf:
    outfile=im_cbf[0].replace(".smooth.pbcor",".accuracy")
    os.system("rm -rf " + outfile)
    immath(imagename = [im_cbf[0],im_model],
        mode = "evalexpr",
        expr = expr,
        outfile = outfile)

if im_caf:
    outfile=im_caf[0].replace(".smooth.pbcor",".accuracy")
    os.system("rm -rf " + outfile)
    immath(imagename = [im_caf[0],im_model],
        mode = "evalexpr",
        expr = expr,
        outfile = outfile)

if im_cdf:
    outfile=im_cdf[0].replace(".smooth.pbcor",".accuracy")
    os.system("rm -rf " + outfile)
    immath(imagename = [im_cdf[0],im_model],
        mode = "evalexpr",
        expr = expr,
        outfile = outfile)

if im_cdaf:
    outfile=im_cdaf[0].replace(".smooth.pbcor",".accuracy")
    os.system("rm -rf " + outfile)
    immath(imagename = [im_cdaf[0],im_model],
        mode = "evalexpr",
        expr = expr,
        outfile = outfile)


