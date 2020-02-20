dir_data="/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"


### figure 1
convert -crop 700x570+75+20 $dir_data"ngc4321_12co10_m0.png" $dir_data"ngc4321_12co10_m0b.png"
convert -crop 700x570+75+20 $dir_data"ngc4321_12co21_m0.png" $dir_data"ngc4321_12co21_m0b.png"
convert -crop 700x570+21+20 $dir_data"ngc4321_r21.png" $dir_data"ngc4321_r21b.png"
convert -crop 700x570+21+20 $dir_data"ngc4321_r21_m8.png" $dir_data"ngc4321_r21_m8b.png"

convert +append -border 0x0 $dir_data"ngc4321_12co10_m0b.png" $dir_data"ngc4321_12co21_m0b.png" $dir_data"fig01a.png"
convert +append -border 0x0 $dir_data"ngc4321_r21b.png" $dir_data"ngc4321_r21_m8b.png" $dir_data"fig01b.png"

convert -append -border 0x0 $dir_data"fig01a.png" $dir_data"fig01b.png" eps2:$dir_data"f01.eps"

rm -rf $dir_data"ngc4321_12co10_m0.png" $dir_data"ngc4321_12co10_m0b.png"
rm -rf $dir_data"ngc4321_12co21_m0.png" $dir_data"ngc4321_12co21_m0b.png"
rm -rf $dir_data"ngc4321_r21.png" $dir_data"ngc4321_r21b.png"
rm -rf $dir_data"ngc4321_r21_m8.png" $dir_data"ngc4321_r21_m8b.png"
rm -rf $dir_data"fig01a.png" $dir_data"fig01b.png"


### figure 2
convert +append -border 0x0 $dir_data"missingflux_co10.png" $dir_data"missingflux_co21.png" $dir_data"missingflux_r21.png" eps2:$dir_data"f02.eps"

rm -rf $dir_data"missingflux_co10.png" $dir_data"missingflux_co21.png" $dir_data"missingflux_r21.png"


### figure 3
convert -append -border 0x0 $dir_data"ngc4321_scatter_co10_co21.png" $dir_data"ngc4321_scatter_co21_r21.png" eps2:$dir_data"f03.eps"

rm -rf $dir_data"ngc4321_scatter_co10_co21.png" $dir_data"ngc4321_scatter_co21_r21.png"


### figure 4
convert -crop 1110x205+170+30 $dir_data"figure_hists_ngc0628.png" $dir_data"figure_hists_ngc0628b.png"
convert -crop 1110x185+170+50 $dir_data"figure_hists_ngc3627.png" $dir_data"figure_hists_ngc3627b.png"
convert -crop 1110x215+170+50 $dir_data"figure_hists_ngc4321.png" $dir_data"figure_hists_ngc4321b.png"

convert -append -border 0x0 $dir_data"figure_hists_ngc0628b.png" $dir_data"figure_hists_ngc3627b.png" $dir_data"figure_hists_ngc4321b.png" eps2:$dir_data"f04.eps"

rm -rf $dir_data"figure_hists_ngc0628.png" $dir_data"figure_hists_ngc0628b.png"
rm -rf 1110x185+170+50 $dir_data"figure_hists_ngc3627.png" $dir_data"figure_hists_ngc3627b.png"
rm -rf 1110x215+170+50 $dir_data"figure_hists_ngc4321.png" $dir_data"figure_hists_ngc4321b.png"


### figure 5


### figure 6
convert -crop 580x570+75+20 $dir_data"ngc0628_r21_mask.png" $dir_data"ngc0628_r21_maskb.png"
convert -crop 580x570+75+20 $dir_data"ngc3627_r21_mask.png" $dir_data"ngc3627_r21_maskb.png"
convert -crop 580x570+75+20 $dir_data"ngc4254_r21_mask.png" $dir_data"ngc4254_r21_maskb.png"
convert -crop 600x570+75+20 $dir_data"ngc4321_r21_mask.png" $dir_data"ngc4321_r21_maskb.png"

convert +append -border 0x0 $dir_data"ngc0628_r21_maskb.png" $dir_data"ngc3627_r21_maskb.png" $dir_data"ngc4254_r21_maskb.png" $dir_data"ngc4321_r21_maskb.png" eps2:$dir_data"f06.eps"

rm -rf $dir_data"ngc0628_r21_mask.png" $dir_data"ngc0628_r21_maskb.png"
rm -rf 580x570+75+20 $dir_data"ngc3627_r21_mask.png" $dir_data"ngc3627_r21_maskb.png"
rm -rf 580x570+75+20 $dir_data"ngc4254_r21_mask.png" $dir_data"ngc4254_r21_maskb.png"
rm -rf 600x570+75+20 $dir_data"ngc4321_r21_mask.png" $dir_data"ngc4321_r21_maskb.png"


### figure 7
### figure 8

