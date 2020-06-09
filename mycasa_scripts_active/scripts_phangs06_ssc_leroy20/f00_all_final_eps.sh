dir_data="/Users/saito/data/myproj_active/proj_phangs06_ssc/eps/"


### figure 0
convert +append -border 0x0 $dir_data"ngc0628_skymodel.png" $dir_data"ngc0628_7m.png" $dir_data"fig_ssc_01a.png"
convert +append -border 0x0 $dir_data"ngc0628_tp2vis.png" $dir_data"ngc0628_tpmodel.png" $dir_data"ngc0628_feather.png" $dir_data"fig_ssc_01b.png"
convert -append -border 0x0 $dir_data"fig_ssc_01a.png" $dir_data"fig_ssc_01b.png" eps2:$dir_data"ssc_image_ngc0628.eps"

rm -rf $dir_data"ngc0628_skymodel.png" $dir_data"ngc0628_7m.png" $dir_data"fig_ssc_01a.png"
rm -rf $dir_data"ngc0628_tp2vis.png" $dir_data"ngc0628_tpmodel.png" $dir_data"ngc0628_feather.png" $dir_data"fig_ssc_01b.png"

### figure 0
convert dir_data"fig_fidelity_vs_circ_diameter.png" eps2:$dir_data"ssc_fidelity_vs_size.eps"

convert dir_data"ssc_fidelity_vs_size.png" eps2:dir_data"ssc_fidelity_vs_size.eps"