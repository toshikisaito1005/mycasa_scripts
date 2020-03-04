import os
import glob
sys.path.append(os.getcwd())
import toolsJu01Ssc as tl


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_published/proj_ju01_ssc/"
#dir_proj = "../"

galaxy = ["am2038"]
#galaxy = ["am0956","am1158","am1255","am1300","am2038"
#          "am2055","arp230","ngc3597","ngc7135"]


#####################
### def
#####################


#####################
### Main
#####################
for i in range(len(galaxy)):
    # import datacube
    galname = galaxy[i]
    datacube = glob.glob(dir_proj + galname + "/*12m7m.image")[0]
    pbimage = datacube.replace(".image",".pb")
    
    # make maskcube for immoments
    rms, snr, pbcut = tl.know_imaging_keys3(galname)
    datacube2 = datacube + "_tmp"
    os.system("rm -rf " + datacube2)
    immath(imagename = [datacube,pbimage],
           expr = "iif(IM1 >= " + str(pbcut) + ", IM0, 0.0)",
           outfile = datacube2)
           
    outmask = datacube + ".mask4mom"
    tl.createmask(datacube2,rms*snr,outmask)
    beamarea_pix = tl.beam_area(datacube)
    tl.removesmallmasks(outmask,beamarea_pix)
    os.system("rm -rf " + datacube2 + " " + outmask)

    # convolve maskcube
    bmaj = imhead(datacube,"list")["beammajor"]["value"]
    round_beam = str(np.round(bmaj,1) * 1.5) + "arcsec"

    outfile = outmask + ".smooth_tmp"
    os.system("rm -rf " + outfile)
    imsmooth(imagename = outmask + ".min",
             targetres = True,
             major = round_beam,
             minor = round_beam,
             pa = "0deg",
             outfile = outfile)

    tl.createmask(outmask + ".smooth_tmp",0.1,outmask + ".smooth")
    os.system("rm -rf " + outmask + ".smooth_tmp " + outmask + ".min")

    # moment
    datacubes = glob.glob(dir_proj + galname + "/*12m*.image")
    for j in range(len(datacubes)):
        datacube = datacubes[j]
        os.system("rm -rf " + datacube+".pbcor")
        impbcor(imagename = datacube,
                pbimage = pbimage,
                outfile = datacube+".pbcor")
        os.system("rm -rf " + datacube+".pbcor.masked")
        immath(imagename = [datacube+".pbcor", outmask + ".smooth"],
               expr = "IM0*IM1",
               outfile = datacube+".pbcor.masked")

        os.system("rm -rf " + datacube.replace(".image",".moment*"))
        immoments(imagename = datacube+".pbcor.masked",
                  moments = [0],
                  includepix = [rms*2.5,1000000.],
                  outfile = datacube.replace(".image",".moment0"))

        immoments(imagename = datacube+".pbcor.masked",
                  moments = [1],
                  includepix = [rms*2.5,1000000.],
                  outfile = datacube.replace(".image",".moment1"))

        immoments(imagename = datacube+".pbcor.masked",
                  moments = [8],
                  includepix = [rms*2.5,1000000.],
                  outfile = datacube.replace(".image",".moment8"))
        os.system("rm -rf " + datacube+".pbcor.masked")

os.system("rm -rf  *.last")
