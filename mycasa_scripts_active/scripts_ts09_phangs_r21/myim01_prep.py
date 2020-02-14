import os
import scripts_phangs_r21 as r21

dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_raw/"


#####################
### Main Procedure
#####################
os.system("rm -rf " + dir_data.replace("_raw",""))
os.mkdir(dir_data.replace("_raw",""))

# ngc0628
common_beam = "4.0arcsec"
co10_fits = dir_data + "ngc0628_co10_3p5as_k.fits"
co21_fits = dir_data + "ngc0628_12m+7m+tp_co21_pbcorr_round_k.fits"
co10_output = dir_data.replace("_raw","") + "ngc0628_co10_pbcor_4p0.image"
co21_output = dir_data.replace("_raw","") + "ngc0628_co21_pbcor_4p0.image"
r21.stage_cubes(common_beam,co10_fits,co21_fits,co10_output,co21_output)

# ngc3627
common_beam = "8.0arcsec"
co10_fits = dir_data + "ngc3627_co10_8as_k.fits"
co21_fits = dir_data + "ngc3627_12m+7m+tp_co21_pbcorr_round_k.fits"
co10_output = dir_data.replace("_raw","") + "ngc3627_co10_pbcor_8p0.image"
co21_output = dir_data.replace("_raw","") + "ngc3627_co21_pbcor_8p0.image"
r21.stage_cubes(common_beam,co10_fits,co21_fits,co10_output,co21_output)

# ngc4254
common_beam = "8.0arcsec"
co10_fits = dir_data + "ngc4254_co10_8as_k.fits"
co21_fits = dir_data + "ngc4254_12m+7m+tp_co21_pbcorr_round_k.fits"
co10_output = dir_data.replace("_raw","") + "ngc4254_co10_pbcor_8p0.image"
co21_output = dir_data.replace("_raw","") + "ngc4254_co21_pbcor_8p0.image"
r21.stage_cubes(common_beam,co10_fits,co21_fits,co10_output,co21_output)

# ngc0628
common_beam = "4.0arcsec"
co10_fits = dir_data + "ngc4321_co10_4as_k.fits"
co21_fits = dir_data + "ngc4321_12m+7m+tp_co21_pbcorr_round_k.fits"
co10_output = dir_data.replace("_raw","") + "ngc4321_co10_pbcor_4p0.image"
co21_output = dir_data.replace("_raw","") + "ngc4321_co21_pbcor_4p0.image"
r21.stage_cubes(common_beam,co10_fits,co21_fits,co10_output,co21_output)

os.system("rm -rf *.last")
