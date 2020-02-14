import os
import re
import sys
import glob
import scipy
import shutil
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../ngc3110/ana/datacube_faintline/"
dir_mask = "../../ngc3110/ana/datacube_line/"
pixelmin = 1.5


#####################
### Main Procedure
#####################
### importfits and imsmooth
os.system("rm -rf " + dir_data + "mask2.image")
imagenames = glob.glob(dir_data + "*.image")
fitsimages = glob.glob(dir_data + "*.fits")
for i in range(len(fitsimages)):
    imagename = fitsimages[i].replace(".fits", ".image")
    done = glob.glob(imagename + ".smooth")
    if not done:
        importfits(fitsimage = fitsimages[i],
            imagename = imagename)
        imtrans(imagename,
            outfile = imagename + ".trans",
            order = "0132")
        imhead(imagename = imagename + ".trans",
            mode = "put",
            hdkey = "reffreqtype",
            hdvalue = "BARY")
        imsmooth(imagename = imagename + ".trans",
            kernel = "gauss",
            targetres = True,
            major = "1.8arcsec",
            minor = "1.8arcsec",
            pa = "0.0deg",
            outfile = imagename + ".smooth")
        os.system("rm -rf " + imagename + " " + imagename + ".trans")


### create mask
imagenames = glob.glob(dir_data + "*.smooth")
myim.createmask(dir_data = dir_data,
    imagename = imagenames[3].split("/")[-1],
    thres = 0.00045 * 2.3,
    outmask = "mask_C18O.mask")


outmask = dir_data + "mask_C18O.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[0],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[0],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[0], mode = "list")["cdelt1"])
pixelsize = pix * 3600 * 180 / np.pi
beamarea = (major * minor * np.pi/(4 * np.log(2))) / (pixelsize ** 2)
ia.open(outmask)
mask = ia.getchunk()
labeled, j = scipy.ndimage.label(mask)
myhistogram = scipy.ndimage.measurements.histogram(labeled, 0, j+1 , j+1)
object_slices = scipy.ndimage.find_objects(labeled)
threshold = beamarea * pixelmin
for i in range(j):
    if myhistogram[i + 1] < threshold:
        mask[object_slices[i]] = 0
ia.putchunk(mask)
ia.done()


### create momement maps for c18o10
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "1~11",
                 mask = "mask_C18O.mask",
                 thres = 0.00075 * 2.5)


### create momement maps for ch3oh
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[1],
                 chans = "1~11",
                 mask = "mask_C18O.mask",
                 thres = 0.0007 * 2.5)


### create momement maps for cs21
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[2],
                 chans = "1~11",
                 mask = "mask_C18O.mask",
                 thres = 0.00065 * 2.5)


### create momement maps for cn10h
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[3],
                 chans = "1~11",
                 mask = "mask_C18O.mask",
                 thres = 0.00045 * 3.0)


### create momement maps for cn10l
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[4],
                 chans = "1~11",
                 mask = "mask_C18O.mask",
                 thres = 0.00045 * 2.5)


### create momement maps for cs54
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[5],
                 chans = "1~11",
                 mask = "mask_C18O.mask",
                 thres = 0.00055 * 2.5)
