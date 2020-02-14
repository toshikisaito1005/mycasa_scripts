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
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig02a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/fig02b_n4321_m8_ap.png eps2:/Users/saito/data/phangs/co_ratio/eps/f02.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/fig02a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/fig02b_n4321_m8_ap.png


### figure 3
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig03a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/fig03b_n4321_m8_bm.png eps2:/Users/saito/data/phangs/co_ratio/eps/f03.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/fig03a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/fig03b_n4321_m8_bm.png


### figure 4
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig04a_n4321_r21_v_co21_ap.png /Users/saito/data/phangs/co_ratio/eps/fig04b_n4321_r21_v_co21_bm.png eps2:/Users/saito/data/phangs/co_ratio/eps/f04.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/fig04a_n4321_r21_v_co21_ap.png /Users/saito/data/phangs/co_ratio/eps/fig04b_n4321_r21_v_co21_bm.png


### figure 5
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f05a_bm_vs_ap_R21_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f05b_bm_vs_ap_P21_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/fig05a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f05c_r21_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f05d_p21_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/fig05b.png
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig05a.png /Users/saito/data/phangs/co_ratio/eps/fig05b.png eps2:/Users/saito/data/phangs/co_ratio/eps/f05.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/f05a_bm_vs_ap_R21_median_n4321*.png /Users/saito/data/phangs/co_ratio/eps/f05b_bm_vs_ap_P21_median_n4321*.png /Users/saito/data/phangs/co_ratio/eps/f05c_r21_median_vs_bm_n4321*.png /Users/saito/data/phangs/co_ratio/eps/f05d_p21_median_vs_bm_n4321*.png /Users/saito/data/phangs/co_ratio/eps/fig05a.png /Users/saito/data/phangs/co_ratio/eps/fig05b.png


### figure 6
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f06a_bm_vs_ap_R21_w_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06b_bm_vs_ap_P21_w_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06c_bm_vs_ap_R21_iw_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06d_bm_vs_ap_P21_iw_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/fig06a.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f06e_r21_w_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06f_m21_w_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06g_r21_iw_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06h_m21_iw_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/fig06b.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f06i_bm_vs_ap_R21_w2_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06j_bm_vs_ap_P21_w2_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06k_bm_vs_ap_R21_iw2_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06l_bm_vs_ap_P21_iw2_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/fig06c.png

convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/f06m_r21_w2_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06n_m21_w2_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06o_r21_iw2_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06p_m21_iw2_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/fig06d.png

convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fig06a.png /Users/saito/data/phangs/co_ratio/eps/fig06b.png /Users/saito/data/phangs/co_ratio/eps/fig06c.png /Users/saito/data/phangs/co_ratio/eps/fig06d.png eps2:/Users/saito/data/phangs/co_ratio/eps/f06.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/f06a_bm_vs_ap_R21_w_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06b_bm_vs_ap_P21_w_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06c_bm_vs_ap_R21_iw_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06d_bm_vs_ap_P21_iw_median_n4321.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f06e_r21_w_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06f_m21_w_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06g_r21_iw_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06h_m21_iw_median_vs_bm_n4321.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f06i_bm_vs_ap_R21_w2_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06j_bm_vs_ap_P21_w2_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06k_bm_vs_ap_R21_iw2_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06l_bm_vs_ap_P21_iw2_median_n4321.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/f06m_r21_w2_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06n_m21_w2_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06o_r21_iw2_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/f06p_m21_iw2_median_vs_bm_n4321.png
rm -rf /Users/saito/data/phangs/co_ratio/eps/fig06a.png /Users/saito/data/phangs/co_ratio/eps/fig06b.png /Users/saito/data/phangs/co_ratio/eps/fig06c.png /Users/saito/data/phangs/co_ratio/eps/fig06d.png





#### aperture-weighted-average
### figure 2
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figw02a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/figw02b_n4321_m8_ap.png eps2:/Users/saito/data/phangs/co_ratio/eps/fw02.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figw02a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/figw02b_n4321_m8_ap.png


### figure 3
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figw03a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/figw03b_n4321_m8_bm.png eps2:/Users/saito/data/phangs/co_ratio/eps/fw03.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figw03a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/figw03b_n4321_m8_bm.png


### figure 4
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figw04a_n4321_r21_v_co21_ap.png /Users/saito/data/phangs/co_ratio/eps/figw04b_n4321_r21_v_co21_bm.png eps2:/Users/saito/data/phangs/co_ratio/eps/fw04.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figw04a_n4321_r21_v_co21_ap.png /Users/saito/data/phangs/co_ratio/eps/figw04b_n4321_r21_v_co21_bm.png


### figure 5
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fw05a_bm_vs_ap_R21_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/fw05b_bm_vs_ap_P21_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/figw05a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fw05c_r21_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/fw05d_p21_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/figw05b.png
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figw05a.png /Users/saito/data/phangs/co_ratio/eps/figw05b.png eps2:/Users/saito/data/phangs/co_ratio/eps/fw05.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/fw05a_bm_vs_ap_R21_median_n4321*.png /Users/saito/data/phangs/co_ratio/eps/fw05b_bm_vs_ap_P21_median_n4321*.png /Users/saito/data/phangs/co_ratio/eps/fw05c_r21_median_vs_bm_n4321*.png /Users/saito/data/phangs/co_ratio/eps/fw05d_p21_median_vs_bm_n4321*.png /Users/saito/data/phangs/co_ratio/eps/figw05a.png /Users/saito/data/phangs/co_ratio/eps/figw05b.png





#### aperture-inverse_weighted-average
### figure 2
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figiw02a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/figiw02b_n4321_m8_ap.png eps2:/Users/saito/data/phangs/co_ratio/eps/fiw02.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figiw02a_n4321_m0_ap.png /Users/saito/data/phangs/co_ratio/eps/figiw02b_n4321_m8_ap.png


### figure 3
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figiw03a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/figiw03b_n4321_m8_bm.png eps2:/Users/saito/data/phangs/co_ratio/eps/fiw03.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figiw03a_n4321_m0_bm.png /Users/saito/data/phangs/co_ratio/eps/figiw03b_n4321_m8_bm.png


### figure 4
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figiw04a_n4321_r21_v_co21_ap.png /Users/saito/data/phangs/co_ratio/eps/figiw04b_n4321_r21_v_co21_bm.png eps2:/Users/saito/data/phangs/co_ratio/eps/fiw04.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/figiw04a_n4321_r21_v_co21_ap.png /Users/saito/data/phangs/co_ratio/eps/figiw04b_n4321_r21_v_co21_bm.png


### figure 5
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fiw05a_bm_vs_ap_R21_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/fiw05b_bm_vs_ap_P21_median_n4321.png /Users/saito/data/phangs/co_ratio/eps/figiw05a.png
convert +append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/fiw05c_r21_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/fiw05d_p21_median_vs_bm_n4321.png /Users/saito/data/phangs/co_ratio/eps/figiw05b.png
convert -append -border 0x0 /Users/saito/data/phangs/co_ratio/eps/figiw05a.png /Users/saito/data/phangs/co_ratio/eps/figiw05b.png eps2:/Users/saito/data/phangs/co_ratio/eps/fiw05.eps

rm -rf /Users/saito/data/phangs/co_ratio/eps/fiw05a_bm_vs_ap_R21_median_n4321*.png /Users/saito/data/phangs/co_ratio/eps/fiw05b_bm_vs_ap_P21_median_n4321*.png /Users/saito/data/phangs/co_ratio/eps/fiw05c_r21_median_vs_bm_n4321*.png /Users/saito/data/phangs/co_ratio/eps/fiw05d_p21_median_vs_bm_n4321*.png /Users/saito/data/phangs/co_ratio/eps/figiw05a.png /Users/saito/data/phangs/co_ratio/eps/figiw05b.png


