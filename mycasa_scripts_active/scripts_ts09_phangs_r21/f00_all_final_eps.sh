dir_data="/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"


### figure 0
convert +append -border 0x0 $dir_data"noise_ngc0628_co10.png" $dir_data"noise_vs_beam.png" eps2:$dir_data"fig00.eps"

rm -rf $dir_data"noise_ngc0628_co10.png" $dir_data"noise_vs_beam.png"


### figure 1
convert +append -border 0x0 $dir_data"missingflux_co10.png" $dir_data"missingflux_co21.png" eps2:$dir_data"fig01.eps"

rm -rf $dir_data"missingflux_co10.png" $dir_data"missingflux_co21.png"

#convert +append -border 0x0 $dir_data"missingflux_co10.png" $dir_data"missingflux_co21.png" $dir_data"missingflux_r21.png" eps2:$dir_data"fig01.eps"
#rm -rf $dir_data"missingflux_co10.png" $dir_data"missingflux_co21.png" $dir_data"missingflux_r21.png"


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


### figure 4
convert -crop 1110x205+170+30 $dir_data"figure_hists_ngc0628.png" $dir_data"figure_hists_ngc0628b.png"
convert -crop 1110x185+170+50 $dir_data"figure_hists_ngc3627.png" $dir_data"figure_hists_ngc3627b.png"
convert -crop 1110x215+170+50 $dir_data"figure_hists_ngc4321.png" $dir_data"figure_hists_ngc4321b.png"

convert -append -border 0x0 $dir_data"figure_hists_ngc0628b.png" $dir_data"figure_hists_ngc3627b.png" $dir_data"figure_hists_ngc4321b.png" eps2:$dir_data"fig04.eps"

rm -rf $dir_data"figure_hists_ngc0628.png" $dir_data"figure_hists_ngc0628b.png"
rm -rf 1110x185+170+50 $dir_data"figure_hists_ngc3627.png" $dir_data"figure_hists_ngc3627b.png"
rm -rf 1110x215+170+50 $dir_data"figure_hists_ngc4321.png" $dir_data"figure_hists_ngc4321b.png"


### figure 5
convert -crop 5750x0+0+00 $dir_data"stats_histo_600pc.png" eps2:$dir_data"fig05.eps"

rm -rf $dir_data"stats_histo_600pc.png"


### figure 6
convert -crop 5750x0+0+00 $dir_data"histoall.png" eps2:$dir_data"fig06.eps"

rm -rf $dir_data"histoall.png"


### figure 7
convert +append -border 0x0 $dir_data"ngc0628_co10_vs_co21.png" $dir_data"ngc3627_co10_vs_co21.png" $dir_data"fig07a.png"
convert -append -border 0x0 $dir_data"fig07a.png" $dir_data"ngc4321_co10_vs_co21.png" eps2:$dir_data"fig07.eps"

rm -rf $dir_data"ngc0628_co10_vs_co21.png" $dir_data"ngc3627_co10_vs_co21.png" $dir_data"fig07a.png"
rm -rf $dir_data"ngc4321_co10_vs_co21.png"


### figure 8
convert +append -border 0x0 $dir_data"ngc0628_co21_vs_r21.png" $dir_data"ngc3627_co21_vs_r21.png" $dir_data"fig08a.png"
convert -append -border 0x0 $dir_data"fig08a.png" $dir_data"ngc4321_co21_vs_r21.png" eps2:$dir_data"fig08.eps"

rm -rf $dir_data"ngc0628_co21_vs_r21.png" $dir_data"ngc3627_co21_vs_r21.png" $dir_data"fig08a.png"
rm -rf $dir_data"ngc4321_co21_vs_r21.png"


### figure 9
convert $dir_data"violin_co21.png" eps2:$dir_data"fig09.eps"

rm -rf $dir_data"violin_co21.png"


### figure 10
convert -crop 600x600+80+30 $dir_data"ngc0628_r21_mask.png" $dir_data"ngc0628_r21_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc3627_r21_mask.png" $dir_data"ngc3627_r21_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc4321_r21_mask.png" $dir_data"ngc4321_r21_maskb.png"

convert +append -border 0x0 $dir_data"ngc0628_r21_maskb.png" $dir_data"ngc3627_r21_maskb.png" $dir_data"fig10a.png"
convert -append -border 0x0 $dir_data"ngc4321_r21_maskb.png" $dir_data"fig_mask_histo.png" $dir_data"fig10b.png"
convert -append -border 0x0 $dir_data"fig10a.png"  eps2:$dir_data"fig10.eps"

rm -rf $dir_data"ngc0628_r21_mask.png" $dir_data"ngc0628_r21_maskb.png"
rm -rf $dir_data"ngc3627_r21_mask.png" $dir_data"ngc3627_r21_maskb.png"
rm -rf $dir_data"ngc4321_r21_mask.png" $dir_data"ngc4321_r21_maskb.png"
rm -rf $dir_data"fig10a.png"

