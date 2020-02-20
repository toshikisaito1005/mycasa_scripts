dir_data="/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"

### figure 1
convert -crop 700x570+75+20 $dir_data"ngc4321_12co10_m0.png" $dir_data"ngc4321_12co10_m0b.png"
convert -crop 700x570+75+20 $dir_data"ngc4321_12co21_m0.png" $dir_data"ngc4321_12co21_m0b.png"
convert -crop 700x570+21+20 $dir_data"ngc4321_r21.png" $dir_data"ngc4321_r21b.png"
convert -crop 700x570+21+20 $dir_data"ngc4321_r21_m8.png" $dir_data"ngc4321_r21_m8b.png"

convert +append -border 0x0 $dir_data"ngc4321_12co10_m0b.png" $dir_data"ngc4321_12co21_m0b.png" $dir_data"fig01a.png"
convert +append -border 0x0 $dir_data"ngc4321_r21b.png" $dir_data"ngc4321_r21_m8b.png" $dir_data"fig01b.png"

convert -append -border 0x0 $dir_data"fig01a.png" $dir_data"fig01b.png" eps2:$dir_data"f01.eps"

rm -rf /Users/saito/data/phangs/co_ratio/eps/fig01a.png /Users/saito/data/phangs/co_ratio/eps/fig01b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4321_12co10_m0*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_12co21_m0*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4321_r21*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_r21_m8*.png

