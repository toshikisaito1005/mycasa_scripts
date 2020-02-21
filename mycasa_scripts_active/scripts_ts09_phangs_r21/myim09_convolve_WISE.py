import os
import glob


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_other/wise/"
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
    wisefits = glob.glob(dir_proj + galname + "*_gauss7p5.fits")
    for j in range(len(beams[i])):
        beamp = str(beams[i][j]).zfill(4).replace(".","p")
        print("# working on beam = "+beamp)
        # co10
        outfile = co10cube.replace("_cube","_cube_"+beamp)
        os.system("rm -rf " + outfile + "_tmp")
        imsmooth(imagename = co10cube,
                 targetres = True,
                 major = str(beams[i][j]) + "arcsec",
                 minor = str(beams[i][j]) + "arcsec",
                 pa = "0deg",
                 outfile = outfile + "_tmp")

        r21.gridtemplate(outfile + "_tmp",
                         image_lengths[i],
                         direction_ras[i],
                         direction_decs[i])
