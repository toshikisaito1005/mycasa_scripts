# README.md for scripts_ju01_ssc

## History
2019-11-26: start at MPIA

2019-11-29: imaging am2038

2019-11-30: add; imaging other galaxies

2019-11-31: add; moment map creation with masking

## General

This is a project aiming at combining ALMA 12m, ACA 7m, and ACA TP data from different cycles including cycle 0. tp2vis (https://github.com/tp2vis/distribute) is used for joint deconvolution.

## Memo
1. statwt requires for different cycle data including cycle 0.
2. Convolving to larger beam is required to recover low surface brightness emission.
3. Do not use **uvtaper** parameter in tclean (something is strange...), use imsmooth instead.
4. May need to re-run uvcontsub because non-negligible contribution from CN lines?
5. 7m and 12m ALMA ms files should be **split**ed in advance (i.e., no corrected column and a single science field).
6. tclean is not optimized for all galaxies as well as moment map creation. Modify key_imaging.txt.
7. TP weight may not be optimized. Modify tp2viswt_multiply in key_makems.txt.

## How to run
0. fill key_rawdata.txt properly (already done).
0. run myscript00_fill_key_makems.py and fill key_makems.txt (already done).
1. execfile("myscript01_makems.py") # This creates regridded ms files (tp, 7m, and 12m) based on parameters wrriten in key_makems.txt.
2. execfile("myscript02_autocleanloop.py")
3. execfile("myscript03_moments.py")

## Data
2011.0.00099.S: merger remnants CO(1-0) 12m

2016.2.00006.S: merger remnants CO(1-0) 7m+TP

...

## Versions
CASA Version 5.4.0-70

## Directory Structure
data/
  - mycasa_scripts_*/ - scripts_ju01_ssc/   # all scripts
  - myproj_*/ - proj_ju01_ssc/ - data_raw/  # all data required
