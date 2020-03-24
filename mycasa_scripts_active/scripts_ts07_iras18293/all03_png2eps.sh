dir_data="/Users/saito/data/myproj_published/proj_ts07_iras18293/eps/"

rm -rf figures/
cp -r ${dir_data%/*} figures
rm -rf figures/*.eps
convert figures/radial_alpha_flat.png -resize 30% figures/radial_alpha_flat.png
convert figures/radial_alpha_nonflat.png -resize 30% figures/radial_alpha_nonflat.png
convert figures/radial_param_flat.png -resize 30% figures/radial_param_flat.png
convert figures/scatter_ci_dust.png -resize 30% figures/scatter_ci_dust.png
convert figures/scatter_co_ci.png -resize 30% figures/scatter_co_ci.png
convert figures/scatter_co_dust.png -resize 30% figures/scatter_co_dust.png
convert figures/scatter_co_ratio.png -resize 30% figures/scatter_co_ratio.png


### figure 1
convert -crop 683x570+42+20 $dir_data"iras18293_12co10_m0.png" $dir_data"iras18293_12co10_m0b.png"
convert -crop 683x570+42+20 $dir_data"iras18293_ci10_m0.png" $dir_data"iras18293_ci10_m0b.png"
convert -crop 683x570+42+20 $dir_data"iras18293_b8contin.png" $dir_data"iras18293_b8continb.png"
convert -crop 683x570+42+20 $dir_data"radial_flux.png" $dir_data"radial_fluxb.png"
convert +append -border 0x0 $dir_data"iras18293_12co10_m0b.png" $dir_data"iras18293_ci10_m0b.png" $dir_data"fig01a.png"
convert +append -border 0x0 $dir_data"iras18293_b8continb.png" $dir_data"radial_fluxb.png" $dir_data"fig01b.png"
convert -append -border 0x0 $dir_data"fig01a.png" $dir_data"fig01b.png" eps2:$dir_data"fig01.eps"

rm -rf $dir_data"iras18293_12co10_m0.png" $dir_data"iras18293_12co10_m0b.png"
rm -rf $dir_data"iras18293_ci10_m0.png" $dir_data"iras18293_ci10_m0b.png"
rm -rf $dir_data"radial_flux.png" $dir_data"radial_fluxb.png"
rm -rf $dir_data"iras18293_b8contin.png" $dir_data"iras18293_b8continb.png"
rm -rf $dir_data"fig01a.png" $dir_data"fig01b.png"

convert $dir_data"fig01.png" eps2:$dir_data"fig01.eps"

rm -rf $dir_data"fig01.png"


# figure 2
convert -crop 2550x2400+80+400 $dir_data"scatter_co_ci.png" $dir_data"scatter_co_cib.png"
convert -crop 2550x2400+80+400 $dir_data"scatter_ci_dust.png" $dir_data"scatter_ci_dustb.png"
convert -crop 2550x2400+80+400 $dir_data"scatter_co_ratio.png" $dir_data"scatter_co_ratiob.png"
convert -crop 2550x2400+80+400 $dir_data"scatter_cico_dust.png" $dir_data"scatter_cico_dustb.png"
convert +append -border 0x0 $dir_data"scatter_co_cib.png" $dir_data"scatter_ci_dustb.png" $dir_data"fig02a.png"
convert +append -border 0x0 $dir_data"scatter_co_ratiob.png" $dir_data"scatter_cico_dustb.png" $dir_data"fig02b.png"
convert -append -border 0x0 $dir_data"fig02a.png" $dir_data"fig02b.png" eps2:$dir_data"fig02.eps"

#convert -crop 2550x2400+80+400 $dir_data"scatter_co_ci.png" $dir_data"scatter_co_cib.png"
#convert -crop 2550x2400+80+400 $dir_data"scatter_co_ratio.png" $dir_data"scatter_co_ratiob.png"
#convert -crop 2550x2400+80+400 $dir_data"scatter_co_dust.png" $dir_data"scatter_co_dustb.png"
#convert -crop 2550x2400+80+400 $dir_data"scatter_ci_dust.png" $dir_data"scatter_ci_dustb.png"
#convert +append -border 0x0 $dir_data"scatter_co_cib.png" $dir_data"scatter_co_ratiob.png" $dir_data"fig02a.png"
#convert +append -border 0x0 $dir_data"scatter_co_dustb.png" $dir_data"scatter_ci_dustb.png" $dir_data"fig02b.png"
#convert -append -border 0x0 $dir_data"fig02a.png" $dir_data"fig02b.png" $dir_data"fig02.png"

rm -rf $dir_data"scatter_co_ci.png" $dir_data"scatter_co_cib.png"
rm -rf $dir_data"scatter_ci_dust.png" $dir_data"scatter_ci_dustb.png"
rm -rf $dir_data"scatter_co_ratio.png" $dir_data"scatter_co_ratiob.png"
rm -rf $dir_data"scatter_cico_dust.png" $dir_data"scatter_cico_dustb.png"
rm -rf $dir_data"fig02a.png" $dir_data"fig02b.png"

#convert $dir_data"fig02.png" eps2:$dir_data"fig02.eps"
#rm -rf $dir_data"fig02.png"


# figure 3
convert -crop 2150x1320+110+40 $dir_data"histo_ci_co.png" $dir_data"histo_ci_cob.png"
convert -crop 2065x1320+185+40 $dir_data"histo_ci_dust.png" $dir_data"histo_ci_dustb.png"
convert -crop 2150x1390+110+40 $dir_data"histo_ci_co_weight.png" $dir_data"histo_ci_co_weightb.png"
convert -crop 2065x1390+185+40 $dir_data"histo_ci_dust_weight.png" $dir_data"histo_ci_dust_weightb.png"
convert +append -border 0x0 $dir_data"histo_ci_cob.png" $dir_data"histo_ci_dustb.png" $dir_data"fig03a.png"
convert +append -border 0x0 $dir_data"histo_ci_co_weightb.png" $dir_data"histo_ci_dust_weightb.png" $dir_data"fig03b.png"

convert -append -border 0x0 $dir_data"fig03a.png" $dir_data"fig03b.png" eps2:$dir_data"fig03.eps"

rm -rf $dir_data"histo_ci_co.png" $dir_data"histo_ci_cob.png"
rm -rf $dir_data"histo_ci_dust.png" $dir_data"histo_ci_dustb.png"
rm -rf $dir_data"histo_ci_co_weight.png" $dir_data"histo_ci_co_weightb.png"
rm -rf $dir_data"histo_ci_dust_weight.png" $dir_data"histo_ci_dust_weightb.png"
rm -rf $dir_data"histo_ci_co_weightb.png" $dir_data"histo_ci_dust_weightb.png"


# figure 4
convert -crop 683x570+42+20 $dir_data"iras18293_ratio_m0.png" $dir_data"fig03.png"
rm -rf $dir_data"iras18293_ratio_m0.png"

convert $dir_data"fig04.png" eps2:$dir_data"fig04.eps"

rm -rf $dir_data"fig04.png"


# figure 5
convert -crop 2150x1520+70+150 $dir_data"radial_alpha_co.png" $dir_data"radial_alpha_cob.png"
convert -crop 2150x1520+70+150 $dir_data"radial_alpha_ci.png" $dir_data"radial_alpha_cib.png"
convert +append -border 0x0 $dir_data"radial_alpha_cob.png" $dir_data"radial_alpha_cib.png" eps2:$dir_data"fig05.eps"

rm -rf $dir_data"radial_alpha_co.png" $dir_data"radial_alpha_cob.png"
rm -rf $dir_data"radial_alpha_ci.png" $dir_data"radial_alpha_cib.png"

# figure 6
convert -crop 2000x1800+70+300 $dir_data"heatmap_alpha_ci.png" eps2:$dir_data"fig06.eps"

rm -rf $dir_data"heatmap_alpha_ci.png"
