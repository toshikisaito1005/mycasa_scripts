import os
import glob
from astropy import units as u


# WISE data = MJy/sr


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_other/wise/"
dir_product_pre = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
galaxy = ["ngc0628",
          "ngc4321",
          "ngc3627"]
image_lengths = [280.,
                 230.,
                 280.] # arcsec
direction_ras = ["24.174deg",
                 "185.729deg",
                 "170.063deg"]
direction_decs = ["15.783deg",
                  "15.8223deg",
                  "12.9914deg"]
beams = [[13.6],
         [8.2],
         [15.0]]


#####################
### Main
#####################
for i in range(len(galaxy)):
    galname = galaxy[i]
    print("### working on " + galname + " wise")

    dir_product = dir_product_pre + galname + "_wise/"
    done = glob.glob(dir_product)
    if not done:
        os.mkdir(dir_product)

    wisefits = glob.glob(dir_proj + galname + "*_gauss7p5.fits")

    for j in range(len(beams[i])):
        beamp = str(beams[i][j]).zfill(4).replace(".","p")
        print("# working on beam = "+beamp)
        
        for k in range(len(wisefits)):
            # import FITS to CASA
            imagename = dir_product + wisefits[k].split("/")[-1].replace(".fits",".image")
            os.system("rm -rf " + imagename + "_tmp")
            importfits(fitsimage = wisefits[k],
                       imagename = imagename + "_tmp")

            imhead(imagename = imagename + "_tmp",
                   mode = "add",
                   hdkey = "beammajor",
                   hdvalue = "7.5arcsec")

            imhead(imagename = imagename + "_tmp",
                   mode = "put",
                   hdkey = "beamminor",
                   hdvalue = "7.5arcsec")


