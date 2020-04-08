import os
import glob
import scripts_phangs_r21 as r21


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
galaxy = ["ngc0628",
          "ngc4321",
          #"ngc4254",
          "ngc3627"]
image_lengths = [280.,
                 230.,
                 #250.,
                 280.] # arcsec
direction_ras = ["24.174deg",
                 "185.729deg",
                 #"184.706deg",
                 "170.063deg"]
direction_decs = ["15.783deg",
                  "15.8223deg",
                  #"14.4169deg",
                  "12.9914deg"]
beams = [[6.0,8.0,10.0,12.0,13.6,14.0,16.0,18.0,20.0,22.0,33.0],
         [6.0,8.0,8.5,10.0,12.0,14.0,16.0,18.0,20.0,22.0,33.0],
         #[10.0,12.0,14.0,16.0,18.0,20.0,22.0,24.0,26.0,33.0],
         [10.0,12.0,14.0,15.0,16.0,18.0,20.0,22.0,24.0,26.0,33.0]]
#native = ["04p0","04p0","08p0"]


#####################
### Main
#####################
for i in range(len(galaxy)):
    galname = galaxy[i]
    print("### working on " + galname)
    """
    # preparation
    os.mkdir(dir_proj + galname + "_co10/")
    data_orig = glob.glob(dir_proj + "data_ready/" + galname + "_co10_*.image")[0]
    data_use = dir_proj + galname + "_co10/co10_cube.image"
    os.system("cp -r " + data_orig + " " + data_use)

    os.system("rm -rf " + outfile.replace(".image",".fits"))
    exportfits(imagename = data_use,
        fitsimage = data_use.replace(".image","_"+native[i]+".fits"))

    os.mkdir(dir_proj + galname + "_co21/")
    data_orig = glob.glob(dir_proj + "data_ready/" + galname + "_co21_*.image")[0]
    data_use = dir_proj + galname + "_co21/co21_cube.image"
    os.system("cp -r " + data_orig + " " + data_use)

    os.system("rm -rf " + outfile.replace(".image",".fits"))
    exportfits(imagename = data_use,
        fitsimage = data_use.replace(".image","_"+native[i]+".fits"))
    """
    #
    co10cube = glob.glob(dir_proj + galname + "_co10/*_cube.image")[0]
    co21cube = glob.glob(dir_proj + galname + "_co21/*_cube.image")[0]
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

        os.system("rm -rf " + outfile)
        imregrid(imagename = outfile + "_tmp",
                 template = "template.image",
                 output = outfile,
                 axes = [0,1])

        os.system("rm -rf " + outfile.replace(".image",".fits"))
        exportfits(imagename = outfile,
            fitsimage = outfile.replace(".image",".fits"))

        os.system("rm -rf " + outfile + "_tmp")

        # co21
        outfile = co21cube.replace("_cube","_cube_"+beamp)
        os.system("rm -rf " + outfile + "_tmp")
        imsmooth(imagename = co21cube,
                 targetres = True,
                 major = str(beams[i][j]) + "arcsec",
                 minor = str(beams[i][j]) + "arcsec",
                 pa = "0deg",
                 outfile = outfile + "_tmp")

        os.system("rm -rf " + outfile)
        imregrid(imagename = outfile + "_tmp",
                 template = "template.image",
                 output = outfile,
                 axes = [0,1])
        os.system("rm -rf template.image")

        exportfits(imagename = outfile,
            fitsimage = outfile.replace(".image",".fits"))

        os.system("rm -rf " + outfile + "_tmp")

os.system("rm -rf *.last template.fits template.im")
