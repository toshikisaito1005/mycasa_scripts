# README for mycasaimaging_scripts
## Requirement
### Astropy in CASA
You need to use astropy inside CASA.  To do so, follow the instruction below (http://docs.astropy.org/en/stable/install.html#installing-astropy-into-casa).

Start up CASA as normal, and type:
```
> from setuptools.command import easy_install
> easy_install.main(['--user', 'pip'])
```
Now, quit CASA and re-open it, then type the following to install Astropy:
```
> import pip
> pip.main(['install', 'astropy', '--user'])
```
Then close CASA again and open it, and you should be able to import Astropy:
```
> import astropy
```


### Analysis Utilities
see this link.
```
CASA Guides: https://casaguides.nrao.edu/index.php?title=Analysis_Utilities
Nagai-san's instruction (in Japanese): http://alma-intweb.mtk.nao.ac.jp/~nagai/ALMAdata/index5.html
```
~/.casa/init.py should be like this.
```
import sys 
sys.path.append("/PATH_TO_ANALYSIS_SCRIPTS/")
import analysisUtils as aU 
es = aU.stuffForScienceDataReduction()
```


## Get started
run this command wherever you want to decompress.
```
> git clone https://github.com/toshikisaito1005/phangs_visual_qa_scripts.git
```


## Example
### execfile("mycasaimaging_moments.py")
Edit those parameters.
```
dir_data         = "../data/"       # relative path to your data
pixelmin         = 5.               # remove small mask reions smaller than beamsize * pixelmin
imagename        = "hogehoge.image" # your CASA cube name
rms              = 0.001            # pixel rms per channel
threshold_mask   = 2.               # threshold for masking: rms * threshold_mask
chans            = "10~20"          # select channnels for immoments
threshold_moment = 3.               # thrshold for immomenths: rms * threshold_moment
```


### execfile("mycasaimaging_eps.py")
Edit those parameters.
Matplotlib colormap reference (https://matplotlib.org/examples/color/colormaps_reference.html)
```
dir_data          = "../data/"                             # relative path to your images
ra_center         = "10:04:02.090"                         # image center
dec_center        = "-6.28.29.604"                         # image center
value             = 10.                                    # if value is not defined, value = image peak
contour           = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]   # contour * value
xlim              = [-30, 30]                              # image area (arcsec) from the image center
ylim              = [30, -30]                              # image area (arcsec) from the image center

imagename_contour = "moment0.fits"                         # moemnt 0 image
imagename_color   = "moment0.fits"                         # moment 1 image
title             = "$^{12}$CO (1-0) Integrated Intensity" # eps title
colorscale        = "PuBu"                                 # colorscale
colorlog          = True                                   # logsaled colorbar if True
colorbar          = False                                  # show colorbar if True
clim              = [-300, 300]                            # color range, if not defiend, clim = [min, max]
colorbar_label    = "(Jy km s$^{-1}$)"                     # eps colorbar label
output            = "12co10_m0.eps"                        # output file name
```

<img src="https://user-images.githubusercontent.com/29215245/36950915-2ef94464-1ffd-11e8-83de-dcfe215efdab.png" width="500pix">
<img src="https://user-images.githubusercontent.com/29215245/36950918-309b5bb8-1ffd-11e8-8923-65a147d352ae.png" width="500pix">
