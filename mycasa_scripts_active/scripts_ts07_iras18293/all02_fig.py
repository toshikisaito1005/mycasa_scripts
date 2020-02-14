import glob
from subprocess import call

scripts = glob.glob("fig*.py")
for i in range(len(scripts)):
    print("# run " + scripts[i])
    execfile(scripts[i])
