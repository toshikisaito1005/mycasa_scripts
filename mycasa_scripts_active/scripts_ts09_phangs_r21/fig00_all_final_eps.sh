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
convert -crop 790x365+35+0 $dir_data"ngc0628_violin_num.png" $dir_data"ngc0628_violin_numb.png"
convert -crop 720x365+105+0 $dir_data"ngc0628_violin_co10.png" $dir_data"ngc0628_violin_co10b.png"
convert -crop 720x365+105+0 $dir_data"ngc0628_violin_co21.png" $dir_data"ngc0628_violin_co21b.png"
convert -crop 790x338+35+28 $dir_data"ngc3627_violin_num.png" $dir_data"ngc3627_violin_numb.png"
convert -crop 720x338+105+28 $dir_data"ngc3627_violin_co10.png" $dir_data"ngc3627_violin_co10b.png"
convert -crop 720x338+105+28 $dir_data"ngc3627_violin_co21.png" $dir_data"ngc3627_violin_co21b.png"
convert -crop 790x438+35+28 $dir_data"ngc4321_violin_num.png" $dir_data"ngc4321_violin_numb.png"
convert -crop 720x438+105+28 $dir_data"ngc4321_violin_co10.png" $dir_data"ngc4321_violin_co10b.png"
convert -crop 720x438+105+28 $dir_data"ngc4321_violin_co21.png" $dir_data"ngc4321_violin_co21b.png"

convert +append -border 0x0 $dir_data"ngc0628_violin_numb.png" $dir_data"ngc0628_violin_co10b.png" $dir_data"ngc0628_violin_co21b.png" $dir_data"f04a.png"
convert +append -border 0x0 $dir_data"ngc3627_violin_numb.png" $dir_data"ngc3627_violin_co10b.png" $dir_data"ngc3627_violin_co21b.png" $dir_data"f04b.png"
convert +append -border 0x0 $dir_data"ngc4321_violin_numb.png" $dir_data"ngc4321_violin_co10b.png" $dir_data"ngc4321_violin_co21b.png" $dir_data"f04d.png"

convert -append -border 0x0 $dir_data"f04a.png" $dir_data"f04b.png" $dir_data"f04c.png" $dir_data"f04d.png" eps2:$dir_data"f05.eps"

rm -rf $dir_data"ngc0628_violin_num.png" $dir_data"ngc0628_violin_numb.png"
rm -rf $dir_data"ngc0628_violin_co10.png" $dir_data"ngc0628_violin_co10b.png"
rm -rf $dir_data"ngc0628_violin_co21.png" $dir_data"ngc0628_violin_co21b.png"
rm -rf $dir_data"ngc3627_violin_num.png" $dir_data"ngc3627_violin_numb.png"
rm -rf $dir_data"ngc3627_violin_co10.png" $dir_data"ngc3627_violin_co10b.png"
rm -rf $dir_data"ngc3627_violin_co21.png" $dir_data"ngc3627_violin_co21b.png"
rm -rf $dir_data"ngc4321_violin_num.png" $dir_data"ngc4321_violin_numb.png"
rm -rf $dir_data"ngc4321_violin_co10.png" $dir_data"ngc4321_violin_co10b.png"
rm -rf $dir_data"ngc4321_violin_co21.png" $dir_data"ngc4321_violin_co21b.png"
rm -rf $dir_data"f04a.png" $dir_data"f04b.png" $dir_data"f04c.png" $dir_data"f04d.png"


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
convert -crop 1700x1300+70+100 $dir_data"radial_norm_r21.png" $dir_data"radial_norm_r21b.png"
convert -crop 1700x1300+70+100 $dir_data"radial_r21.png" $dir_data"radial_r21b.png"

convert +append -border 0x0 $dir_data"radial_r21b.png" $dir_data"radial_norm_r21b.png" eps2:$dir_data"f07.eps"

rm -rf $dir_data"radial_norm_r21.png" $dir_data"radial_norm_r21b.png"
rm -rf $dir_data"radial_r21.png" $dir_data"radial_r21b.png"

### figure 8

