import glob

#do_step = [1,2,3,4,5,6]
do_step = [0,1,2,3,4,5]

### create plots and images for aperture-averaged data
for i in range(len(do_step)):
    scripts = glob.glob("f" + str(do_step[i]).zfill(2) + "_*.py")
    for j in range(len(scripts)):
        print("### run " + scripts[j])
        execfile(scripts[j])
