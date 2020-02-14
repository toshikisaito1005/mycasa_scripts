import os
import glob
import numpy as np


dir_data = "../../myproj_published/proj_phangs03_outflow/data/"
galaxy = ["ngc6300"]


#####################
### Main Procedure
#####################
# import galaxy information
galinfo = np.loadtxt("key_galaxy.txt",dtype="S100")

#
for i in range(len(galaxy)):
    # import galinfo
    galname = galaxy[i]
    smooth_beam = galinfo[np.where(galinfo[:,0]==galname)][0,2]
    
    # mkdir
    dir_working = dir_data + "../" + galname + "/"
    os.system("rm -rf " + dir_working)
    os.mkdir(dir_working)

    imagename = glob.glob(dir_data + galname + "*12m+7m+tp*.image")[0]

    # imsmooth
    beamsize = imhead(imagename,"list")["beammajor"]["value"]
    outfile1 = dir_working + galname + ".cube.imsmooth_tmp"
    os.system("rm -rf " + outfile1)
    imsmooth(imagename = imagename,
             targetres = True,
             major = smooth_beam + "arcsec",
             minor = smooth_beam + "arcsec",
             pa = "0.0deg",
             outfile = outfile1)

    # imrebin
    cell = np.abs(imhead(outfile1,mode="list")["cdelt1"])*180.*3600./np.pi
    nbin = int(float(smooth_beam) / 4.53 / cell)
    outfile2 = dir_working + galname + ".cube.imsmooth"
    imrebin(imagename = outfile1,
            outfile = outfile2,
            factor = [nbin, nbin])
    os.system("rm -rf " + outfile1)

    # specsmooth
    outfile3 = dir_working + galname + ".cube.imsmooth.specsmooth"
    os.system("rm -rf " + outfile3)
    specsmooth(imagename = outfile2,
               outfile = outfile3,
               function = "hanning")

os.system("rm -rf *.last")
