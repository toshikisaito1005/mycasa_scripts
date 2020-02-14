import os
import sys
import numpy as np
sys.path.append(os.getcwd())
import scripts_phangs_r21 as r21
import datetime
time1 = datetime.datetime.now()


do_steps = [3]
galnames = ["ngc4254"]
beam_sizes = [34.0] # do_steps = 0, 1, 2, 3
apertures = [[24]] # do_steps = 0, 1, 2
aperture_max = [36] # do_steps = 0, 1, 2, 3
# do_steps = 0: moment map creation
# do_steps = 1: line ratio map creation
# do_steps = 2: Nyquist sampling with a single beam size
# do_steps = 3: Nyquist sampling with a series of beam size


#####################
### Define
#####################
def do_step_0(dir_data, param, beam_size):
    r21.cube_to_moments(pixelmin = float(param[7]),
                        increment_mask = float(param[8]),
                        thres_masking = float(param[9]),
                        thres_mom = float(param[10]),
                        pbcut = float(param[11]),
                        dir_data = dir_data,
                        galname = param[0],
                        chans = param[3],
                        suffix = str(beam_size).replace(".","p"),
                        beam_size = beam_size,
                        rms_co10 = float(param[5]),
                        rms_co21 = float(param[6]))

    os.system("rm -rf " + dir_data + param[0] + "/*.cube")
    os.system("rm -rf " + dir_data + param[0] + "/*.mask")
    os.system("rm -rf " + dir_data + param[0] + "/*.mask.all")
    os.system("rm -rf " + dir_data + param[0] + "/*.masked")

    r21.convolve_wise(dir_data,param[0],"w1",7.5,beam_size)
    r21.convolve_wise(dir_data,param[0],"w2",7.5,beam_size)
    r21.convolve_wise(dir_data,param[0],"w3",7.5,beam_size)

def do_step_1(dir_data, param, beam_size):
    chans = param[3]
    n_ch = int(chans.split("~")[1]) - int(chans.split("~")[0]) + 1
    threesigma_co10 = float(param[5])*float(param[13])*sqrt(n_ch)*float(param[12])
    threesigma_co21 = float(param[6])*float(param[13])*sqrt(n_ch)*float(param[12])
    threesigma8_co10 = float(param[5])*float(param[12])
    threesigma8_co21 = float(param[5])*float(param[12])
    r21.moments_to_ratio(dir_data = dir_data,
                         galname = param[0],
                         suffix = str(beam_size).replace(".","p"),
                         threesigma_co10 = threesigma_co10,
                         threesigma_co21 = threesigma_co21,
                         threesigma8_co10 = threesigma8_co10,
                         threesigma8_co21 = threesigma8_co21)
        
    os.system("rm -rf " + dir_data + param[0] + "/*.mask")

def do_step_2(dir_data, param, beam_sizes, apertures):
    weights = ["no", "w", "iw"]
    for j in range(len(weights)):
        r21.sampling_co_wise(dir_data = dir_data,
                             galname = param[0],
                             chans = param[3],
                             suffix = str(beam_size).replace(".","p"),
                             apertures = apertures,
                             fov = float(param[14]),
                             beam_size = beam_size,
                             rms_co10 = float(param[5]),
                             rms_co21 = float(param[6]),
                             rms_w1 = float(param[15]),
                             rms_w2 = float(param[16]),
                             rms_w3 = float(param[17]),
                             velres = float(param[13]),
                             sn_ratio = float(param[12]),
                             ra = param[1],
                             decl = param[2],
                             weight = weights[j])


#####################
### Main procedure
#####################
dir_data = "/Users/saito/data/phangs/co_ratio/"
params = np.loadtxt("parameter_imaging.txt",dtype="S20")

### main part
for i in range(len(galnames)):
    param = params[params[:,0]==galnames[i]][0]
    beam_size = beam_sizes[i]

    if 0 in do_steps:
        do_step_0(dir_data, param, beam_size)

    if 1 in do_steps:
        do_step_1(dir_data, param, beam_size)

    if 2 in do_steps:
        for j in range(len(apertures)):
            do_step_2(dir_data, param, beam_size, apertures[j])

    if 3 in do_steps:
        while beam_size < aperture_max[i]+1:
            apertures = [np.arange(beam_size, aperture_max[i]+1, 2).tolist()]
            for j in range(len(apertures)):
                do_step_0(dir_data, param, beam_size)
                do_step_1(dir_data, param, beam_size)
                do_step_2(dir_data, param, beam_size, apertures[j])
                beam_size += 2.

### print running time
time2 = datetime.datetime.now()
print("#")
print("#")
print("# running time = " + str(time2 - time1))
print("#")
print("#")
