dir_data="/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"


### figure 1
convert +append -border 0x0 $dir_data"missingflux_co10.png" $dir_data"missingflux_co21.png" $dir_data"missingflux_r21.png" eps2:$dir_data"fig01.eps"

rm -rf $dir_data"missingflux_co10.png" $dir_data"missingflux_co21.png" $dir_data"missingflux_r21.png"


### figure 2
convert -crop 600x570+75+20 $dir_data"ngc0628_12co10_m0.png" $dir_data"ngc0628_12co10_m0b.png"
convert -crop 600x570+75+20 $dir_data"ngc0628_12co21_m0.png" $dir_data"ngc0628_12co21_m0b.png"
convert -crop 700x570+21+20 $dir_data"ngc0628_r21.png" $dir_data"ngc0628_r21b.png"
convert -crop 600x570+75+20 $dir_data"ngc3627_12co10_m0.png" $dir_data"ngc3627_12co10_m0b.png"
convert -crop 600x570+75+20 $dir_data"ngc3627_12co21_m0.png" $dir_data"ngc3627_12co21_m0b.png"
convert -crop 700x570+21+20 $dir_data"ngc3627_r21.png" $dir_data"ngc3627_r21b.png"
convert -crop 600x570+75+20 $dir_data"ngc4321_12co10_m0.png" $dir_data"ngc4321_12co10_m0b.png"
convert -crop 600x570+75+20 $dir_data"ngc4321_12co21_m0.png" $dir_data"ngc4321_12co21_m0b.png"
convert -crop 700x570+21+20 $dir_data"ngc4321_r21.png" $dir_data"ngc4321_r21b.png"

convert +append -border 0x0 $dir_data"ngc0628_12co10_m0b.png" $dir_data"ngc0628_12co21_m0b.png" $dir_data"ngc0628_r21b.png" $dir_data"fig01a.png"
convert +append -border 0x0 $dir_data"ngc3627_12co10_m0b.png" $dir_data"ngc3627_12co21_m0b.png" $dir_data"ngc3627_r21b.png" $dir_data"fig01b.png"
convert +append -border 0x0 $dir_data"ngc4321_12co10_m0b.png" $dir_data"ngc4321_12co21_m0b.png" $dir_data"ngc4321_r21b.png" $dir_data"fig01c.png"

convert -append -border 0x0 $dir_data"fig01a.png" $dir_data"fig01b.png" $dir_data"fig01c.png" eps2:$dir_data"fig02.eps"

rm -rf $dir_data"ngc0628_12co10_m0.png" $dir_data"ngc0628_12co10_m0b.png"
rm -rf $dir_data"ngc0628_12co21_m0.png" $dir_data"ngc0628_12co21_m0b.png"
rm -rf $dir_data"ngc0628_r21.png" $dir_data"ngc0628_r21b.png"
rm -rf $dir_data"ngc3627_12co10_m0.png" $dir_data"ngc3627_12co10_m0b.png"
rm -rf $dir_data"ngc3627_12co21_m0.png" $dir_data"ngc3627_12co21_m0b.png"
rm -rf $dir_data"ngc3627_r21.png" $dir_data"ngc3627_r21b.png"
rm -rf $dir_data"ngc4321_12co10_m0.png" $dir_data"ngc4321_12co10_m0b.png"
rm -rf $dir_data"ngc4321_12co21_m0.png" $dir_data"ngc4321_12co21_m0b.png"
rm -rf $dir_data"ngc4321_r21.png" $dir_data"ngc4321_r21b.png"
rm -rf $dir_data"fig01a.png" $dir_data"fig01b.png" $dir_data"fig01c.png"


### figure 3
convert -crop 1500x0+0+100 $dir_data"figure_r21_vs_p21.png" eps2:$dir_data"fig03.eps"

rm -rf $dir_data"figure_r21_vs_p21.png"