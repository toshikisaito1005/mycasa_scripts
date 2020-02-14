import numpy as np
import math
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.optimize
from scipy.optimize import curve_fit
import matplotlib.colors as clr
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u
plt.ioff()


#####################
### Define Parameters
#####################
cosmo = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)


#####################
### Main Procedure
#####################
dir_data = "../../aca_yamashita/"
dir_fits = dir_data + "data/"
dir_momnt = dir_data + "moment/"
dir_product = dir_data + "product/"

### moment map creation
os.system("mkdir " + dir_momnt)

### moment 0
fitsfiles = glob.glob(dir_fits + "*.fits")

chans_all = ["16~34", # ms0074
             "18~31", # ms0362
             "19~29", # ms0617
             "16~33", # ms1126
             "18~31", # ms1181
             "23~26", # ms1699
             "19~30", # ms2018
             "20~28", # ms2400
             "20~29", # ms2816
             "19~30", # ms3003
             "15~33", # ms3271
             "20~28", # ms4090
             "16~26", # ms4517
             "18~29", # ms4777
             "21~27", # ms5158
             "15~33", # ms5829
             "20~29", # ms5961
             "18~30", # ms6312
             "20~29", # ms6552
             "19~30", # ms6610
             "19~29", # ms6790
             "15~34", # ms7069
             "16~33", # ms7100
             "16~34", # ms7278
             "0~1", # ms7785 non-detection?
             "15~33", # ms7882
             "22~28", # ms7994
             "19~29", # ms8271
             "19~29", # ms8714
             "18~31", # ms8885
             "21~28", # ms9127
             "21~27", # ms9201
             "17~31", # ms9403
             "15~33", # ms9438
             "17~32", # ms9913
             "11~36", # vv1105
             "12~33", # vv1607
             "11~38", # vv231
             "4~32", # vv285
             "3~48", # vv316 wider velocity imaging!
             "18~29", # vv352n
             "16~32", # vv352s
             "13~33", # vv492
             "12~36", # vv55n
             "13~38", # vv55s
             "20~28", # vv565
             "0~48", # vv617 wider velocity imaging! (ngc6240)
             "12~39", # vv642
             "13~37", # vv691
             "17~32", # vv754n
             "17~32", # vv754s
             "14~38", # vv75
             "12~37", # vv822
             "2~29", # vv847
             "3~28", # vv987
             "17~29", # vv989
             ]

done = glob.glob(dir_product)
if not done:
    os.system("mkdir " + dir_product)

product_file = dir_product + "output_size.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#num target maj err min err\n")
f.close()

for i in range(len(fitsfiles)):
#for i in range(1):
    naming = fitsfiles[i].split("/")[-1].replace(".fits",".moment0")
    outfile = dir_momnt + naming
    os.system("rm -rf " + outfile)
    immoments(imagename = fitsfiles[i],
              moments = [0],
              chans = chans_all[i],
              outfile = outfile)
    imfit(imagename = outfile,
          logfile = outfile + "_imfit.txt",
          residual = outfile + ".residual")

    f = open(outfile + "_imfit.txt")
    lines = f.readlines()
    f.close()

    freq_obs = float(lines[45].split(":")[1].split("GHz")[0])
    z = 230.53800 / freq_obs - 1
    DL = float(str(cosmo.luminosity_distance(z)).split(" Mpc")[0])
    arcsec2pc = np.tan(np.radians(1/3600.)) * DL * 10**6

    size_tmp = lines[35].split(":")[1]
    size_maj = str(int(float(size_tmp.split("+/-")[0]) * arcsec2pc))
    err_maj = str(int(float(size_tmp.split("+/-")[1].split("arc")[0]) * arcsec2pc))
    
    size_tmp = lines[36].split(":")[1]
    size_min = str(int(float(size_tmp.split("+/-")[0]) * arcsec2pc))
    err_min = str(int(float(size_tmp.split("+/-")[1].split("arc")[0]) * arcsec2pc))

    f = open(product_file, "a")
    f.write(str(i) + " " + naming.split("_7m_co21.moment0")[0] + " " \
            + size_maj + " " + err_maj + " " \
            + size_min + " " + err_min + "\n")
    f.close

