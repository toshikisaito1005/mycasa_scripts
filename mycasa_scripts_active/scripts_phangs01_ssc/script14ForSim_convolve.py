import os
import glob
import numpy as np

caf_images = glob.glob("../sim_phangs/*/sim_*_caf_br.image")
cbf_images = glob.glob("../sim_phangs/*/sim_*_cbf_br.image")
cdf_images = glob.glob("../sim_phangs/*/sim_*_cdf_br.image")
aca_images = glob.glob("../sim_phangs/*/sim_*_7m_br.image")
cdaf_images = glob.glob("../sim_phangs/*/sim_*_cdf_br.feather")

for i in range(len(caf_images)):
    galname = caf_images[i].split("/")[2]
    skymodel = glob.glob("../phangs_dr1/" + galname + "*.jyperbeam")[0]
    imagenames = [caf_images[i],cbf_images[i],cdf_images[i],cdaf_images[i],aca_images[i]]

    outfile = aca_images[i].replace("_7m_br.image","_skymodel.smooth_tmp_")
    os.system("rm -rf " + outfile)
    imsmooth(imagename = skymodel,
             targetres = True,
             major = "10arcsec",
	     minor = "10arcsec",
	     pa = "0deg",
	     outfile = outfile)

    outfile = aca_images[i].replace("_7m_br.image","_skymodel.smooth")
    os.system("rm -rf " + outfile)
    imregrid(imagename = aca_images[i].replace("_7m_br.image","_skymodel.smooth_tmp_"),
             template = aca_images[i],
	     output = outfile)
    os.system("rm -rf " + aca_images[i].replace("_7m_br.image","_skymodel.smooth_tmp_"))

    imagename = aca_images[i].replace("_7m_br.image","_skymodel.smooth")
    fitsimage = aca_images[i].replace("_7m_br.image","_skymodel.smooth.fits")
    os.system("rm -rf " + fitsimage)
    exportfits(imagename = imagename,
               fitsimage = fitsimage)

    os.system("rm -rf " + imagename)
    importfits(fitsimage = fitsimage,
               imagename = imagename,
	       defaultaxes=True,
	       defaultaxesvalues=["RA","Dec","Frequency","Stokes"])

    for j in imagenames:
        outfile = j.replace(".image","") + ".smooth"
	os.system("rm -rf " + outfile)
	imsmooth(imagename = j,
	         targetres = True,
	         major = "10arcsec",
		 minor = "10arcsec",
		 pa = "0deg",
		 outfile = outfile)

        outfile = j.replace(".image","") + ".smooth.pbcor"
	os.system("rm -rf " + outfile)
	impbcor(imagename = j.replace(".image","") + ".smooth",
	        pbimage = aca_images[i].replace(".image",".pb"),
		outfile = outfile)

        os.system("rm -rf " + j.replace(".image","") + ".fidelity")
        expr = "iif(IM1>0.1,abs(IM1)/abs(IM0-IM1),0.0)"
        immath(imagename = [j.replace(".image","") + ".smooth.pbcor",
	                    aca_images[i].replace("_7m_br.image","_skymodel.smooth")],
               mode = "evalexpr",
	       expr = expr,
	       outfile = j.replace(".image","") + ".fidelity")


