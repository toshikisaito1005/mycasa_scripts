import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/..")
import mycasaimaging_tools as myim


box = ""
pixelmin = 10.

#####################
### Main Procedure
#####################
### hcn_eso148
dir_data = "../../hcn_ulirgs/hcn_eso148/"

os.system("rm -rf " + dir_data + "mask2.image")
os.system("rm -rf " + dir_data + "*moment*")
fitsimages = glob.glob(dir_data + "*_hc*.fits")
for i in range(len(fitsimages)):
    os.system("rm -rf " + fitsimages[i].replace(".fits", ".image"))
    importfits(fitsimage = fitsimages[i],
               imagename = fitsimages[i].replace(".fits", ".image"))

imagenames = glob.glob(dir_data + "*_hc*.image")

# hcn43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = 0.0005 * 2.3,
                outmask = "mask_eso148_hcn.mask")

outmask = dir_data + "mask_eso148_hcn.mask"
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "15~40",
                 mask = "mask_eso148_hcn.mask",
                 thres = 0.0005 * 2.7)

# hco_plus43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[1].split("/")[-1],
                thres = 0.0006 * 2.3,
                outmask = "mask_eso148_hco_plus.mask")

outmask = dir_data + "mask_eso148_hco_plus.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[1], mode = "list")["cdelt1"])
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
                 imagename = imagenames[1],
                 chans = "15~40",
                 mask = "mask_eso148_hco_plus.mask",
                 thres = 0.0006 * 2.7)


### hcn_eso286
dir_data = "../../hcn_ulirgs/hcn_eso286/"

os.system("rm -rf " + dir_data + "mask2.image")
os.system("rm -rf " + dir_data + "*moment*")
fitsimages = glob.glob(dir_data + "*_hc*.fits")
for i in range(len(fitsimages)):
    os.system("rm -rf " + fitsimages[i].replace(".fits", ".image"))
    importfits(fitsimage = fitsimages[i],
               imagename = fitsimages[i].replace(".fits", ".image"))

imagenames = glob.glob(dir_data + "*_hc*.image")

# hcn43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = 0.0005 * 2.3,
                outmask = "mask_eso286_hcn.mask")

outmask = dir_data + "mask_eso286_hcn.mask"
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "10~35",
                 mask = "mask_eso286_hcn.mask",
                 thres = 0.0005 * 2.7)

# hco_plus43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[1].split("/")[-1],
                thres = 0.0006 * 2.3,
                outmask = "mask_eso286_hco_plus.mask")

outmask = dir_data + "mask_eso286_hco_plus.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[1], mode = "list")["cdelt1"])
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
                 imagename = imagenames[1],
                 chans = "10~35",
                 mask = "mask_eso286_hco_plus.mask",
                 thres = 0.0006 * 2.7)


### hcn_iras05189
dir_data = "../../hcn_ulirgs/hcn_iras05189/"

os.system("rm -rf " + dir_data + "mask2.image")
os.system("rm -rf " + dir_data + "*moment*")
fitsimages = glob.glob(dir_data + "*_hc*.fits")
for i in range(len(fitsimages)):
    os.system("rm -rf " + fitsimages[i].replace(".fits", ".image"))
    importfits(fitsimage = fitsimages[i],
               imagename = fitsimages[i].replace(".fits", ".image"))

imagenames = glob.glob(dir_data + "*_hc*.image")

# hcn43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = 0.0004 * 2.3,
                outmask = "mask_iras05189_hcn.mask")

outmask = dir_data + "mask_iras05189_hcn.mask"
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "5~41",
                 mask = "mask_iras05189_hcn.mask",
                 thres = 0.0004 * 2.7)

# hco_plus43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[1].split("/")[-1],
                thres = 0.00045 * 2.3,
                outmask = "mask_iras05189_hco_plus.mask")

outmask = dir_data + "mask_iras05189_hco_plus.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[1], mode = "list")["cdelt1"])
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
                 imagename = imagenames[1],
                 chans = "9~37",
                 mask = "mask_iras05189_hco_plus.mask",
                 thres = 0.0006 * 2.7)


### hcn_iras13120
dir_data = "../../hcn_ulirgs/hcn_iras13120/"

os.system("rm -rf " + dir_data + "mask2.image")
os.system("rm -rf " + dir_data + "*moment*")
fitsimages = glob.glob(dir_data + "*_hc*.fits")
for i in range(len(fitsimages)):
    os.system("rm -rf " + fitsimages[i].replace(".fits", ".image"))
    importfits(fitsimage = fitsimages[i],
               imagename = fitsimages[i].replace(".fits", ".image"))

imagenames = glob.glob(dir_data + "*_hc*.image")

# hcn43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = 0.0009 * 2.5,
                outmask = "mask_iras13120_hcn.mask")

outmask = dir_data + "mask_iras13120_hcn.mask"
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "7~46",
                 mask = "mask_iras13120_hcn.mask",
                 thres = 0.0009 * 3.0)

# hco_plus43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[1].split("/")[-1],
                thres = 0.0011 * 2.5,
                outmask = "mask_iras13120_hco_plus.mask")

outmask = dir_data + "mask_iras13120_hco_plus.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[1], mode = "list")["cdelt1"])
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
                 imagename = imagenames[1],
                 chans = "9~42",
                 mask = "mask_iras13120_hco_plus.mask",
                 thres = 0.0011 * 3.0)


### hcn_irasf12112
dir_data = "../../hcn_ulirgs/hcn_irasf12112/"

os.system("rm -rf " + dir_data + "mask2.image")
os.system("rm -rf " + dir_data + "*moment*")
fitsimages = glob.glob(dir_data + "*_hc*.fits")
for i in range(len(fitsimages)):
    os.system("rm -rf " + fitsimages[i].replace(".fits", ".image"))
    importfits(fitsimage = fitsimages[i],
               imagename = fitsimages[i].replace(".fits", ".image"))

imagenames = glob.glob(dir_data + "*_hc*.image")

# hcn43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = 0.0008 * 2.7,
                outmask = "mask_irasf12112_hcn.mask")

outmask = dir_data + "mask_irasf12112_hcn.mask"
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "12~68",
                 mask = "mask_irasf12112_hcn.mask",
                 thres = 0.0008 * 3.0)

# hco_plus43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[1].split("/")[-1],
                thres = 0.0008 * 2.7,
                outmask = "mask_irasf12112_hco_plus.mask")

outmask = dir_data + "mask_irasf12112_hco_plus.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[1], mode = "list")["cdelt1"])
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
                 imagename = imagenames[1],
                 chans = "24~72",
                 mask = "mask_irasf12112_hco_plus.mask",
                 thres = 0.0008 * 3.0)


### hcn_irasf17208
dir_data = "../../hcn_ulirgs/hcn_irasf17208/"

os.system("rm -rf " + dir_data + "mask2.image")
os.system("rm -rf " + dir_data + "*moment*")
fitsimages = glob.glob(dir_data + "*_hc*.fits")
for i in range(len(fitsimages)):
    os.system("rm -rf " + fitsimages[i].replace(".fits", ".image"))
    importfits(fitsimage = fitsimages[i],
               imagename = fitsimages[i].replace(".fits", ".image"))

imagenames = glob.glob(dir_data + "*_hc*.image")

# hcn43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = 0.00075 * 2.7,
                outmask = "mask_irasf17208_hcn.mask")

outmask = dir_data + "mask_irasf17208_hcn.mask"
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

myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "0~49",
                 mask = "mask_irasf17208_hcn.mask",
                 thres = 0.00075 * 3.0)

# hco_plus43
myim.createmask(dir_data = dir_data,
                imagename = imagenames[1].split("/")[-1],
                thres = 0.0008 * 2.7,
                outmask = "mask_irasf17208_hco_plus.mask")

outmask = dir_data + "mask_irasf17208_hco_plus.mask"
os.system("cp -r " + outmask + " " + outmask + ".all")
major = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beammajor")["value"]
minor = imhead(imagename = imagenames[1],
               mode = "get", hdkey = "beamminor")["value"]
pix = abs(imhead(imagename = imagenames[1], mode = "list")["cdelt1"])
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
                 imagename = imagenames[1],
                 chans = "7~64",
                 mask = "mask_irasf17208_hco_plus.mask",
                 thres = 0.0008 * 3.0)
