dir_data="/Users/saito/data/myproj_active/proj_phangs06_ssc/eps/"


### figure
convert +append -border 0x0 $dir_data"ngc0628_skymodel.png" $dir_data"ngc0628_7m.png" $dir_data"fig_ssc_01a.png"
convert +append -border 0x0 $dir_data"ngc0628_tp2vis.png" $dir_data"ngc0628_tpmodel.png" $dir_data"ngc0628_feather.png" $dir_data"fig_ssc_01b.png"
convert -append -border 0x0 $dir_data"fig_ssc_01a.png" $dir_data"fig_ssc_01b.png" $dir_data"ssc_image_ngc0628.png"

convert +append -border 0x0 $dir_data"ngc4303_skymodel.png" $dir_data"ngc4303_7m.png" $dir_data"fig_ssc_01a.png"
convert +append -border 0x0 $dir_data"ngc4303_tp2vis.png" $dir_data"ngc4303_tpmodel.png" $dir_data"ngc4303_feather.png" $dir_data"fig_ssc_01b.png"
convert -append -border 0x0 $dir_data"fig_ssc_01a.png" $dir_data"fig_ssc_01b.png" $dir_data"ssc_image_ngc4303.png"

rm -rf $dir_data"ngc0628_skymodel.png" $dir_data"ngc0628_7m.png" $dir_data"fig_ssc_01a.png"
rm -rf $dir_data"ngc0628_tp2vis.png" $dir_data"ngc0628_tpmodel.png" $dir_data"ngc0628_feather.png" $dir_data"fig_ssc_01b.png"
rm -rf $dir_data"ngc1097_skymodel.png" $dir_data"ngc1097_7m.png" $dir_data"fig_ssc_01a.png"
rm -rf $dir_data"ngc1097_tp2vis.png" $dir_data"ngc1097_tpmodel.png" $dir_data"ngc1097_feather.png" $dir_data"fig_ssc_01b.png"
rm -rf $dir_data"ngc4303_skymodel.png" $dir_data"ngc4303_7m.png" $dir_data"fig_ssc_01a.png"
rm -rf $dir_data"ngc4303_tp2vis.png" $dir_data"ngc4303_tpmodel.png" $dir_data"ngc4303_feather.png" $dir_data"fig_ssc_01b.png"

### figure
convert $dir_data"fig_fidelity_vs_circ_diameter.png" eps2:$dir_data"ssc_fidelity_vs_size.eps"

### figure
convert -crop 0x345+0+0 $dir_data"ssc_fidelity_vs_size.png" $dir_data"ssc_fidelity_vs_sizeb.png"
convert -crop 0x345+0+0 $dir_data"ssc_diff_total_vs_size.png" $dir_data"ssc_diff_total_vs_sizeb.png"

convert -append -border 0x0 $dir_data"ssc_fidelity_vs_sizeb.png" $dir_data"ssc_diff_total_vs_sizeb.png" $dir_data"ssc_diff_vs_size.png" eps2:$dir_data"ssc_results.eps"

rm -rf $dir_data"ssc_fidelity_vs_size.png" $dir_data"ssc_fidelity_vs_sizeb.png" $dir_data"ssc_diff_total_vs_size.png" $dir_data"ssc_diff_total_vs_sizeb.png" $dir_data"ssc_diff_vs_size.png"
