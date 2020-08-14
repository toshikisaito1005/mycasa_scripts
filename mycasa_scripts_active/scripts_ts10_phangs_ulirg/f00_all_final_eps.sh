dir_data="/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"
dir_product="/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/products/"
#rm -rf $dir_product
#mkdir $dir_product

galname1=(eso267 eso297g011 eso297g012 eso507 eso557 ic4518e ic4518w ic5179 iras06592)
galname2=(irasf10409 irasf17138 mcg02 ngc1614 ngc2369 ngc3110 ngc3256 ngc5257 ngc6240)
galname3=(eso319)

### figure 1
#for var in ${galname1[@]} ${galname2[@]} ${galname3[@]}
#do
#convert -crop 710x560+40+30 $dir_data$var"_m0.png" $dir_data$var"_m0_clip.png"
#done

### figure 2
convert -crop 1800x1570+200+280 $dir_data"plot_scatter_all.png" $dir_data"plot_scatter_all.png"
convert -crop 1800x1570+200+280 $dir_data"plot_scatter_env.png" $dir_data"plot_scatter_env.png"
convert +append -border 0x0 $dir_data"plot_scatter_all.png" $dir_data"plot_scatter_env.png" $dir_product"plot_scatter.png"

### figure 3
convert -append -border 0x0 $dir_data"plot_pturb_all.png" $dir_data"plot_vir_all.png" $dir_product"plot_pturb_vir.png"

### figure 4
convert -crop 720x510+50+15 $dir_data"plot_size_pturb.png" $dir_data"plot_size_pturbb.png"
convert -crop 720x580+50+15 $dir_data"plot_size_virial.png" $dir_data"plot_size_virialb.png"

convert -crop 720x580+50+15 $dir_data"plot_mass_pturb.png" $dir_data"plot_mass_pturbb.png"


convert +append -border 0x0 $dir_data"plot_size_pturb.png" $dir_data"plot_size_virial.png" $dir_product"plot_size.png"

### 
