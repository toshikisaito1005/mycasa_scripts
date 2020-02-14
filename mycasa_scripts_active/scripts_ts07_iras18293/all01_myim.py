import glob

data_tar = "/Users/saito/data/myproj_published/proj_ts07_iras18293.tgz"
data_untar = "/Users/saito/data/myproj_published/"
os.system("tar zxvf " + data_tar + " -C " + data_untar)

scripts = glob.glob("myim*.py")
for i in range(len(scripts)):
    print("# run " + scripts[i])
    execfile(scripts[i])
