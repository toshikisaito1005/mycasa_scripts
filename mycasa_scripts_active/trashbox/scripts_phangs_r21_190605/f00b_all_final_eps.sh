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
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f2_hists_wise_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/f2_hists_wise_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/f2_hists_wise_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/f2_hists_wise_ngc4254.png eps2:/Users/saito/data/phangs/co_ratio/eps/f02.eps
#convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f2_hists_co.png /Users/saito/data/phangs/co_ratio/eps/f2_hists_wise.png eps2:/Users/saito/data/phangs/co_ratio/eps/f02.eps

#rm -rf /Users/saito/data/phangs/co_ratio/eps/f2_hists_co.png /Users/saito/data/phangs/co_ratio/eps/f2_hists_wise.png


### figure 3
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig03a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/fig03b_n4321_m8_ap.png eps2:/Users/saito/data/phangs/co_ratio/eps/f03.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/fig03a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/fig03b_n4321_m8_ap.png


### figure 4
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig04a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/fig04b_n4321_m8_bm.png eps2:/Users/saito/data/phangs/co_ratio/eps/f04.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/fig04a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/fig04b_n4321_m8_bm.png


### figure 5
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig05a_n4321_r21_v_co21_ap.png /Users/saito/data/phangs/co_ratio/eps/fig05b_n4321_r21_v_co21_bm.png eps2:/Users/saito/data/phangs/co_ratio/eps/f05.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/fig05a_n4321_r21_v_co21_ap.png /Users/saito/data/phangs/co_ratio/eps/fig05b_n4321_r21_v_co21_bm.png

### figure 6
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/f06a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/f06b.png
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f06a.png /Users/saito/data/phangs/co_ratio/eps/f06b.png eps2:/Users/saito/data/phangs/co_ratio/eps/f06.eps
rm -rf /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median_ngc4321.png /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median_ngc0628.png /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median_ngc3627.png /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median_ngc4254.png /Users/saito/data/phangs/co_ratio/eps/f06a.png /Users/saito/data/phangs/co_ratio/eps/f06b.png

#convert /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median.png eps2:/Users/saito/data/phangs/co_ratio/eps/f06.eps
#rm -rf /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median.png

### figure 7
convert -crop 1650x610+120+50 /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot1.png /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot1b.png
convert -crop 1650x610+120+50 /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot2.png /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot2b.png
convert -crop 1650x610+120+50 /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot3.png /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot3b.png


convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot1b.png /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot2b.png /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot3b.png eps2:/Users/saito/data/phangs/co_ratio/eps/f07.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot1.png /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot2.png /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot3.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot1b.png /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot2b.png /Users/saito/data/phangs/co_ratio/eps/figure7_multiplot3b.png

### figure 8
convert -crop 1650x460+120+50 /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot1.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot1b.png
convert -crop 1650x460+120+50 /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot2.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot2b.png
convert -crop 1650x460+120+50 /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot3.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot3b.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot1b.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot2b.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot3b.png /Users/saito/data/phangs/co_ratio/eps/f08a.png

convert -crop 1400x1400+120+150 /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot4.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot4b.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f08a.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot4b.png eps2:/Users/saito/data/phangs/co_ratio/eps/f08.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot1.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot1b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot2.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot2b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot3.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot3b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot4.png /Users/saito/data/phangs/co_ratio/eps/figure8_multiplot4b.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f08a.png

#### aperture-weighted-average
### figure 3
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figw03a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/figw03b_n4321_m8_ap.png eps2:/Users/saito/data/phangs/co_ratio/eps/fw03.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figw03a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/figw03b_n4321_m8_ap.png


### figure 4
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figw04a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/figw04b_n4321_m8_bm.png eps2:/Users/saito/data/phangs/co_ratio/eps/fw04.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figw04a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/figw04b_n4321_m8_bm.png


### figure 5
convert /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median_w.png eps2:/Users/saito/data/phangs/co_ratio/eps/fw05.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/heatmap_r21_median_w.png


### figure 7
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figw07a_n4321_w1_v_r21_ap.png /Users/saito/data/phangs/co_ratio/eps/figw07b_n4321_w2_v_r21_ap.png /Users/saito/data/phangs/co_ratio/eps/figw07c_n4321_w3_v_r21_ap.png eps2:/Users/saito/data/phangs/co_ratio/eps/fw07.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figw07a_n4321_w1_v_r21_ap.png /Users/saito/data/phangs/co_ratio/eps/figw07b_n4321_w2_v_r21_ap.png /Users/saito/data/phangs/co_ratio/eps/figw07c_n4321_w3_v_r21_ap.png



#### aperture-inverse_weighted-average
### figure 3
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figiw03a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/figiw03b_n4321_m8_ap.png eps2:/Users/saito/data/phangs/co_ratio/eps/fiw03.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figiw03a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/figiw03b_n4321_m8_ap.png


### figure 4
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figiw04a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/figiw04b_n4321_m8_bm.png eps2:/Users/saito/data/phangs/co_ratio/eps/fiw04.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figiw04a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/figiw04b_n4321_m8_bm.png


### figure 7
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figiw07a_n4321_w1_v_r21_ap.png /Users/saito/data/phangs/co_ratio/eps/figiw07b_n4321_w2_v_r21_ap.png /Users/saito/data/phangs/co_ratio/eps/figiw07c_n4321_w3_v_r21_ap.png eps2:/Users/saito/data/phangs/co_ratio/eps/fiw07.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figiw07a_n4321_w1_v_r21_ap.png /Users/saito/data/phangs/co_ratio/eps/figiw07b_n4321_w2_v_r21_ap.png /Users/saito/data/phangs/co_ratio/eps/figiw07c_n4321_w3_v_r21_ap.png

