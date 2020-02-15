import os
import glob
import scipy
from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.ioff()

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
dir_data = "/Users/saito/data/myproj_active/proj_jwu01_ngc6240/data/"
imagenames = glob.glob(dir_data + "*.smooth.regrid")
imagenames.sort()
noises = [0.0011,0.005,0.0006,0.0004,0.0004]
pbcuts = [0.75,0.35,0.9,0.9,0.9]
snr = 2.0


#####################
### Functions
#####################
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

def func1(x, a, c):
    return a*np.exp(-(x)**2/(2*c**2))

def noisehist(imagename,noises_byeye,output,bins=200,thres=0.00001):
    """
    """
    shape = imhead(imagename,mode="list")["shape"]
    box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
    data = imval(imagename,box=box)
    pixvalues = data["data"].flatten()
    pixvalues = pixvalues[abs(pixvalues)>thres]
    
    # plot
    histrange = [pixvalues.min()/1.5-0.02,-pixvalues.min()/1.5+0.02]
    plt.figure(figsize=(10,10))
    plt.rcParams["font.size"] = 22
    histdata = plt.hist(pixvalues,
                        bins=bins,
                        range=histrange,
                        lw=0,
                        log=True,
                        color="blue",
                        alpha=0.5)
        
    popt, pcov = curve_fit(func1,
                           histdata[1][2:][histdata[1][2:]<noises_byeye],
                           histdata[0][1:][histdata[1][2:]<noises_byeye],
                           p0 = [np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]),
                                 noises_byeye],
                           maxfev = 10000)
                        
    x = np.linspace(histdata[1][1], histdata[1][-1], 200)
    plt.plot(x, func1(x, popt[0], popt[1]),
             '-', c="black", lw=5, label = "1 sigma = " + str(np.round(popt[1]*1000,2)) + " mJy beam$^{-1}$")
    plt.plot([0,0],
             [1e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*8.0],
             '-',color='black',lw=2)
    plt.plot([popt[1],popt[1]],
             [1e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*8.0],
             '--',color='black',lw=2)
    plt.plot([popt[1]*2.5,popt[1]*2.5],
             [1e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*8.0],
             '--',color='black',lw=4)
    plt.plot([-popt[1],-popt[1]],
             [1e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*8.0],
             '--',color='black',lw=2)
                        
    plt.title(imagename.split("/")[-1])
    plt.xlim(histrange)
    plt.ylim([1e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*8.0])
    plt.xlabel("Pixel value (Jy beam$^{-1}$)")
    plt.ylabel("Number of pixels")
    plt.legend(loc = "upper right")
    plt.savefig(output,dpi=100)
                        
    return popt[1]


#####################
### Main
#####################
dir_eps = dir_data + "../eps/"
done = glob.glob(dir_eps)
if not done:
    os.mkdir(dir_eps)

for i in range(len(imagenames)):
    # prepare workinf directory e.g., image_co10
    name_line = imagenames[i].split("ngc6240_")[1].split("_")[0]
    dir_image = dir_data+"../image_"+name_line+"/"
    pbimage = dir_image + name_line + "_cube.pb"
    cubeimage = dir_image + name_line + "_cube.image"
    os.system("rm -rf " + dir_image)
    os.system("mkdir " + dir_image)
    os.system("cp -r " + imagenames[i] + " " + cubeimage)
    os.system("cp -r " + imagenames[i].replace("smooth","pb") + " " + pbimage)

    print("### woking on " + name_line)
    # noise histgrams
    output = dir_eps + "noise_" + name_line + ".png"
    popt1 = noisehist(imagenames[i],noises[i],output,bins=200,thres=0.0001)

    # imsmooth
    cubesmooth1 = cubeimage.replace(".image",".smooth1") # 4.0 mJy
    imsmooth(imagename = cubeimage,
             targetres = True,
             major = "1.2arcsec",
             minor = "1.2arcsec",
             pa = "0deg",
             outfile = cubesmooth1)

    cubesmooth2 = cubeimage.replace(".image",".smooth2") # 10 mJy
    imsmooth(imagename = cubeimage,
             targetres = True,
             major = "3.5arcsec",
             minor = "3.5arcsec",
             pa = "0deg",
             outfile = cubesmooth2)

    # create mask
    createmask(cubeimage,popt1*1.*2.0,dir_image+"/"+name_line+"_mask0.image")
    createmask(cubesmooth1,popt1*2.*4.5,dir_image+"/"+name_line+"_mask1.image")
    createmask(cubesmooth2,popt1*5.*9.0,dir_image+"/"+name_line+"_mask2.image")
    
    immath(imagename = [dir_image+"/"+name_line+"_mask0.image",
                        dir_image+"/"+name_line+"_mask1.image",
                        dir_image+"/"+name_line+"_mask2.image",
                        dir_image+"/"+name_line+"_cube.pb"],
           expr = "iif(IM0+IM1+IM2 >= 2.0, 1.0, 0.0)",
           outfile = dir_image+"/"+name_line+"_mask_tmp.image")
        
    immath(imagename = [dir_image+"/"+name_line+"_mask_tmp.image",
                        dir_image+"/"+name_line+"_cube.pb"],
           expr = "iif(IM1 >= "+str(pbcuts[i])+", IM0, 0.0)",
           outfile = dir_image+"/"+name_line+"_mask.image")

    os.system("rm -rf "+dir_image+"/"+name_line+"_cube.smooth1")
    os.system("rm -rf "+dir_image+"/"+name_line+"_cube.smooth2")
    os.system("rm -rf "+dir_image+"/"+name_line+"_mask0.image")
    os.system("rm -rf "+dir_image+"/"+name_line+"_mask1.image")
    os.system("rm -rf "+dir_image+"/"+name_line+"_mask2.image")
    os.system("rm -rf "+dir_image+"/"+name_line+"_mask_tmp.image")
    
    impbcor(imagename = cubeimage,
            pbimage = pbimage,
            cutoff = 0.3,
            outfile = cubeimage+".pbcor")
            
    immath(imagename = [cubeimage+".pbcor",dir_image+"/"+name_line+"_mask.image"],
           expr = "IM0*IM1",
           outfile = cubeimage+".pbcor.masked")
    
    immoments(imagename = cubeimage+".pbcor.masked",
              moments = [0],
              includepix = [popt1*snr,100000.],
              outfile = dir_image+"/"+name_line+".moment0")
        
    immoments(imagename = cubeimage+".pbcor.masked",
              moments = [1],
              includepix = [popt1*snr,100000.],
              outfile = dir_image+"/"+name_line+".moment1")
              
    immoments(imagename = cubeimage+".pbcor.masked",
              moments = [8],
              includepix = [popt1*snr,100000.],
              outfile = dir_image+"/"+name_line+".moment8")


