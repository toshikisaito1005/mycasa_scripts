dir_data="/Users/saito/data/myproj_published/proj_phangs02_feather/figures/"

### figure 1
convert +append -border 0x0 $dir_data"test01.png" $dir_data"test02.png" $dir_data"fig01a.png"
convert +append -border 0x0 $dir_data"test03.png" $dir_data"test04.png" $dir_data"fig01b.png"
convert -append -border 0x0 $dir_data"fig01a.png" $dir_data"fig01b.png" $dir_data"fig01.png"

rm -rf $dir_data"test01.png" $dir_data"test02.png" $dir_data"fig01a.png"
rm -rf $dir_data"test03.png" $dir_data"test04.png" $dir_data"fig01b.png"

### figure 2
convert +append -border 0x0 $dir_data"test06_12m+7m_br_2p5.png" $dir_data"test06_12m+7m_br.pb.png" $dir_data"test06_12m+7m_br_2p5.diff.png" $dir_data"fig01a.png"
convert +append -border 0x0 $dir_data"test07_12m+7m_br_2p5.png" $dir_data"test07_12m+7m_br.pb.png" $dir_data"test07_12m+7m_br_2p5.diff.png" $dir_data"fig01b.png"
convert -append -border 0x0 $dir_data"fig01b.png" $dir_data"fig01a.png" $dir_data"fig02.png"

rm -rf $dir_data"test06_12m+7m_br_2p5.png" $dir_data"test06_12m+7m_br.pb.png" $dir_data"test06_12m+7m_br_2p5.diff.png" $dir_data"fig01a.png"
rm -rf $dir_data"test07_12m+7m_br_2p5.png" $dir_data"test07_12m+7m_br.pb.png" $dir_data"test07_12m+7m_br_2p5.diff.png" $dir_data"fig01b.png"

### figure 3
convert +append -border 0x0 $dir_data"test07_featherfirst_sd1p0_br.png" $dir_data"test07_pbcorrfirst_sd1p0_br.png" $dir_data"test07_pbcorrfirst_sd1p0_tpcut_br.png" $dir_data"fig02a.png"
convert +append -border 0x0 $dir_data"test07_featherfirst_sd1p0_br.diff.png" $dir_data"test07_pbcorrfirst_sd1p0_br.diff.png" $dir_data"test07_pbcorrfirst_sd1p0_tpcut_br.diff.png" $dir_data"fig02b.png"
convert -append -border 0x0 $dir_data"fig02a.png" $dir_data"fig02b.png" $dir_data"fig03.png"

rm -rf $dir_data"test07_featherfirst_sd1p0_br.png" $dir_data"test07_pbcorrfirst_sd1p0_br.png" $dir_data"test07_pbcorrfirst_sd1p0_tpcut_br.png" $dir_data"fig02a.png"
rm -rf $dir_data"test07_featherfirst_sd1p0_br.diff.png" $dir_data"test07_pbcorrfirst_sd1p0_br.diff.png" $dir_data"test07_pbcorrfirst_sd1p0_tpcut_br.diff.png" $dir_data"fig02b.png"

### figure 4
convert +append -border 0x0 $dir_data"test06_featherfirst_sd1p0_br.png" $dir_data"test06_pbcorrfirst_sd1p0_br.png" $dir_data"test06_pbcorrfirst_sd1p0_tpcut_br.png" $dir_data"fig02a.png"
convert +append -border 0x0 $dir_data"test06_featherfirst_sd1p0_br.diff.png" $dir_data"test06_pbcorrfirst_sd1p0_br.diff.png" $dir_data"test06_pbcorrfirst_sd1p0_tpcut_br.diff.png" $dir_data"fig02b.png"
convert -append -border 0x0 $dir_data"fig02a.png" $dir_data"fig02b.png" $dir_data"fig04.png"

rm -rf $dir_data"test06_featherfirst_sd1p0_br.png" $dir_data"test06_pbcorrfirst_sd1p0_br.png" $dir_data"test06_pbcorrfirst_sd1p0_tpcut_br.png" $dir_data"fig02a.png"
rm -rf $dir_data"test06_featherfirst_sd1p0_br.diff.png" $dir_data"test06_pbcorrfirst_sd1p0_br.diff.png" $dir_data"test06_pbcorrfirst_sd1p0_tpcut_br.diff.png" $dir_data"fig02b.png"

### figure 5
convert +append -border 0x0 $dir_data"test0607_featherfirst_then_merge.png" $dir_data"test0607_pbcorrfirst_then_merge.png" $dir_data"fig04a.png"
convert +append -border 0x0 $dir_data"test0607_featherfirst_then_merge.diff.png" $dir_data"test0607_pbcorrfirst_then_merge.diff.png" $dir_data"fig04b.png"
convert -append -border 0x0 $dir_data"fig04a.png" $dir_data"fig04b.png" $dir_data"fig05.png"

rm -rf $dir_data"test0607_featherfirst_then_merge.png" $dir_data"test0607_pbcorrfirst_then_merge.png" $dir_data"fig04a.png"
rm -rf $dir_data"test0607_featherfirst_then_merge.diff.png" $dir_data"test0607_pbcorrfirst_then_merge.diff.png" $dir_data"fig04b.png"

### figure 6
convert +append -border 0x0 $dir_data"test0607_12m+7m_merge.png" $dir_data"test0607_merge_then_pbcorrfirst.png" $dir_data"fig05a.png"
convert +append -border 0x0 $dir_data"test0607_12m+7m_merge.diff.png" $dir_data"test0607_merge_then_pbcorrfirst.diff.png" $dir_data"fig05b.png"
convert -append -border 0x0 $dir_data"fig05a.png" $dir_data"fig05b.png" $dir_data"fig06.png"

rm -rf $dir_data"test0607_12m+7m_merge.png" $dir_data"test0607_merge_then_pbcorrfirst.png" $dir_data"fig05a.png"
rm -rf $dir_data"test0607_12m+7m_merge.diff.png" $dir_data"test0607_merge_then_pbcorrfirst.diff.png" $dir_data"fig05b.png"

### figure 7
convert -crop 720x260+20+180 $dir_data"test0607_featherfirst_then_merge.diff_clip.png" $dir_data"fig7a.png"
convert -crop 720x260+20+180 $dir_data"test0607_pbcorrfirst_then_merge.diff_clip.png" $dir_data"fig7b.png"
convert -crop 720x260+20+180 $dir_data"test0607_merge_then_pbcorrfirst.diff_clip.png" $dir_data"fig7d.png"
convert -crop 720x260+20+180 $dir_data"test0607_12m+7m_merge.diff_clip.png" $dir_data"fig7c.png"

convert +append -border 0x0 $dir_data"fig7a.png" $dir_data"fig7b.png" $dir_data"fig07upp.png"
convert +append -border 0x0 $dir_data"fig7c.png" $dir_data"fig7d.png" $dir_data"fig07low.png"
convert -append -border 0x0 $dir_data"fig07upp.png" $dir_data"fig07low.png" $dir_data"fig07.png"

rm -rf $dir_data"test0607_featherfirst_then_merge.diff_clip.png" $dir_data"fig7a.png"
rm -rf $dir_data"test0607_pbcorrfirst_then_merge.diff_clip.png" $dir_data"fig7b.png"
rm -rf $dir_data"test0607_merge_then_pbcorrfirst.diff_clip.png" $dir_data"fig7d.png"
rm -rf $dir_data"test0607_12m+7m_merge.diff_clip.png" $dir_data"fig7c.png"
rm -rf $dir_data"fig07upp.png" $dir_data"fig07low.png"

# move
cp -r ${dir_data%/*} .
