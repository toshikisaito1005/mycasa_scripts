import glob

print("### Before running this script, make sure you already run")
print("### radex_grid_ngc3110.py.")

scripts = glob.glob("myim*.py")

for i in range(len(scripts)):
    print("### running " + scripts[i])
    execfile(scripts[i])
