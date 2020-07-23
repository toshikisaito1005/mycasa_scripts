dir_data="/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"

galname1=(eso267 eso297g011 eso297g012 eso507 eso557 ic4518e ic4518w ic5179 iras06592)
galname2=()

### figure 1
for var in ${galname[@]}
do
convert -crop 700x560+50+30 $dir_data$var"_m0.png" $dir_data$var"_m0_clip.png"
done
