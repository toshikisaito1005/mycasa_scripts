import os
import sys
import csv
import glob
import datetime
import numpy as np
import astropy.units as u
from astroquery.ned import Ned
from astroquery.alma import Alma
time_stamp = str(datetime.datetime.now()).split(" ")[0].replace("-", "")

search_freq = 492.16065100
data_suffix = "c_atom10"
key_download = "txt" # fits

dir_data = "../proj_goals_" + data_suffix + "/"
list_donwload_txt = "goals_" + data_suffix + "_" + time_stamp + ".txt"

done = glob.glob(dir_data)
if not done:
    os.system("mkdir " + dir_data)

array_goals = np.loadtxt("goals_list_name.txt",
                         delimiter = ",",
                         dtype = "S20")

loop = len(array_goals)

list_donwload = []
#for i in range(loop):
for i in range([0,1]):
    result_table = Ned.query_object(array_goals[i])
    print(array_goals[i] + ", z=" + str(result_table["Redshift"][0]))
    target = Alma.query_object(array_goals[i])
    spws = target['Frequency support'].tolist()
    uids = target['Member ous id'].tolist()
    loop2 = len(spws)
    for j in range(loop2):
        print(uids[j])
        for k in range(len(spws[j].split(" U "))):
            freq_cover = spws[j].split(" U ")[k].split(",")[0]
            edge_low = float(freq_cover.split("..")[0].replace("[", ""))
            edge_high = float(freq_cover.split("..")[1].replace("GHz", ""))
            redshift_plus_1 = 1 + result_table["Redshift"][0]
            obs_freq = search_freq/redshift_plus_1
            if edge_low < obs_freq < edge_high:
                print(data_suffix + " is here!")
                uid_url_table = Alma.stage_data(uids[j])
                myAlma = Alma()
                myAlma.cache_location = \
                    "/mnt/fhgfs/saito/data_node4/" \
                    + dir_data.replace("../", "")
                if key_download == "fits":
                    filelist = \
                        myAlma.download_and_extract_files(uid_url_table['URL'])
                    list_donwload.append(array_goals[i])
                elif key_download == "txt":
                    list_donwload.append(array_goals[i])

np.savetxt(dir_data + list_donwload_txt, np.array(list(set(list_donwload))), fmt = "%s")

