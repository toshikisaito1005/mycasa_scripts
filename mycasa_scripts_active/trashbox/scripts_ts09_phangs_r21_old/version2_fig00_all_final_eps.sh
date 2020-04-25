### figure 1
convert -crop 700x570+75+20 /Users/saito/data/phangs/co_ratio/eps/ngc4321_12co10_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_12co10_m0b.png
convert -crop 700x570+75+20 /Users/saito/data/phangs/co_ratio/eps/ngc4321_12co21_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_12co21_m0b.png
convert -crop 700x570+21+20 /Users/saito/data/phangs/co_ratio/eps/ngc4321_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_r21b.png
convert -crop 700x570+21+20 /Users/saito/data/phangs/co_ratio/eps/ngc4321_r21_m8.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_r21_m8b.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4321_12co10_m0b.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_12co21_m0b.png /Users/saito/data/phangs/co_ratio/eps/fig01a.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4321_r21b.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_r21_m8b.png /Users/saito/data/phangs/co_ratio/eps/fig01b.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig01a.png /Users/saito/data/phangs/co_ratio/eps/fig01b.png eps2:/Users/saito/data/phangs/co_ratio/eps/f01.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/fig01a.png /Users/saito/data/phangs/co_ratio/eps/fig01b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4321_12co10_m0*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_12co21_m0*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4321_r21*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_r21_m8*.png


### figure 2
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/missingflux_co10.png /Users/saito/data/phangs/co_ratio/eps/missingflux_co21.png /Users/saito/data/phangs/co_ratio/eps/missingflux_r21.png eps2:/Users/saito/data/phangs/co_ratio/eps/f02.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/missingflux_co10.png /Users/saito/data/phangs/co_ratio/eps/missingflux_co21.png /Users/saito/data/phangs/co_ratio/eps/missingflux_r21.png


### figure 3
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4321_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_scatter_co21_r21.png eps2:/Users/saito/data/phangs/co_ratio/eps/f03.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4321_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_scatter_co21_r21.png

### figure 4 # 1110 => 1460 for WISE
convert -crop 1110x195+170+30 /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc0628_wise.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc0628b.png
convert -crop 1110x195+170+30 /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc3627_wise.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc3627b.png
convert -crop 1110x195+170+30 /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc4254_wise.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc4254b.png
convert -crop 1110x240+170+30 /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc4321_wise.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc4321b.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc0628b.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc3627b.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc4254b.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc4321b.png eps2:/Users/saito/data/phangs/co_ratio/eps/f04.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc0628_wise.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc3627_wise.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc4254_wise.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc4321_wise.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc0628b.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc3627b.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc4254b.png /Users/saito/data/phangs/co_ratio/eps/figure_hists_ngc4321b.png


### figure 5
convert -crop 790x365+35+0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_num.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_numb.png
convert -crop 720x365+105+0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_co10.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_co10b.png
convert -crop 720x365+105+0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_co21b.png
convert -crop 790x338+35+28 /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_num.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_numb.png
convert -crop 720x338+105+28 /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_co10.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_co10b.png
convert -crop 720x338+105+28 /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_co21b.png
convert -crop 790x338+35+28 /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_num.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_numb.png
convert -crop 720x338+105+28 /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_co10.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_co10b.png
convert -crop 720x338+105+28 /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_co21b.png
convert -crop 790x438+35+28 /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_num.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_numb.png
convert -crop 720x438+105+28 /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_co10.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_co10b.png
convert -crop 720x438+105+28 /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_co21b.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_numb.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_co10b.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_co21b.png /Users/saito/data/phangs/co_ratio/eps/f04a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_numb.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_co10b.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_co21b.png /Users/saito/data/phangs/co_ratio/eps/f04b.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_numb.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_co10b.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_co21b.png /Users/saito/data/phangs/co_ratio/eps/f04c.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_numb.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_co10b.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_co21b.png /Users/saito/data/phangs/co_ratio/eps/f04d.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f04a.png /Users/saito/data/phangs/co_ratio/eps/f04b.png /Users/saito/data/phangs/co_ratio/eps/f04c.png /Users/saito/data/phangs/co_ratio/eps/f04d.png eps2:/Users/saito/data/phangs/co_ratio/eps/f05.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_num*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_co10*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_violin_co21*.png /Users/saito/data/phangs/co_ratio/eps/f04a.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_num*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_co10*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_violin_co21*.png /Users/saito/data/phangs/co_ratio/eps/f04b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_num*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_co10*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_violin_co21*.png /Users/saito/data/phangs/co_ratio/eps/f04c.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_num*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_co10*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_violin_co21*.png /Users/saito/data/phangs/co_ratio/eps/f04d.png


### figure 6
convert -crop 1610x890+25+195 /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc0628b.png
convert -crop 1550x890+85+195 /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc3627b.png
convert -crop 1550x890+85+195 /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc4254b.png
convert -crop 1550x890+85+195 /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc4321b.png
convert -crop 1610x890+25+195 /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc0628b.png
convert -crop 1550x890+85+195 /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc3627b.png
convert -crop 1550x890+85+195 /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc4254b.png
convert -crop 1550x890+85+195 /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc4321b.png

convert -crop 1610x1500+25+195 /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc0628b.png
convert -crop 1550x1500+85+195 /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc3627b.png
convert -crop 1550x1500+85+195 /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc4254b.png
convert -crop 1550x1500+85+195 /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc4321b.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc0628b.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc3627b.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc4254b.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc4321b.png /Users/saito/data/phangs/co_ratio/eps/f06a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc0628b.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc3627b.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc4254b.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc4321b.png /Users/saito/data/phangs/co_ratio/eps/f06b.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc0628b.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc3627b.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc4254b.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc4321b.png /Users/saito/data/phangs/co_ratio/eps/f06c.png
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f06a.png /Users/saito/data/phangs/co_ratio/eps/f06b.png /Users/saito/data/phangs/co_ratio/eps/f06c.png eps2:/Users/saito/data/phangs/co_ratio/eps/f06.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc0628b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc3627b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc4254b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/radial_co10_ngc4321b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc0628b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc3627b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc4254b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/radial_co21_ngc4321b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc0628b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc3627b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc4254b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/radial_r21_ngc4321b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f06a.png /Users/saito/data/phangs/co_ratio/eps/f06b.png /Users/saito/data/phangs/co_ratio/eps/f06c.png


### figure 7
convert -crop 1700x1270+70+140 /Users/saito/data/phangs/co_ratio/eps/radial_norm_r21.png eps2:/Users/saito/data/phangs/co_ratio/eps/f07.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/radial_norm_r21.png


### appendix 1
convert -crop 580x570+75+20 /Users/saito/data/phangs/co_ratio/eps/ngc0628_12co10_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_12co10_m0b.png
convert -crop 580x570+75+20 /Users/saito/data/phangs/co_ratio/eps/ngc0628_12co21_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_12co21_m0b.png
convert -crop 700x570+21+20 /Users/saito/data/phangs/co_ratio/eps/ngc0628_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_r21b.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_12co10_m0b.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_12co21_m0b.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_r21b.png /Users/saito/data/phangs/co_ratio/eps/appendix01a.png

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_12co10_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_12co10_m0b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_12co21_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_12co21_m0b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_r21b.png

convert -crop 580x570+75+20 /Users/saito/data/phangs/co_ratio/eps/ngc3627_12co10_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_12co10_m0b.png
convert -crop 580x570+75+20 /Users/saito/data/phangs/co_ratio/eps/ngc3627_12co21_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_12co21_m0b.png
convert -crop 700x570+21+20 /Users/saito/data/phangs/co_ratio/eps/ngc3627_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_r21b.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc3627_12co10_m0b.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_12co21_m0b.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_r21b.png /Users/saito/data/phangs/co_ratio/eps/appendix01b.png

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc3627_12co10_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_12co10_m0b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc3627_12co21_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_12co21_m0b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc3627_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_r21b.png

convert -crop 580x570+75+20 /Users/saito/data/phangs/co_ratio/eps/ngc4254_12co10_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_12co10_m0b.png
convert -crop 580x570+75+20 /Users/saito/data/phangs/co_ratio/eps/ngc4254_12co21_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_12co21_m0b.png
convert -crop 700x570+21+20 /Users/saito/data/phangs/co_ratio/eps/ngc4254_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_r21b.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4254_12co10_m0b.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_12co21_m0b.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_r21b.png /Users/saito/data/phangs/co_ratio/eps/appendix01c.png

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4254_12co10_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_12co10_m0b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4254_12co21_m0.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_12co21_m0b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4254_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_r21b.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/appendix01a.png /Users/saito/data/phangs/co_ratio/eps/appendix01b.png /Users/saito/data/phangs/co_ratio/eps/appendix01c.png eps2:/Users/saito/data/phangs/co_ratio/eps/appendix01.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/appendix01a.png /Users/saito/data/phangs/co_ratio/eps/appendix01b.png /Users/saito/data/phangs/co_ratio/eps/appendix01c.png

### appendix 2
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/appendix02a.png
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/appendix02a.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_scatter_co10_co21.png eps2:/Users/saito/data/phangs/co_ratio/eps/appendix02.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/appendix02a.png

### appendix 3
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/appendix03a.png
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/appendix03a.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_scatter_co21_r21.png eps2:/Users/saito/data/phangs/co_ratio/eps/appendix03.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/appendix03a.png

