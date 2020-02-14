import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../ngc3110/ana/data_vv114/"
pixelmin = 10.


#####################
### Main Procedure
#####################
fitsimages = glob.glob(dir_data + "*.fits")
for i in range(len(fitsimages)):
    imagename = fitsimages[i].replace(".fits", ".image")
    done = glob.glob(imagename)
    if not done:
        importfits(fitsimage = fitsimages[i],
                   imagename = imagename,
                   defaultaxes = True,
                   defaultaxesvalues = ['Right Ascension',
                                        'Declination',
                                        'Stokes',
                                        'Frequency'])


os.system("rm -rf " + dir_data + "mask2.image")
imagenames = glob.glob(dir_data + "*.image.imsmooth")



### VV 114
os.system("rm -rf " + dir_data + "mask2.image")
imagename = imagenames[0]
thres = 0.004 * 1.
thres2 = 0.004 * 2.5
maskname = "vv114.mask"
chans = "1~64"

myim.createmask(dir_data = dir_data,
                imagename = imagename.split("/")[-1],
                thres = thres,
                outmask = maskname)
outmask = dir_data + maskname
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagename,
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagename,
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagename, mode = "list")["cdelt1"])
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
myim.moment_maps(dir_data = dir_data,
                 imagename = imagename,
                 chans = chans,
                 mask = maskname,
                 thres = thres2)

