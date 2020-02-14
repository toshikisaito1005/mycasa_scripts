# README.md for scripts_phangs04_school

## History
2019-12-13: start at MPIA


## General
This is a project preparing for internal PHANGS-ALMA school on January 14th, 2020. My task is to "present 1-2 use cases (to make things more obvious): for instance, when do we need 12m+7m+TP vs 12m+7m, or how/when to access the data cube vs the moments."

We could just do something super simple, e.g.,

(i) measure the flux within the 12m+7m+tp and 12m+7m cubes (in Jy, and also estimate total solar masses of H2 using Galactic XCO)

(ii) plot pixel-by-pixel correlation of moment-0 maps from 12m+7m+tp and 7m+tp, including convolve to same resolution, regridding and application of common FoV mask (based on tpeak image).

## How to run
1. execfile("myscript01_prep_multibeam.py")
2. execfile("myscript02_prep_all_gals.py")
3. execfile("myscript03_diffmap_ngc0628.py")
4. execfile("myfig*.py")

## Data
releast v3p4

## Versions
CASA Version 5.4.0-70

## Directory Structure
data/
  - mycasa_scripts_active/ - scripts_phangs04_school/   # all scripts
  - myproj_*/ - proj_phangs04_school/ - data_raw/  # all data required
