import os
import sys
import glob
from scipy import fftpack
import pyfits
import numpy as np
import pylab as py
sys.path.append(os.getcwd())
import radialProfile
py.ioff()

# https://www.astrobetter.com/blog/2010/03/03/fourier-transforms-of-images-in-python/
moms = glob.glob("../*/*moment0")
for i in range(len(moms)):
#for i in range(1):
    # moment map manipulation
    os.system("rm -rf "+moms[i]+".box_tmp1_")
    imregrid(imagename=moms[i],
             template="J2000",
	     output=moms[i]+".box_tmp1_")

    os.system("rm -rf "+moms[i]+".box_tmp2_")
    immath(imagename=moms[i]+".box_tmp1_",
           expr="IM0",
	   outfile=moms[i]+".box_tmp2_",
	   box="31,32,158,159")

    # create taper function
    cl.addcomponent(dir="185.470deg, 4.47367deg",
        flux=1.0,
	fluxunit="Jy",
	freq="100GHz",
	shape="Gaussian",
	majoraxis="65.0arcsec",
	minoraxis="65.0arcsec",
	positionangle="0.0deg")

    ia.fromshape(moms[i]+"_tp_func.image",
        [128,128,1,1],
	overwrite=True)
    cs=ia.coordsys()
    cs.setunits(["rad","rad","","Hz"])
    cell_rad=qa.convert(qa.quantity("1.0arcsec"),"rad")["value"]
    cs.setincrement([-cell_rad,cell_rad], "direction")
    cs.setreferencevalue([qa.convert("185.470deg", "rad")["value"],
                          qa.convert("4.47367deg", "rad")["value"]],
			 type="direction")
    cs.setreferencevalue("100GHz","spectral")
    cs.setincrement("1GHz","spectral")
    ia.setcoordsys(cs.torecord())
    ia.setbrightnessunit("Jy/pixel")
    ia.modify(cl.torecord(),subtract=False)
    cl.done()
    cl.close()
    ia.close()

    # taper
    os.system("rm -rf "+moms[i]+".box_tmp3_")
    maxval = imstat(moms[i]+"_tp_func.image")["max"][0]
    immath(imagename=[moms[i]+".box_tmp2_",moms[i]+"_tp_func.image"],
           expr="IM0*IM1/"+str(maxval),
	   outfile=moms[i]+".box_tmp3_")

    os.system("rm -rf "+moms[i]+".fits")
    exportfits(imagename=moms[i]+".box_tmp3_",
               fitsimage=moms[i]+".fits",
	       dropstokes=True,
	       dropdeg=True)

    os.system("rm -rf "+moms[i]+".box_tmp*_")

    # FFT
    image = pyfits.getdata(moms[i]+".fits")

    F1 = fftpack.fft2(image.astype(float))

    F2 = fftpack.fftshift(F1)

    psd2D = np.abs(F2)**2
    psd1D = radialProfile.azimuthalAverage(psd2D)
 
    py.figure(1)
    py.clf()
    py.imshow(np.log10(image), cmap=py.cm.Greys)
    py.savefig(moms[i]+"_image.png")

    py.figure(2)
    py.clf()
    py.imshow(np.log10(psd2D))
    np.savetxt(moms[i]+"_psd2d.txt", psd2D)

    py.savefig(moms[i]+"_psd2d.png")

    py.figure(3)
    py.clf()
    py.xlim([0,10])
    #py.xlim([0,90])
    py.ylim([8,13])
    #py.ylim([10**-1,10**1.2])
    py.semilogy(np.log10(psd1D))
    py.savefig(moms[i]+"_psd1d.png")

os.system("rm -rf *.last")
