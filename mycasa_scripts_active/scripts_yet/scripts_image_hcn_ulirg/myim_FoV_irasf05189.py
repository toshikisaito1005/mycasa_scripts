import csv

dir_work = "../../hcn_ulirgs/other/"

###irasf05189
name_csv = dir_work + "irasf05189_fov.csv"
name_casafile = dir_work + "irasf05189_fov"
data = []
with open(name_csv, "rb") as f:
    reader = csv.reader(f)
    header = next(reader)
    
    for row in reader:
        data.append(row)

cl.done()
for i in range(len(data)):
    fov_ra, fov_dec = data[i][0], data[i][1]
    direction = "J2000 " + str(fov_ra) + "deg " + str(fov_dec) + "deg"
    cl.addcomponent(dir = direction,
                    flux = 1.0,
                    fluxunit = "Jy",
                    freq = "229.564GHz",
                    shape = "Gaussian",
                    majoraxis = "18.53arcsec",
                    minoraxis = "18.53arcsec",
                    positionangle = "0.0deg")

ia.fromshape(name_casafile+".im",[512,512,1,1], overwrite = True)
cs = ia.coordsys()
cs.setunits(["rad","rad","","Hz"])
cell_rad = qa.convert(qa.quantity("0.2arcsec"),"rad")["value"]
cs.setincrement([-cell_rad,cell_rad],"direction")
cs.setreferencevalue([qa.convert("80.255708deg","rad")["value"],qa.convert("-25.362514deg","rad")["value"]],type="direction")
cs.setreferencevalue("229.564GHz","spectral")
cs.setincrement("1GHz","spectral")
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)

max_value = imstat(name_casafile+".im")["max"][0]
immath(imagename=name_casafile+".im",
       mode = "evalexpr",
       expr = "IM0/" + str(max_value),
       outfile = name_casafile+".im.imath")
os.system("rm -rf " + name_casafile + ".fits")
exportfits(imagename = name_casafile + ".im.imath",
           fitsimage = name_casafile + ".fits",
           overwrite = True)
os.system("rm -rf " + name_casafile + ".im*")
