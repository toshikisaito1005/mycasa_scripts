import numpy as np
import os
import glob
import pyfits
import shutil
from astropy.coordinates import SkyCoord

dir_data = "/Users/saito/data/myproj_published/proj_phangs02_feather/"
#dir_data = "../"
projects = ["test08"] # ["test06"], ["test07"], ["test08"]
ptgtable = "test01" # "test02", "test03", "test01"
image_length = 320 # 280. # arcsec
direction_ra = "24.174deg"
direction_dec = "15.783deg"
obsfreq = 230.53800
tpbeam = "28.615arcsec"
fluxin = 10.0 # Jy

dir_model = dir_data + "data_model/"
os.system("rm -rf " + dir_model)
os.mkdir(dir_model)

####################
### main
####################
### create skymodel
# import template from ngc0628
template = dir_data + "data/ngc0628_chan_jyperpix.skymodel"
blc_ra_tmp = imstat(template)["blcf"].split(", ")[0]
blc_dec_tmp = imstat(template)["blcf"].split(", ")[1]
blc_ra = blc_ra_tmp.replace(":","h",1).replace(":","m",1)+"s"
blc_dec = blc_dec_tmp.replace(".","d",1).replace(".","m",1)+"s"
beamsize = round(imhead(template,"list")["beammajor"]["value"], 2)
pix_size = round(beamsize/4.53, 2)
size_x = int(image_length / pix_size)
size_y = size_x
c = SkyCoord(blc_ra, blc_dec)
ra_dgr = str(c.ra.degree)
dec_dgr = str(c.dec.degree)
#
direction_ra1 = str(float(direction_ra.strip("deg"))+90/3600.)+"deg" # 60
direction_dec1 = str(float(direction_dec.strip("deg"))-0/3600.)+"deg"
direction="J2000 "+direction_ra1+" "+direction_dec1
cl.done()
cl.addcomponent(dir=direction,
                flux=fluxin,
                fluxunit="Jy",
                freq="230.0GHz",
                shape="Gaussian",
                majoraxis="0.3arcmin", # tpbeam,
                minoraxis="0.1arcmin", # tpbeam,
                positionangle="45.0deg")
#
direction_ra2 = str(float(direction_ra.strip("deg"))-0/3600.)+"deg"
direction_dec2 = str(float(direction_dec.strip("deg"))-5/3600.)+"deg"
direction="J2000 "+direction_ra2+" "+direction_dec2
cl.addcomponent(dir=direction,
                flux=fluxin,
                fluxunit="Jy",
                freq="230.0GHz",
                shape="Gaussian",
                majoraxis="0.3arcmin", # tpbeam,
                minoraxis="0.1arcmin", # tpbeam,
                positionangle="45.0deg")
#
direction_ra3 = str(float(direction_ra.strip("deg"))-90/3600.)+"deg" # 60
direction_dec3 = str(float(direction_dec.strip("deg"))-10/3600.)+"deg"
direction="J2000 "+direction_ra3+" "+direction_dec3
cl.addcomponent(dir=direction,
                flux=fluxin,
                fluxunit="Jy",
                freq="230.0GHz",
                shape="Gaussian",
                majoraxis="0.3arcmin", # tpbeam,
                minoraxis="0.1arcmin", # tpbeam,
                positionangle="45.0deg")

ia.fromshape(dir_model+"gauss_chan_jyperpix.im",[size_x,size_y,1,1],overwrite=True)
cs=ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad=qa.convert(qa.quantity(str(pix_size)+"arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert(direction_ra,"rad")["value"],
                      qa.convert(direction_dec,"rad")["value"]],
                     type="direction")
cs.setreferencevalue(str(obsfreq)+"GHz","spectral")
cs.setincrement("1GHz","spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
ia.close()
cl.close()

exportfits(imagename=dir_model+"gauss_chan_jyperpix.im",
           fitsimage=dir_model+"gauss_chan_jyperpix.fits",
           overwrite=True)
                         
os.system("rm -rf "+dir_model+"gauss_chan_jyperpix.skymodel")
importfits(fitsimage=dir_model+"gauss_chan_jyperpix.fits",
           imagename=dir_model+"gauss_chan_jyperpix.skymodel")
os.system("rm -rf "+dir_model+"gauss_chan_jyperpix.fits")
os.system("rm -rf "+dir_model+"gauss_chan_jyperpix.im")

# create tp model
skymodel = glob.glob(dir_model + "gauss_chan_jyperpix.skymodel")[0]
outfile1 = dir_model + "gauss_chan_jyperbeam.tpimage_tmp"
os.system("rm -rf " + outfile1)
imsmooth(imagename = skymodel,
         major = tpbeam,
         minor = tpbeam,
         pa = "0deg",
         outfile = outfile1)

cell = np.abs(imhead(outfile1,mode='list')['cdelt1'])*180.*3600./np.pi
nbin = int(float(tpbeam.replace("arcsec","")) / 4.53 / cell)
outfile2 = dir_model + "gauss_chan_jyperbeam.tpimage"
imrebin(imagename=outfile1,outfile=outfile2,factor=[nbin,nbin])
os.system("rm -rf " + outfile1)

# create tclean mask
outfile1 = dir_model + "gauss.mask"
os.system("rm -rf " + outfile1)
immath(imagename = skymodel,
       mode = "evalexpr",
       expr = "iif(IM0>=0.00035,1.0,0.0)",
       outfile = outfile1)

# makems using simobserve
skymodel = glob.glob(dir_model + "gauss_chan_jyperpix.skymodel")[0]
tpmodel = glob.glob(dir_model + "gauss_chan_jyperbeam.tpimage")[0]
galname = skymodel.split("/")[-1].split("_")[0]

for i in range(len(projects)):
    print("### working on " + projects[i])
    os.system("rm -rf " + projects[i] + " " + dir_data + projects[i])

    print("# 12m array...")
    ptgfile = ptgtable + ".alma.cycle5.1.ptg.txt"
    num_mosaic = len(np.loadtxt(ptgfile,dtype="S30")[:,0])
    totaltime = str(num_mosaic*10) + "s"
    simobserve(antennalist = "alma.cycle5.1.cfg",
               skymodel = skymodel,
               project = projects[i],
               indirection = "",
               incell = "",
               mapsize = ["",""],
               incenter = "",
               inbright = "",
               setpointings = False,
               ptgfile = ptgfile,
               graphics = "none",
               obsmode = "int",
               totaltime = totaltime,
               pointingspacing = "0.5PB",
               #thermalnoise = "",
               overwrite = True)

    print("# 7m array...")
    ptgfile = ptgtable + ".aca.cycle5.ptg.txt"
    num_mosaic = len(np.loadtxt(ptgfile,dtype="S30")[:,0])
    totaltime = str(num_mosaic*30) + "s"
    simobserve(antennalist = "aca.cycle5.cfg",
               skymodel = skymodel,
               project = projects[i],
               indirection = "",
               incell = "",
               mapsize = ["",""],
               incenter = "",
               inbright = "",
               setpointings = False,
               ptgfile = ptgfile,
               graphics = "none",
               obsmode = "int",
               totaltime = totaltime,
               pointingspacing = "0.4arcmin",
               #thermalnoise = "",
               overwrite = True)

    os.system("mv " + projects[i] + " " + dir_data)

os.system("rm -rf *.last")
