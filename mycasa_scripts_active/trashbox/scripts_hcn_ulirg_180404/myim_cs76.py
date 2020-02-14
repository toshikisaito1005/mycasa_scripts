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
spw_cs76 = glob.glob("../../hcn_ulirgs/hcn_*/*spw0*.fits")
spw_cs76.pop(0)
chan_cs76 = ["5~14", "0~9", "6~14", "2~15", "2~18"]
rms_cs76 = [0.0008, 0.0006, 0.0009, 0.0006, 0.0013]


for k in range(len(spw_cs76)):
    outmask = spw_cs76[k].split("/")[3].replace("hcn", "cs")
    dir_data = spw_cs76[k].split("/")[0] + "/" + spw_cs76[k].split("/")[1] + "/" + spw_cs76[k].split("/")[2] + "/" + spw_cs76[k].split("/")[3] + "/"
    myim.createmask(dir_data = dir_data,
                    imagename = spw_cs76[k].split("/")[-1],
                    thres = rms_cs76[k] * 2.5,
                    outmask = outmask)
    os.system("cp -r " + dir_data + outmask + " " + dir_data + outmask + ".all")
    major = imhead(imagename = spw_cs76[k],
                   mode = "get", hdkey = "beammajor")["value"]
    minor = imhead(imagename = spw_cs76[k],
                   mode = "get", hdkey = "beamminor")["value"]
    pix = abs(imhead(imagename = spw_cs76[k],
                     mode = "list")["cdelt1"])
    pixelsize = pix * 3600 * 180 / np.pi
    beamarea = (major * minor * np.pi/(4 * np.log(2))) / (pixelsize ** 2)
    ia.open(dir_data + outmask)
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
                     imagename = dir_data + spw_cs76[k].split("/")[-1],
                     chans = chan_cs76[k],
                     mask = outmask,
                     thres = rms_cs76[k] * 2.7)
    os.system("mv " + dir_data + spw_cs76[k].split("/")[-1]+".moment0 " + dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment0")
    os.system("mv " + dir_data + spw_cs76[k].split("/")[-1]+".moment1 " + dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment1")
    os.system("mv " + dir_data + spw_cs76[k].split("/")[-1]+".moment2 " + dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment2")
    fits_hcn = glob.glob(dir_data + "*hcn43*moment0*.fits")
    template_hcn = fits_hcn[0].replace(".fits", ".image")
    importfits(fitsimage = dir_data + fits_hcn[0],
               imagename = dir_data + template_hcn)
    imregrid(imagename = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment0",
             template = template_hcn,
             output = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment0.regrid",
             overwrite = True)
    imregrid(imagename = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment1",
             template = template_hcn,
             output = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment1.regrid",
             overwrite = True)
    imregrid(imagename = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment2",
             template = template_hcn,
             output = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment2.regrid",
             overwrite = True)
    exportfits(imagename = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment0.regrid",
               fitsimage = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment0.fits")
    exportfits(imagename = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment1.regrid",
               fitsimage = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment1.fits")
    exportfits(imagename = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment2.regrid",
               fitsimage = dir_data + spw_cs76[k].split("/")[-1].split("_AL2B6")[0] + "_cs76.moment2.fits")
    os.system("rm -rf " + dir_data + "cs_*")
    os.system("rm -rf " + dir_data + template_hcn)
    os.system("rm -rf " + dir_data + spw_cs76[k].split("/")[-1] + ".moment*")
    os.system("rm -rf " + dir_data + "*_cs76.moment0")
    os.system("rm -rf " + dir_data + "*_cs76.moment1")
    os.system("rm -rf " + dir_data + "*_cs76.moment2")
    os.system("rm -rf " + dir_data + "*_cs76.moment*.regrid")
    os.system("rm -rf " + dir_data + "mask2.image")

