dir_data="/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"


### figure 0
convert +append -border 0x0 $dir_data"noise_ngc0628_co10.png" $dir_data"noise_vs_beam.png" $dir_data"fig00.png"

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
convert -append -border 0x0 $dir_data"violin_median.png" $dir_data"violin_disp.png" $dir_data"fig10.png"
convert -append -border 0x0 $dir_data"violin_median.png" $dir_data"violin_disp.png" eps2:$dir_data"fig10.eps"

rm -rf $dir_data"violin_median.png" $dir_data"violin_disp.png"


### figure 11
#convert -crop 600x600+80+30 $dir_data"ngc0628_r21_mask.png" $dir_data"ngc0628_r21_maskb.png"
#convert -crop 600x600+118+30 $dir_data"ngc3627_r21_mask.png" $dir_data"ngc3627_r21_maskb.png"
#convert -crop 600x600+80+30 $dir_data"ngc4321_r21_mask.png" $dir_data"ngc4321_r21_maskb.png"
#convert -crop 600x600+24+30 $dir_data"fig_mask_histo.png" $dir_data"fig_mask_histob.png"
convert -crop 600x600+24+30 $dir_data"fig_mask_histo.png" eps2:$dir_data"fig11.eps"

#convert +append -border 0x0 $dir_data"ngc0628_r21_maskb.png" $dir_data"ngc3627_r21_maskb.png" $dir_data"fig10a.png"
#convert +append -border 0x0 $dir_data"ngc4321_r21_maskb.png" $dir_data"fig_mask_histob.png" $dir_data"fig10b.png"
#convert -append -border 0x0 $dir_data"fig10a.png" $dir_data"fig10b.png" eps2:$dir_data"fig11.eps"

#rm -rf $dir_data"ngc0628_r21_mask.png" $dir_data"ngc0628_r21_maskb.png"
#rm -rf $dir_data"ngc3627_r21_mask.png" $dir_data"ngc3627_r21_maskb.png"
#rm -rf $dir_data"ngc4321_r21_mask.png" $dir_data"ngc4321_r21_maskb.png"
rm -rf $dir_data"fig_mask_histo.png" $dir_data"fig_mask_histob.png"
#rm -rf $dir_data"fig10a.png" $dir_data"fig10b.png"


### figure 12
convert -crop 600x600+80+30 $dir_data"ngc0628_r21_mask.png" $dir_data"ngc0628_r21_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc3627_r21_mask.png" $dir_data"ngc3627_r21_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc4321_r21_mask.png" $dir_data"ngc4321_r21_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc0628_cloud_mask.png" $dir_data"ngc0628_cloud_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc3627_cloud_mask.png" $dir_data"ngc3627_cloud_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc4321_cloud_mask.png" $dir_data"ngc4321_cloud_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc0628_env_mask.png" $dir_data"ngc0628_env_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc3627_env_mask.png" $dir_data"ngc3627_env_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc4321_env_mask.png" $dir_data"ngc4321_env_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc0628_piechart_mask.png" $dir_data"ngc0628_piechart_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc3627_piechart_mask.png" $dir_data"ngc3627_piechart_maskb.png"
convert -crop 600x600+80+30 $dir_data"ngc4321_piechart_mask.png" $dir_data"ngc4321_piechart_maskb.png"

convert -append -border 0x0 $dir_data"ngc0628_r21_maskb.png" $dir_data"ngc3627_r21_maskb.png" $dir_data"ngc4321_r21_maskb.png" $dir_data"fig12a.png"
convert -append -border 0x0 $dir_data"ngc0628_cloud_maskb.png" $dir_data"ngc3627_cloud_maskb.png" $dir_data"ngc4321_cloud_maskb.png" $dir_data"fig12b.png"
convert -append -border 0x0 $dir_data"ngc0628_env_maskb.png" $dir_data"ngc3627_env_maskb.png" $dir_data"ngc4321_env_maskb.png" $dir_data"fig12c.png"
convert -append -border 0x0 $dir_data"ngc0628_piechart_maskb.png" $dir_data"ngc3627_piechart_maskb.png" $dir_data"ngc4321_piechart_maskb.png" $dir_data"fig12d.png"
convert +append -border 0x0 $dir_data"fig12a.png" $dir_data"fig12b.png" $dir_data"fig12c.png" $dir_data"fig12d.png" $dir_data"fig12.png"

rm -rf $dir_data"ngc0628_r21_mask.png" $dir_data"ngc0628_r21_maskb.png"
rm -rf $dir_data"ngc3627_r21_mask.png" $dir_data"ngc3627_r21_maskb.png"
rm -rf $dir_data"ngc4321_r21_mask.png" $dir_data"ngc4321_r21_maskb.png"
rm -rf $dir_data"ngc0628_cloud_mask.png" $dir_data"ngc0628_cloud_maskb.png"
rm -rf $dir_data"ngc3627_cloud_mask.png" $dir_data"ngc3627_cloud_maskb.png"
rm -rf $dir_data"ngc4321_cloud_mask.png" $dir_data"ngc4321_cloud_maskb.png"
rm -rf $dir_data"ngc0628_env_mask.png" $dir_data"ngc0628_env_maskb.png"
rm -rf $dir_data"ngc3627_env_mask.png" $dir_data"ngc3627_env_maskb.png"
rm -rf $dir_data"ngc4321_env_mask.png" $dir_data"ngc4321_env_maskb.png"
rm -rf $dir_data"ngc0628_piechart_mask.png" $dir_data"ngc0628_piechart_maskb.png"
rm -rf $dir_data"ngc3627_piechart_mask.png" $dir_data"ngc3627_piechart_maskb.png"
rm -rf $dir_data"ngc4321_piechart_mask.png" $dir_data"ngc4321_piechart_maskb.png"
rm -rf $dir_data"fig12a.png" $dir_data"fig12b.png" $dir_data"fig12c.png" $dir_data"fig12d.png"

### figure 13
convert -crop 1970x320+15+0 $dir_data"histo_mask_gmc.png" $dir_data"histo_mask_gmcb.png"
convert -crop 1970x320+15+0 $dir_data"histo_mask_piechart.png" $dir_data"histo_mask_piechartb.png"
convert -crop 1970x400+15+0 $dir_data"histo_mask_env.png" $dir_data"histo_mask_envb.png"

convert -append -border 0x0 $dir_data"histo_mask_gmcb.png" $dir_data"histo_mask_piechartb.png" $dir_data"histo_mask_envb.png" eps2:$dir_data"fig13.eps"
convert -append -border 0x0 $dir_data"histo_mask_gmcb.png" $dir_data"histo_mask_piechartb.png" $dir_data"histo_mask_envb.png" $dir_data"fig13.png"

rm -rf $dir_data"histo_mask_gmc.png" $dir_data"histo_mask_gmcb.png"
rm -rf $dir_data"histo_mask_env.png" $dir_data"histo_mask_envb.png"
rm -rf $dir_data"histo_mask_piechart.png" $dir_data"histo_mask_piechartb.png"

### figure 13b
convert -crop 2000x585+40+80 $dir_data"scatter_mask_gmc.png" $dir_data"scatter_mask_gmcb.png"
convert -crop 2000x585+40+80 $dir_data"scatter_piechart.png" $dir_data"scatter_piechart.png"
convert -crop 2000x650+40+80 $dir_data"scatter_mask_env.png" $dir_data"scatter_mask_env.png"

convert -append -border 0x0 $dir_data"scatter_mask_gmcb.png" $dir_data"scatter_piechart.png" $dir_data"scatter_mask_env.png" eps2:$dir_data"fig13b.eps"
convert -append -border 0x0 $dir_data"scatter_mask_gmcb.png" $dir_data"scatter_piechart.png" $dir_data"scatter_mask_env.png" $dir_data"fig13b.png"

### figure 13c
convert -crop 2000x450+5+55 $dir_data"scatter_mask_env_piechart_ngc0628.png" $dir_data"scatter_mask_env_piechart_ngc0628b.png"
convert -crop 2000x450+5+55 $dir_data"scatter_mask_env_piechart_ngc3627.png" $dir_data"scatter_mask_env_piechart_ngc3627b.png"
convert -crop 2000x650+5+55 $dir_data"scatter_mask_env_piechart_ngc4321.png" $dir_data"scatter_mask_env_piechart_ngc4321b.png"

convert -append -border 0x0 $dir_data"scatter_mask_env_piechart_ngc0628b.png" $dir_data"scatter_mask_env_piechart_ngc3627b.png" $dir_data"scatter_mask_env_piechart_ngc4321b.png" eps2:$dir_data"fig13c.eps"

### figure 14
convert -crop 2250x900+120+50 $dir_data"fig_r21_vs_dist.png" $dir_data"fig_r21_vs_distb.png"
convert -crop 2250x860+120+90 $dir_data"fig_r21_vs_disp.png" $dir_data"fig_r21_vs_dispb.png"

convert -append -border 0x0 $dir_data"fig_r21_vs_distb.png" $dir_data"fig_r21_vs_dispb.png" eps2:$dir_data"fig14.eps"

rm -rf $dir_data"fig_r21_vs_dist.png" $dir_data"fig_r21_vs_distb.png"
rm -rf $dir_data"fig_r21_vs_disp.png" $dir_data"fig_r21_vs_dispb.png"


### figure 15
convert -crop 2250x860+120+90 $dir_data"fig_r21_vs_w1.png" $dir_data"fig_r21_vs_w1b.png"
convert -crop 2250x860+120+90 $dir_data"fig_r21_vs_w2.png" $dir_data"fig_r21_vs_w2b.png"
convert -crop 2250x860+120+90 $dir_data"fig_r21_vs_w3.png" $dir_data"fig_r21_vs_w3b.png"

convert -append -border 0x0 $dir_data"fig_r21_vs_w1b.png" $dir_data"fig_r21_vs_w2b.png" $dir_data"fig_r21_vs_w3b.png" eps2:$dir_data"fig15.eps"

rm -rf $dir_data"fig_r21_vs_w1.png" $dir_data"fig_r21_vs_w1b.png"
rm -rf $dir_data"fig_r21_vs_w2.png" $dir_data"fig_r21_vs_w2b.png"
rm -rf $dir_data"fig_r21_vs_w3.png" $dir_data"fig_r21_vs_w3b.png"


### figure 16
convert -crop 2250x900+120+50 $dir_data"fig_r21_vs_ratio_w3w1.png" $dir_data"fig_r21_vs_ratio_w3w1b.png"
convert -crop 2250x860+120+90 $dir_data"fig_r21_vs_ratio_w3co21.png" $dir_data"fig_r21_vs_ratio_w3co21b.png"

convert -append -border 0x0 $dir_data"fig_r21_vs_ratio_w3w1b.png" $dir_data"fig_r21_vs_ratio_w3co21b.png" eps2:$dir_data"fig16.eps"

rm -rf $dir_data"fig_r21_vs_ratio_w3w1.png" $dir_data"fig_r21_vs_ratio_w3w1b.png"
rm -rf $dir_data"fig_r21_vs_ratio_w3co21.png" $dir_data"fig_r21_vs_ratio_w3co21b.png"


### figure 17
convert +append -border 0x0 $dir_data"fig_obs_vs_model_histo_ngc0628.png" $dir_data"fig_obs_vs_model_mom0_ngc0628.png" $dir_data"fig_obs_vs_model_r21_ngc0628.png" $dir_data"fig17.png"
convert +append -border 0x0 $dir_data"fig_obs_vs_model_histo_ngc0628.png" $dir_data"fig_obs_vs_model_mom0_ngc0628.png" $dir_data"fig_obs_vs_model_r21_ngc0628.png" eps2:$dir_data"fig17.eps"

rm -rf $dir_data"fig_noise_vs_mom0_ngc0628.png" $dir_data"fig_obs_vs_model_histo_ngc0628.png"
rm -rf $dir_data"fig_obs_vs_model_mom0_ngc0628.png" $dir_data"fig_obs_vs_model_r21_ngc0628.png"


### figure 18
convert $dir_data"model_scatter.png" eps2:$dir_data"fig18.eps"
convert $dir_data"model_scatter.png" $dir_data"fig18.png"


### figure 19
convert -append -border 0x0 $dir_data"violin_median_simu.png" $dir_data"violin_width_simu.png" $dir_data"fig19.png"
convert -append -border 0x0 $dir_data"violin_median_simu.png" $dir_data"violin_width_simu.png" eps2:$dir_data"fig19.eps"

rm -rf $dir_data"model_scatter.png"
