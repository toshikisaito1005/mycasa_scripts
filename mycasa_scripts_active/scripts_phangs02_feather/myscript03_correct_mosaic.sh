dir_data=../test00/
dir_output=../data/

### 7m
# mosaic shape for test01 and test02
sed -e "/015.49.35.334573/d" -e "/015.44.23.565427/d" -e "/01:36:52.49/d" -e "/01:36:30.88/d" -e "/01:36:51.6/d" -e "/01:36:31.7/d" $dir_data"test00.aca.cycle5.ptg.txt" > "test01.aca.cycle5.ptg.txt"
sed '83,162d' test01.aca.cycle5.ptg.txt > test02.aca.cycle5.ptg.txt
sed '1,82d' test01.aca.cycle5.ptg.txt > test03.aca.cycle5.ptg.txt

# create casa region files
sed "/^#/d" test01.aca.cycle5.ptg.txt | sed "s/J2000 /ellipse[[/g" | sed "s/ /,/g" | sed "s/,,10.0/],[23.423arcsec,23.423arcsec],0deg]/g" > testtest.txt
echo "#CRTFv0" | cat - testtest.txt > $dir_output"test01.aca.cycle5.ptg.region"
rm -rf testtest.txt

sed "/^#/d" test02.aca.cycle5.ptg.txt | sed "s/J2000 /ellipse[[/g" | sed "s/ /,/g" | sed "s/,,10.0/],[23.423arcsec,23.423arcsec],0deg]/g" > testtest.txt
echo "#CRTFv0" | cat - testtest.txt > $dir_output"test02.aca.cycle5.ptg.region"
rm -rf testtest.txt

sed "/^#/d" test03.aca.cycle5.ptg.txt | sed "s/J2000 /ellipse[[/g" | sed "s/ /,/g" | sed "s/,,10.0/],[23.423arcsec,23.423arcsec],0deg]/g" > testtest.txt
echo "#CRTFv0" | cat - testtest.txt > $dir_output"test03.aca.cycle5.ptg.region"
rm -rf testtest.txt


### 12m
# mosaic shape for test01 and test02
sed -e "/015.44.20/d" -e "/015.49.38/d" -e "/015.49.27.308018/d" -e "/015.44.31.591982/d" -e "/01:36:52.6/d" -e "/01:36:30.7/d" -e "/01:36:31.1/d" -e "/01:36:52.2/d" $dir_data"test00.alma.cycle5.1.ptg.txt" > "test01.alma.cycle5.1.ptg.txt"
sed '308,612d' test01.alma.cycle5.1.ptg.txt > test02.alma.cycle5.1.ptg.txt
sed '1,307d' test01.alma.cycle5.1.ptg.txt > test03.alma.cycle5.1.ptg.txt

# create casa region files
sed "/^#/d" test01.alma.cycle5.1.ptg.txt | sed "s/J2000 /ellipse[[/g" | sed "s/ /,/g" | sed "s/,,10.0/],[13.664arcsec,13.664arcsec],0deg]/g" > testtest.txt
echo "#CRTFv0" | cat - testtest.txt > $dir_output"test01.alma.cycle5.1.ptg.region"
rm -rf testtest.txt

sed "/^#/d" test02.alma.cycle5.1.ptg.txt | sed "s/J2000 /ellipse[[/g" | sed "s/ /,/g" | sed "s/,,10.0/],[13.664arcsec,13.664arcsec],0deg]/g" > testtest.txt
echo "#CRTFv0" | cat - testtest.txt > $dir_output"test02.alma.cycle5.1.ptg.region"
rm -rf testtest.txt

sed "/^#/d" test03.alma.cycle5.1.ptg.txt | sed "s/J2000 /ellipse[[/g" | sed "s/ /,/g" | sed "s/,,10.0/],[13.664arcsec,13.664arcsec],0deg]/g" > testtest.txt
echo "#CRTFv0" | cat - testtest.txt > $dir_output"test03.alma.cycle5.1.ptg.region"
rm -rf testtest.txt


# rm -rf $dir_data
