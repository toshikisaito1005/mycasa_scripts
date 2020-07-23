import os
import glob
import scipy
from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord

# CASA imports
from taskinit import *
from importfits import importfits
from imregrid import imregrid
from imsmooth import imsmooth
from imval import imval
from immoments import immoments
from immath import immath
from makemask import makemask
from imhead import imhead
from imstat import imstat
from exportfits import exportfits
import analysisUtils as aU
mycl = aU.createCasaTool(cltool)
mycs = aU.createCasaTool(cstool)
myia = aU.createCasaTool(iatool)
myrg = aU.createCasaTool(rgtool)
myqa = aU.createCasaTool(qatool)


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/phangs_ulirg/"
galnames = ["ngc1614", # z = 0.01594
            "ngc3110", # z = 0.01686
            "ngc6240", # z = 0.02448
            "ngc3256", # z = 0.00935
            "irasf13373a", # ngc 5258, z = 0.02254
            "irasf13373b", # ngc 5257, z = 0.02268
            "iras13120"] # z = 0.03076
beams = [round(120/305.,2), # 120 pc resolution
         round(120/326.,2), # 120 pc resolution
         round(120/483.,2), # 120 pc resolution
         round(120/184.,2), # 120 pc resolution
         round(120/444.,2), # 120 pc resolution
         round(120/444.,2), # 120 pc resolution
         round(120/600.,2)] # 120 pc resolution
#beams = [0.22, 0.18, 0.11, 0.22, 0.21, 0.20, 0.19] # native resolution
ras = ["04h34m00.038s",
       "10h04m02.102s",
       "16h52m58.893s",
       "10h27m51.203s",
       "13h39m57.682s", # ngc 5258
       "13h39m52.926s", # ngc 5257
       "13h15m06.325s"]
decls = ["-8d34m45.052s",
         "-6d28m29.987s",
         "2d24m03.869s",
         "-43d54m16.908s",
         "0d49m50.988s", # ngc 5258
         "0d50m24.355s", # ngc 5257
         "-55d09m22.707s"]
chanss = ["10~62", "5~58", "15~168", "85~165", "5~60", "10~65", "15~89"]
pbcuts = [0.7, 0.5, 0.5, 0.5, 0.5, 0.5, 0.85]
pointings = [1, 1, 1, 2, 3, 3, 1]
snr_moms = [3, 3, 1., 3, 3, 3, 3]


#####################
### Functions
#####################
def eazy_importfits(fitsimage,defaultaxes=True):
    """
    for moment map creation
    """
    defaultaxesvalues = ['Right Ascension',
                         'Declination',
                         'Stokes',
                         'Frequency']
    imname = fitsimage.replace(".fits", ".image")
    os.system("rm -rf " + imname)
    importfits(fitsimage = fitsimage,
               imagename = imname,
               defaultaxes = defaultaxes,
               defaultaxesvalues = defaultaxesvalues)

def easy_imsmooth(imagename,targetbeam,delete_original=True):
    """
    for moment map creation
    """
    os.system("rm -rf " + imagename + ".smooth")
    imsmooth(imagename = imagename,
             kernel = "gauss",
             major = str(targetbeam) + "arcsec",
             minor = str(targetbeam) + "arcsec",
             pa = "0.0deg",
             targetres = True,
             outfile = imagename + ".smooth")

    if delete_original==True:
        os.system("rm -rf " + imagename)

def rebinpix(imagename,output,blc_ra,blc_dec,pbcut=0.5,freq=230.53800,pointing=1):
    """
    change pixel size to bmaj/4.53
    """
    # get native grid information
    num_x_pix=imhead(imagename,mode="list")["shape"][0]
    num_y_pix=imhead(imagename,mode="list")["shape"][1]
    pix_radian=imhead(imagename,mode="list")["cdelt2"]
    pix_arcsec = round(pix_radian * 3600 * 180 / np.pi, 2)
    
    # create tempalte image
    beamsize=round(imhead(imagename,"list")["beammajor"]["value"], 2)
    pix_size=round(beamsize/4.53, 2)
    #size_x = max(int(num_x_pix*pix_arcsec/pix_size)+4,int(num_y_pix*pix_arcsec/pix_size)+4)
    size_x = (21 * (300/freq) / pix_size) * (0.5/pbcut) * pointing * 1.5
    size_y = size_x
    c = SkyCoord(blc_ra, blc_dec)
    ra_dgr = str(c.ra.degree)
    dec_dgr = str(c.dec.degree)
    direction_ra = str(ra_dgr)+"deg"
    direction_dec = str(dec_dgr)+"deg"
    direction="J2000 "+direction_ra+" "+direction_dec
    mycl.done()
    mycl.addcomponent(dir=direction,
                      flux=1.0,
                      fluxunit="Jy",
                      freq="230.0GHz",
                      shape="Gaussian",
                      majoraxis="0.1arcmin",
                      minoraxis="0.05arcmin",
                      positionangle="45.0deg")

    myia.fromshape(output+"_tmp_",[size_x,size_y,1,1],overwrite=True)
    mycs=myia.coordsys()
    mycs.setunits(["rad","rad","","Hz"])
    cell_rad=myqa.convert(myqa.quantity(str(pix_size)+"arcsec"),"rad")["value"]
    mycs.setincrement([-cell_rad,cell_rad],"direction")
    mycs.setreferencevalue([myqa.convert(direction_ra,"rad")["value"],
                            myqa.convert(direction_dec,"rad")["value"]],
                           type="direction")
    mycs.setreferencevalue("230GHz","spectral")
    mycs.setincrement("1GHz","spectral")
    myia.setcoordsys(mycs.torecord())
    myia.setbrightnessunit("Jy/pixel")
    myia.modify(mycl.torecord(),subtract=False)
    exportfits(imagename=output+"_tmp_",
               fitsimage=output+"_tmp_.fits",
               overwrite=True)

    importfits(fitsimage=output+"_tmp_.fits",imagename=output)
                      
    myia.close()
    mycl.close()
    os.system("rm -rf "+output+"_tmp_")
    os.system("rm -rf "+output+"_tmp_.fits")

def easy_imregrid(imagename,template,axes=-1,delete_original=True):
    """
    for moment map creation
    """
    os.system("rm -rf " + imagename + ".regrid")
    imregrid(imagename = imagename,
             template = template,
             axes=axes,
             output = imagename + ".regrid")
        
    if delete_original==True:
        os.system("rm -rf " + imagename)

def ch_noise(image_cube,chans):
    ch_line_start = int(chans.split("~")[0])
    ch_line_end = int(chans.split("~")[1])
    size_cube = imhead(image_cube)["shape"][3]

    if int(ch_line_start)-1 > 0:
        ch_noise_1 = "0~"+str(ch_line_start-1)
    else:
        ch_noise_1 = ""

    if ch_line_end+1 < size_cube-1:
        ch_noise_2 = str(ch_line_end+1)+"~"+str(size_cube-1)
    else:
        ch_noise_2 = ""

    ch_noise = ",".join([ch_noise_1, ch_noise_2]).rstrip(",")

    return ch_noise

def beam_area(imagename):
    """
    for moment map creation
    """
    major = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beammajor")["value"]
    minor = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beamminor")["value"]
    pix = abs(imhead(imagename = imagename,
                     mode = "list")["cdelt1"])

    pixelsize = pix * 3600 * 180 / np.pi
    beamarea = (major * minor * np.pi/(4 * np.log(2))) \
               / (pixelsize ** 2)

    return beamarea

def remove_smallmask(outmask,beamarea,pixelmin):
    """
    for moment map creation
    """
    os.system("rm -rf " + outmask + ".all")
    os.system("cp -r " + outmask + " " + outmask + ".all")
    
    myia.open(outmask)
    mask = myia.getchunk()
    labeled, j = scipy.ndimage.label(mask)
    myhistogram = \
        scipy.ndimage.measurements.histogram(labeled,0,j+1,j+1)
    object_slices = scipy.ndimage.find_objects(labeled)
    threshold = beamarea * pixelmin

    for i in range(j):
        if myhistogram[i + 1] < threshold:
            mask[object_slices[i]] = 0
    myia.putchunk(mask)
    myia.done()

def imsmooth3(imagename,outmask,chans,beam_size,template,pixelmin=10):
    chnoise = ch_noise(imagename,chans)
    factor1, factor2, factor3 = 3, 9, 15
    
    # imsmooth
    os.system("rm -rf "+imagename+".smooth1")
    imsmooth(imagename=imagename,
             targetres=True,
             major=str(beam_size*factor1)+"arcsec",
             minor=str(beam_size*factor1)+"arcsec",
             pa="0deg",
             outfile=imagename+".smooth1")
    rms1 = imstat(imagename+".smooth1",chans=chnoise)["rms"][0]

    os.system("rm -rf "+imagename+".smooth2")
    imsmooth(imagename=imagename,
             targetres=True,
             major=str(beam_size*factor2)+"arcsec",
             minor=str(beam_size*factor2)+"arcsec",
             pa="0deg",
             outfile=imagename+".smooth2")
    rms2 = imstat(imagename+".smooth2",chans=chnoise)["rms"][0]

    os.system("rm -rf "+imagename+".smooth3")
    imsmooth(imagename=imagename,
             targetres=True,
             major=str(beam_size*factor3)+"arcsec",
             minor=str(beam_size*factor3)+"arcsec",
             pa="0deg",
             outfile=imagename+".smooth3")
    rms3 = imstat(imagename+".smooth3",chans=chnoise)["rms"][0]
    
    # imregrid
    easy_imregrid(imagename+".smooth1",template,axes=[0,1])
    easy_imregrid(imagename+".smooth2",template,axes=[0,1])
    easy_imregrid(imagename+".smooth3",template,axes=[0,1])
    
    # immath: snr should be 4, but 8 for iras13120
    os.system("rm -rf "+imagename+".smooth1.mask")
    immath(imagename=imagename+".smooth1.regrid",
           mode="evalexpr",
           expr="iif(IM0>="+str(rms1*4)+",1.0,0.0)",
           outfile=imagename+".smooth1.mask")

    os.system("rm -rf "+imagename+".smooth2.mask")
    immath(imagename=imagename+".smooth2.regrid",
           mode="evalexpr",
           expr="iif(IM0>="+str(rms2*4)+",1.0,0.0)",
           outfile=imagename+".smooth2.mask")

    os.system("rm -rf "+imagename+".smooth3.mask")
    immath(imagename=imagename+".smooth3.regrid",
           mode="evalexpr",
           expr="iif(IM0>="+str(rms3*4)+",1.0,0.0)",
           outfile=imagename+".smooth3.mask")

    os.system("rm -rf "+outmask)
    immath(imagename=[imagename+".smooth1.mask",
                      imagename+".smooth2.mask",
                      imagename+".smooth3.mask"],
           mode="evalexpr",
           expr="iif(IM0+IM1+IM2>=3.0,1.0,0.0)",
           outfile=outmask)

    os.system("rm -rf "+imagename+".smooth1.regrid")
    os.system("rm -rf "+imagename+".smooth2.regrid")
    os.system("rm -rf "+imagename+".smooth3.regrid")

    beamarea = beam_area(imagename)
    remove_smallmask(outmask,beamarea,pixelmin)

def createmask(imagename,thres,outmask):
    """
    for moment map creation
    """
    os.system("rm -rf " + outmask)
    immath(imagename = imagename,
           mode = "evalexpr",
           expr = "iif(IM0 >= " + str(thres) + ", 1.0, 0.0)",
           outfile = outmask)
    imhead(imagename = outmask,
           mode = "del",
           hdkey = "beammajor")

def moment_maps(imagename,
                chans,
                mask,
                thres,
                beam,
                output_mom = [0,2,8]):
    """
    """
    # create masked cube
    outfile = imagename + ".masked"
    os.system("rm -rf " + outfile)
    immath(imagename = [imagename, mask],
           mode = "evalexpr",
           expr = "iif(IM1 >= 1.0, IM0, 0.0)",
           outfile = outfile)

    # modify the header of the mask
    imhead(outfile,"put","beamminor",str(beam)+"arcsec")
    imhead(outfile,"put","beammajor",str(beam)+"arcsec")
    imhead(outfile,"put","beampa","0deg")

    #create moment maps using the masked cube
    for i in range(len(output_mom)):
        outfile = imagename + ".moment" + str(output_mom[i])
        os.system("rm -rf " + outfile)
        immoments(imagename = imagename + ".masked",
                  moments = [output_mom[i]],
                  chans = chans,
                  includepix = [thres, 1000000.],
                  outfile = outfile)

#####################
### Main
#####################
print("### running "+galnames[i])
### define names
dir_dataraw = dir_proj + "data_raw/"
dir_data = dir_proj + "data/"
dir_gal = dir_proj + galnames[i] + "/"
suffix = str(beams[i]).replace(".","p")

### initialize
os.system("rm -rf "+dir_data+galnames[i]+"*")
os.system("rm -rf "+dir_gal+"*"+suffix+"*.moment*")
os.system("rm -rf "+dir_gal+"*"+suffix+"*.mask*")
os.system("rm -rf "+dir_gal+"*"+suffix+"*.cube")

### step 1: importfits
print("### step 1: importfits")

# copy data from data_raw/ to data/
os.system("cp -r "+dir_dataraw+galnames[i]+"* "+dir_data)

# eazy_importfits
fitsimages = glob.glob(dir_data+"*.fits")
for j in range(len(fitsimages)):
    eazy_importfits(fitsimages[j])

os.system("rm -rf "+dir_data+"*.fits")

# find imported images
image_cube = glob.glob(dir_data+galnames[i]+"*pbcor.image*")[0]
pb_cube = glob.glob(dir_data+galnames[i]+"*pb.image*")[0]

if galnames[i]=="ngc1614":
    os.system("rm -rf "+pb_cube+".trans")
    imtrans(imagename=pb_cube,
            outfile=pb_cube+".trans",
            order="0132")
    os.system("rm -rf "+pb_cube)
    pb_cube = pb_cube+".trans"


# depb
image_cube_depb = image_cube.replace("pbcor","depb")
os.system("rm -rf "+image_cube_depb)
impbcor(imagename=image_cube,
        pbimage=pb_cube,
        outfile=image_cube_depb,
        mode="multiply")

# collapse pb cube
os.system("rm -rf " + pb_cube.replace(".image",""))
immoments(imagename=pb_cube,
          moments=[0],
          outfile=pb_cube.replace(".image",""))
os.system("rm -rf " + pb_cube)
pb_map = pb_cube.replace(".image","")

### step 2: shaping datacubes
print("### step 2: rebinpix for pb")
easy_imsmooth(image_cube,beams[i],delete_original=True)
image_cube_sm = image_cube + ".smooth"

temp_rebinpix = image_cube.replace(".image","")+".template"
os.system("rm -rf "+temp_rebinpix)
rebinpix(image_cube_sm,temp_rebinpix,ras[i],decls[i],pbcuts[i])

easy_imregrid(pb_map,temp_rebinpix,axes=[0,1],delete_original=True)
os.system("rm -rf "+pb_cube)
pb_map = pb_map + ".regrid"

### step 3: create hybrid mask
print("### step 3: create hybrid mask")
outmask = image_cube_depb.replace("_depb.image",".hybridmask")
imsmooth3(image_cube_depb,outmask,chanss[i],beams[i],temp_rebinpix)

### step 4: immoments
print("### step 4: immoments with pbcut = "+str(pbcuts[i]))

# smooth depb cube
easy_imsmooth(image_cube_depb,beams[i],delete_original=True)
image_cube_depb_sm = image_cube_depb + ".smooth"

# mv to galname/ directory
os.system("mkdir "+dir_gal)
easy_imregrid(image_cube_sm,temp_rebinpix,axes=[0,1],delete_original=True)
easy_imregrid(image_cube_depb_sm,temp_rebinpix,axes=[0,1],delete_original=True)

image_cube2 = dir_gal+galnames[i]+"_co21_"+suffix+".cube"
os.system("rm -rf "+image_cube2)
os.system("cp -r "+image_cube_sm+".regrid "+image_cube2)
os.system("cp -r "+image_cube_depb_sm+".regrid "+image_cube2+".depb")

# immoments
chnoise = ch_noise(image_cube2,chanss[i])
rms = imstat(image_cube2,chans=chnoise)["rms"][0]
moment_maps(image_cube2,chanss[i],outmask,rms*snr_moms[i],beams[i])

# pb masking
mask_pb = dir_gal+galnames[i]+"_pb_"+suffix+".mask"
peak = imhead(pb_map,mode="list")["datamax"]
createmask(pb_map,peak*pbcuts[i],mask_pb)

images_moment = glob.glob(image_cube2 + ".moment*")
for k in range(len(images_moment)):
    outfile = images_moment[k].replace(".cube","")
    if galnames[i] == "ngc3110":
        os.system("mv " + images_moment[k] + " " \
                  + images_moment[k].replace(".cube",""))
    else:
        os.system("rm -rf " + outfile)
        immath(imagename = [images_moment[k],mask_pb],
               mode = "evalexpr",
               expr = "IM0*IM1",
               outfile = outfile)
        os.system("rm -rf " + images_moment[k])

# clean up
os.system("rm -rf "+dir_data+galnames[i]+"*")
os.system("rm -rf "+dir_gal+"*"+suffix+"*.mask*")
os.system("rm -rf *.last")
