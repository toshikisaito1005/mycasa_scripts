import os
import glob

from spectral_cube import SpectralCube
import astropy.units as u
from astropy.io import fits
import numpy as np
from radio_beam import Beam
import scDerivativeRoutines as scderive
import scMaskingRoutines as scmask

import scMoments as scmoments

scmoments.moment_generator(
  cubefile = "co10_cube_04p0.fits",
  root_name = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/ngc0628_co10/")

scderive.write_moment0