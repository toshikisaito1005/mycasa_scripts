import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd())
import mycasaimaging_tools as myim


dir_data = "../ALMA_ACA_co10/fits/data_aca/data_aca/"
pixelmin = 3.


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
imagenames = glob.glob(dir_data + "*.image")



### NGC 6240
os.system("rm -rf " + dir_data + "mask2.image")
imagename = imagenames[3]
thres = 0.0011 * 2.
thres2 = 0.001 * 2.5
maskname = "ngc6240.mask"
chans = "20~81"

myim.createmask(dir_data = dir_data,
                imagename = imagename,
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


### NGC 1614
os.system("rm -rf " + dir_data + "mask2.image")
imagename = imagenames[0]
thres = 0.0014 * 2.
thres2 = 0.0014 * 2.5
maskname = "ngc1614.mask"
chans = "1~28"

myim.createmask(dir_data = dir_data,
                imagename = imagename,
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


### NGC 5257
os.system("rm -rf " + dir_data + "mask2.image")
imagename = imagenames[1]
thres = 0.001 * 2.
thres2 = 0.001 * 2.5
maskname = "ngc5257.mask"
chans = "5~32"

myim.createmask(dir_data = dir_data,
                imagename = imagename,
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


### NGC 5258
os.system("rm -rf " + dir_data + "mask2.image")
imagename = imagenames[2]
thres = 0.001 * 2.
thres2 = 0.001 * 2.5
maskname = "ngc5258.mask"
chans = "3~30"

myim.createmask(dir_data = dir_data,
                imagename = imagename,
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


### VV114
pixelmin = 5.

os.system("rm -rf " + dir_data + "mask2.image")
imagename = imagenames[4]
thres = 0.002 * 3.5
thres2 = 0.002 * 4.
maskname = "vv114.mask"
chans = "0~59"

outfile = imagenames[4] + ".trans"
os.system("rm -rf " + outfile)
imtrans(imagename = imagename,
    outfile = outfile,
    order = "0132")

myim.createmask(dir_data = dir_data,
                imagename = imagenames[4] + ".trans",
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
                 imagename = imagenames[4] + ".trans",
                 chans = chans,
                 mask = maskname,
                 thres = thres2)

