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
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4321_flux_4p0_4p0_no.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_flux_8p0_8p0_no.png eps2:/Users/saito/data/phangs/co_ratio/eps/f02.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4321_flux_4p0_4p0_no.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_flux_8p0_8p0_no.png

### figure 3
convert -crop 1190x245+250+50 /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc0628b.png
convert -crop 1190x245+250+50 /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc3627b.png
convert -crop 1190x245+250+50 /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc4254b.png
convert -crop 1190x295+250+50 /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc4321b.png
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc0628b.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc3627b.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc4254b.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc4321b.png eps2:/Users/saito/data/phangs/co_ratio/eps/f03.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc4321.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc0628b.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc3627b.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc4254b.png /Users/saito/data/phangs/co_ratio/eps/f03_hists_ngc4321b.png

### figure 4
convert -crop 1460x245+170+50 /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc0628b.png
convert -crop 1460x235+170+60 /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc3627b.png
convert -crop 1460x235+170+60 /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc4254b.png
convert -crop 1460x285+170+60 /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc4321b.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc0628b.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc3627b.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc4254b.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc4321b.png eps2:/Users/saito/data/phangs/co_ratio/eps/f04.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc4321.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc0628b.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc3627b.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc4254b.png /Users/saito/data/phangs/co_ratio/eps/f04_hists_ngc4321b.png

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

# figure 6
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/f06a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4254_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/f06b.png
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f06a.png /Users/saito/data/phangs/co_ratio/eps/f06b.png eps2:/Users/saito/data/phangs/co_ratio/eps/f06.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_scatter_co10_co21.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4254_scatter_co10_co21.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_scatter_co10_co21.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f06a.png /Users/saito/data/phangs/co_ratio/eps/f06b.png

# figure 7
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/f07a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4254_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/f07b.png
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f07a.png /Users/saito/data/phangs/co_ratio/eps/f07b.png eps2:/Users/saito/data/phangs/co_ratio/eps/f07.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_scatter_co21_r21.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4254_scatter_co21_r21.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_scatter_co21_r21.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f07a.png /Users/saito/data/phangs/co_ratio/eps/f07b.png

# figure 8 ???x1510+???+170
convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1a.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1b.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1c.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1d.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1db.png

convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2a.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2b.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2c.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2d.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2db.png

convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3a.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3b.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3c.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3d.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3db.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1ab.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1bb.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1cb.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1db.png /Users/saito/data/phangs/co_ratio/eps/f08a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2ab.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2bb.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2cb.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2db.png /Users/saito/data/phangs/co_ratio/eps/f08b.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3ab.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3bb.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3cb.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3db.png /Users/saito/data/phangs/co_ratio/eps/f08c.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f08a.png /Users/saito/data/phangs/co_ratio/eps/f08b.png /Users/saito/data/phangs/co_ratio/eps/f08c.png eps2:/Users/saito/data/phangs/co_ratio/eps/f08_ngc4321.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1a*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1b*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1c*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot1d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2a*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2b*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2c*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot2d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3a*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3b*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3c*.png /Users/saito/data/phangs/co_ratio/eps/ngc4321_mplot3d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f08a.png /Users/saito/data/phangs/co_ratio/eps/f08b.png /Users/saito/data/phangs/co_ratio/eps/f08c.png

# figure 8 ???x1510+???+170: ngc0628
convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1a.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1b.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1c.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1d.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1db.png

convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2a.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2b.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2c.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2d.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2db.png

convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3a.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3b.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3c.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3d.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3db.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1ab.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1bb.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1cb.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1db.png /Users/saito/data/phangs/co_ratio/eps/f08a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2ab.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2bb.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2cb.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2db.png /Users/saito/data/phangs/co_ratio/eps/f08b.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3ab.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3bb.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3cb.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3db.png /Users/saito/data/phangs/co_ratio/eps/f08c.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f08a.png /Users/saito/data/phangs/co_ratio/eps/f08b.png /Users/saito/data/phangs/co_ratio/eps/f08c.png eps2:/Users/saito/data/phangs/co_ratio/eps/f08_ngc0628.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1a*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1b*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1c*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot1d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2a*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2b*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2c*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot2d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3a*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3b*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3c*.png /Users/saito/data/phangs/co_ratio/eps/ngc0628_mplot3d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f08a.png /Users/saito/data/phangs/co_ratio/eps/f08b.png /Users/saito/data/phangs/co_ratio/eps/f08c.png

# figure 8 ???x1510+???+170: ngc3627
convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1a.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1b.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1c.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1d.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1db.png

convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2a.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2b.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2c.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2d.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2db.png

convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3a.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3b.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3c.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3d.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3db.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1ab.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1bb.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1cb.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1db.png /Users/saito/data/phangs/co_ratio/eps/f08a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2ab.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2bb.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2cb.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2db.png /Users/saito/data/phangs/co_ratio/eps/f08b.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3ab.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3bb.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3cb.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3db.png /Users/saito/data/phangs/co_ratio/eps/f08c.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f08a.png /Users/saito/data/phangs/co_ratio/eps/f08b.png /Users/saito/data/phangs/co_ratio/eps/f08c.png eps2:/Users/saito/data/phangs/co_ratio/eps/f08_ngc3627.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1a*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1b*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1c*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot1d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2a*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2b*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2c*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot2d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3a*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3b*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3c*.png /Users/saito/data/phangs/co_ratio/eps/ngc3627_mplot3d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f08a.png /Users/saito/data/phangs/co_ratio/eps/f08b.png /Users/saito/data/phangs/co_ratio/eps/f08c.png

# figure 8 ???x1510+???+170: ngc4254
convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1a.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1b.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1c.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1d.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1db.png

convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2a.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2b.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2c.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2d.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2db.png

convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3a.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3b.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3c.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3d.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3db.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1ab.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1bb.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1cb.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1db.png /Users/saito/data/phangs/co_ratio/eps/f08a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2ab.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2bb.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2cb.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2db.png /Users/saito/data/phangs/co_ratio/eps/f08b.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3ab.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3bb.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3cb.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3db.png /Users/saito/data/phangs/co_ratio/eps/f08c.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f08a.png /Users/saito/data/phangs/co_ratio/eps/f08b.png /Users/saito/data/phangs/co_ratio/eps/f08c.png eps2:/Users/saito/data/phangs/co_ratio/eps/f08_ngc4254.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1a*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1b*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1c*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot1d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2a*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2b*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2c*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot2d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3a*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3b*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3c*.png /Users/saito/data/phangs/co_ratio/eps/ngc4254_mplot3d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f08a.png /Users/saito/data/phangs/co_ratio/eps/f08b.png /Users/saito/data/phangs/co_ratio/eps/f08c.png


# figure 9 ???x1510+???+170
convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1a.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1b.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1c.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1d.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1db.png

convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2a.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2b.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2c.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2d.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2db.png

convert -crop 1420x1510+0+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3a.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3ab.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3b.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3bb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3c.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3cb.png
convert -crop 1210x1510+210+170 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3d.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3db.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1ab.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1bb.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1cb.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1db.png /Users/saito/data/phangs/co_ratio/eps/f09a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2ab.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2bb.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2cb.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2db.png /Users/saito/data/phangs/co_ratio/eps/f09b.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3ab.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3bb.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3cb.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3db.png /Users/saito/data/phangs/co_ratio/eps/f09c.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f09a.png /Users/saito/data/phangs/co_ratio/eps/f09b.png /Users/saito/data/phangs/co_ratio/eps/f09c.png eps2:/Users/saito/data/phangs/co_ratio/eps/f09.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1a*.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1b*.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1c*.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot1d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2a*.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2b*.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2c*.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot2d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3a*.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3b*.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3c*.png /Users/saito/data/phangs/co_ratio/eps/fig09_allmplot3d*.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f09a.png /Users/saito/data/phangs/co_ratio/eps/f09b.png /Users/saito/data/phangs/co_ratio/eps/f09c.png
