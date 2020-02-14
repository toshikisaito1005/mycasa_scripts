import os
import sys
import re
import glob
import numpy as np
import scipy
import matplotlib.pyplot as plt

DL = 69.4 # Mpc
redshift = 0.016858


#####################
### function
#####################
def measure_beamarea(imagename):
    bmaj = imhead(imagename,"list")["beammajor"]["value"]
    bmin = imhead(imagename,"list")["beamminor"]["value"]
    pix = abs(imhead(imagename,"list")["cdelt1"])
    beamarea = np.pi * bmaj * bmin / 4. / (pix * 3600 * 180 / np.pi)**2

    return beamarea


#####################
### Main Procedure
#####################
dir_data = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/image_nyquist/"
txt_data = "ngc3110_all_sum.txt"
data = np.loadtxt(dir_data + txt_data)
data_ra = data[:,0]
data_dec = data[:,1]
data_12co10 = data[:,2]
#data_12co21 = data[:,3]
#data_13co10 = data[:,4]
#data_13co21 = data[:,5]
#data_c18o21 = data[:,6]
data_1p45GHz = data[:,7]
data_b3 = data[:,8]
data_b6 = data[:,9]
data_alpha = data[:,10]
data_ssc = data[:,11]

### parameters
area = np.pi * (0.325 * 3. / 2.)**2

# spectral index
contindex = np.log10(data_b6/data_b3)/np.log10(234.6075/104.024625)
for i in range(len(contindex)):
    if data_b3[i] == 0.:
        contindex[i] = 0.

contindex[np.where(np.isinf(contindex))] = 0
contindex[np.where(np.isnan(contindex))] = 0

# corr-SFR density
lumi_halpha = data_alpha * 36.5 * 4. * np.pi * (69.4 * 10**6. * 3. * 10.**18.)**2.
lumi_vla = data_1p45GHz / 17.5873 * 1.e-23 * (4. * np.pi * (69.4 * 1000000. * 3086000000000000000.) ** 2.)
sfr = (lumi_halpha + 0.39e+13 * lumi_vla) / 10. ** 41.27
density_sfr = sfr / area

# SSC number density
beamarea = measure_beamarea(dir_data+"../image_others/ssc.image")
density_ssc = data_ssc / beamarea / area

# CO(1-0) luminosity
nu_obs = 115.27120 / (1+redshift)
beamarea = measure_beamarea(dir_data+"../image_12co10/12co10.moment0")
data_12co10_Jykms = data_12co10 / beamarea
lumi_co10 = 3.25e+7 * data_12co10_Jykms / nu_obs**2 * DL**2 / (1+redshift)**2

# SFE using alpha_co = 1.1
gmass = lumi_co10 * 1.1
sfe = sfr / gmass * 10**9
sfe[np.where(np.isinf(sfe))] = 0
sfe[np.where(np.isnan(sfe))] = 0

# export
data2export = np.c_[np.round(data_ra,5),
                    np.round(data_dec,5),
                    np.round(contindex,2),
                    np.round(density_sfr,4),
                    np.round(density_ssc,4),
                    np.round(lumi_co10,-4),
                    np.round(sfe,2)]

os.system("rm -rf " + dir_data + "ngc3110_params.txt")
np.savetxt(dir_data + "ngc3110_params.txt",
           data2export,
           fmt = "%.7e",
           header="ra dec spec_index sfr_density ssc_density co10_lumi sfe")

