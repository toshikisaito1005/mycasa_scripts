import os
import sys
import glob
import numpy as np
from astropy.coordinates import SkyCoord


dir_project = "/Users/saito/data/myproj_active/proj_phangs06_ssc/"
tpbeam = "28.6arcsec"


##############################
### def
##############################
def biggersize(
    imagename,
    output,
    ):
    # get native grid information
    num_x_pix = imhead(imagename,mode="list")["shape"][0]
    num_y_pix = imhead(imagename,mode="list")["shape"][1]
    pix_radian = imhead(imagename,mode="list")["cdelt2"]
    obsfreq = 230.53800 # imhead(imagename,mode="list")["crval4"]/1e9
    pix_arcsec = round(pix_radian * 3600 * 180 / np.pi, 3)

    # create tempalte image
    blc_ra_tmp=imstat(imagename)["blcf"].split(", ")[0]
    blc_dec_tmp=imstat(imagename)["blcf"].split(", ")[1]
    blc_ra = blc_ra_tmp.replace(":","h",1).replace(":","m",1)+"s"
    blc_dec = blc_dec_tmp.replace(".","d",1).replace(".","m",1)+"s"
    beamsize=round(imhead(imagename,"list")["beammajor"]["value"], 2)
    pix_size=round(beamsize/4.53, 2)
    size_x = np.max([num_x_pix, num_y_pix]) * pix_arcsec / pix_size * 1.5
    size_y = size_x
    c = SkyCoord(blc_ra, blc_dec)
    ra_dgr = str(c.ra.degree)
    dec_dgr = str(c.dec.degree)
    direction_ra = str(float(ra_dgr) - num_x_pix*pix_arcsec/3600./2.*5/4.)+"deg"
    direction_dec = str(float(dec_dgr) + num_y_pix*pix_arcsec/3600./2.)+"deg"
    direction="J2000 "+direction_ra+" "+direction_dec
    cl.done()
    cl.addcomponent(dir=direction,
                    flux=1.0,
                    fluxunit="Jy",
                    freq="230.0GHz",
                    shape="Gaussian",
                    majoraxis="0.1arcmin",
                    minoraxis="0.05arcmin",
                    positionangle="45.0deg")

    ia.fromshape("template.im",[size_x,size_y,1,1],overwrite=True)
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
    exportfits(imagename="template.im",
               fitsimage="template.fits",
               overwrite=True)
    #
    importfits(fitsimage="template.fits",
               imagename="template.image")
    #
    # regrid
    os.system("rm -rf "+output)
    imregrid(imagename=imagename,
             template="template.image",
             output=output,
             axes=[0,1])

    os.system("rm -rf template.image template.fits")
    ia.close()
    cl.close()

##############################
### main
##############################
### directories
dir_mask = dir_project + "v3p4_hybridmask/"
dir_data = dir_project + "v3p4_tpeak/"


### get systemic velocity definition
mosaic_def = np.loadtxt("mosaic_definitions.txt",dtype="S20",usecols=(0,3))
mosaic_def = np.c_[[s.split("_")[0] for s in mosaic_def[:,0]], mosaic_def[:,1]]


### convert to CASA image
fitsimages = glob.glob(dir_mask + "*.fits")
fitsimages.extend(glob.glob(dir_data + "*.fits"))
for i in range(len(fitsimages)):
  print("### " + str(i+1) + "/" + str(len(fitsimages)))
  importfits(fitsimage = fitsimages[i],
    imagename = fitsimages[i].replace(".fits",".image"))
  os.system("rm -rf " + fitsimages[i])

os.system("rm -rf " + dir_data + "ic5332_12m+7m+tp_co21_strict_tpeak.image")
os.system("rm -rf " + dir_data + "ngc1300_12m+7m+tp_co21_strict_tpeak.image")
os.system("rm -rf " + dir_data + "ngc4569_12m+7m+tp_co21_strict_tpeak.image")
os.system("rm -rf " + dir_data + "ngc4298_12m+7m+tp_co21_strict_tpeak.image")
os.system("rm -rf " + dir_data + "ngc7496_12m+7m+tp_co21_strict_tpeak.image")


###
imagenames = glob.glob(dir_data + "*.image")
imagenames.sort()
#
for i in range(len(imagenames)):
  #
  this_image = imagenames[i]
  print("### processing " + this_image.split("/")[-1] + " " + str(i+1) + "/" + str(len(imagenames)))
  bmaj = imhead(this_image,mode="list")["beammajor"]["value"]
  factor = 1.222e+6 / bmaj**2 / 230.53800**2
  #
  maskname = glob.glob(dir_mask + this_image.split("/")[-1].split("12m")[0] + "*_hybridmask.image")
  if maskname:
    maskname = maskname[0]
    #
    maskname2 = maskname.replace(".image",".mask2")
    os.system("rm -rf " + maskname2)
    immoments(imagename=maskname, outfile=maskname2)
    #
    expr = "iif(IM1>=1.0,"+"IM0/"+str(factor)+",0.0)"
    #
    outfile1 = this_image.replace(".image",".jyperbeam")
    os.system("rm -rf " + outfile1)
    immath(imagename=[this_image,maskname2], mode="evalexpr", expr=expr, outfile=outfile1)
    # skymodel
    bmaj = imhead(outfile1,mode="list")["beammajor"]["value"]
    size_pix = abs(imhead(outfile1,mode="list")["cdelt1"])
    area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
    beamarea = (bmaj*bmaj*np.pi) / (4*np.log(2)) / area_pix_arcsec
    #
    outfile2 = this_image.replace(".image",".skymodel")
    os.system("rm -rf " + outfile2)
    immath(imagename=outfile1, expr="IM0/"+str(beamarea), outfile=outfile2)
    #
    imhead(imagename=outfile2, mode="put", hdkey="bunit", hdvalue="Jy/pixel")
    imhead(imagename=outfile1, mode="put", hdkey="bunit", hdvalue="Jy/beam")
    # make imsize of outfile1 bigger
    os.system("rm -rf " + outfile1 + ".bigger_tmp")
    biggersize(outfile1, outfile1 + ".bigger_tmp")
    # blank to 0
    ia.open(outfile1 + ".bigger_tmp")
    ia.replacemaskedpixels(0., update=True)
    ia.close()
    #
    os.system("rm -rf " + outfile1 + ".bigger")
    immath(outfile1 + ".bigger_tmp",
        expr = "iif(IM0>=0,IM0,0)",
        outfile = outfile1 + ".bigger")
    os.system("rm -rf " + outfile1 + ".bigger_tmp")
    #
    outfile3 = this_image.replace(".image",".jypb.smooth_tmp_")
    os.system("rm -rf " + outfile3)
    imsmooth(imagename=outfile1+".bigger", major=tpbeam, minor=tpbeam, pa="0deg", outfile=outfile3)
    #
    cell = np.abs(imhead(outfile3,mode='list')['cdelt1']) * 180.*3600./np.pi
    nbin = int(28.5 / 4.5 / cell)
    #
    outfile4 = this_image.replace(".image",".jypb.smooth")
    os.system("rm -rf " + outfile4)
    imrebin(imagename=outfile3, outfile=outfile4, factor=[nbin,nbin])
    #
    bmaj = imhead(outfile4,mode="list")["beammajor"]["value"]
    size_pix = abs(imhead(outfile4,mode="list")["cdelt1"])
    area_pix_arcsec = (size_pix * 3600 * 180 / np.pi) ** 2
    beamarea = (bmaj*bmaj*np.pi) / (4*np.log(2)) / area_pix_arcsec
    #
    outfile5 = this_image.replace(".image",".jyppix.smooth")
    os.system("rm -rf " + outfile5)
    immath(imagename=outfile4, expr="IM0/"+str(beamarea), outfile=outfile5)
    #
    imhead(imagename=outfile5, mode="put", hdkey="bunit", hdvalue="Jy/pixel")
    imhead(imagename=outfile5, mode="del", hdkey="beammajor")
    #
    os.system("rm -rf " + maskname)
    os.system("rm -rf " + outfile3)
    #
    maskname3 = maskname.replace(".image",".mask2.smooth")
    os.system("rm -rf " + maskname3)
    #
    imsmooth(imagename=maskname2, targetres=True, major="3arcsec", minor="3arcsec", pa="0deg", outfile=maskname3)
    #
    maskname4 = maskname.replace(".image",".mask")
    os.system("rm -rf " + maskname4)
    immath(imagename=maskname3, mode="evalexpr", expr="iif(IM0>=1.0,1.0,0.0)", outfile=maskname4)
    #
    os.system("rm -rf " + maskname.replace(".image",".mask2*"))
    os.system("rm -rf " + maskname.replace(".image",".mask3*"))
    #
    maskfits = maskname.replace(".image",".mask.fits")
    os.system("rm -rf " + maskfits)
    exportfits(imagename=maskname4, fitsimage=maskfits)
    #
    os.system("rm -rf " + maskname4)
    importfits(fitsimage=maskfits, imagename=maskname4, defaultaxes=True, defaultaxesvalues=["RA","Dec","Frequency","Stokes"])
    os.system("rm -rf " + maskfits)


os.system("rm -rf *.last")
