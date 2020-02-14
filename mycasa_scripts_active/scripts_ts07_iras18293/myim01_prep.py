import os
import glob
import numpy as np
from astropy.coordinates import SkyCoord

dir_data = "/Users/saito/data/myproj_published/proj_ts07_iras18293/data_raw/"
imagename= dir_data + "iras18293_co10_12m_l10_br.image.smooth"
imagenames = glob.glob(dir_data + "*.smooth")
imagenames.extend(glob.glob(dir_data + "*.pb"))

#####################
### Main Procedure
#####################
# get native grid information
num_x_pix = imhead(imagename,mode="list")["shape"][0]
num_y_pix = imhead(imagename,mode="list")["shape"][1]
pix_radian = imhead(imagename,mode="list")["cdelt2"]
obsfreq = imhead(imagename,mode="list")["crval4"]/1e9
pix_arcsec = round(pix_radian * 3600 * 180 / np.pi, 3)

# create tempalte image
blc_ra_tmp=imstat(imagename)["blcf"].split(", ")[0]
blc_dec_tmp=imstat(imagename)["blcf"].split(", ")[1]
blc_ra = blc_ra_tmp.replace(":","h",1).replace(":","m",1)+"s"
blc_dec = blc_dec_tmp.replace(".","d",1).replace(".","m",1)+"s"
beamsize=round(imhead(imagename,"list")["beammajor"]["value"], 2)
pix_size=round(beamsize/4.53, 2)
size_x = int(21. * 300. / obsfreq / pix_size)
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

importfits(fitsimage="template.fits",
           imagename="template.image")


# regrid
os.system("rm -rf " + dir_data.replace("data_raw","data"))
os.system("mkdir " + dir_data.replace("data_raw","data"))
for i in range(len(imagenames)):
    os.system("rm -rf "+imagenames[i]+".regrid")
    imregrid(imagename=imagenames[i],
             template="template.image",
             output=imagenames[i].replace("data_raw","data")+".regrid",
             axes=[0,1])

ia.close()
cl.close()

os.system("rm -rf template.*")
os.system("rm -rf *.last")
