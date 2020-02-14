# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
import radex

T_kins = np.arange(3,100,1)*u.K
n_H2s  = np.logspace(2.0, 7.0, 40.)/u.cm**3
column_H2 = [10**22.0,
             10**22.1,
             10**22.2,
             10**22.3,
             10**22.4,
             10**22.5]

for i in range(len(column_H2)):
    ### 12co
    N_mol  = (column_H2[i]*3e-4)/u.cm**2
    calc = radex.RADEX('CO')
    calc.default_params['N_mol'] = N_mol

    params_10, output_10 = calc('1-0', T_kin=T_kins, n_H2=n_H2s)
    params_21, output_21 = calc('2-1', T_kin=T_kins, n_H2=n_H2s)

    ### 13co
    N_mol  = (column_H2[i]*3e-4/70)/u.cm**2
    calc = radex.RADEX('13CO')
    calc.default_params['N_mol'] = N_mol

    params_13co10, output_13co10 = calc('1-0',
                                        T_kin=T_kins,
                                        n_H2=n_H2s)
    params_13co21, output_13co21 = calc('2-1',
                                        T_kin=T_kins,
                                        n_H2=n_H2s)

    x_axis = params_10['T_kin']
    y_axis = params_10['n_H2']
    ratio_12co21_12co10  = output_21['I']/output_10['I']
    ratio_12co21_13co21  = output_21['I']/output_13co21['I']

    data = np.c_[x_axis.flatten(),
                 y_axis.flatten(),
                 ratio_12co21_12co10.flatten(),
                 ratio_12co21_13co21.flatten()]

    np.savetxt('out_' + str(i * 0.1 + 21.0) + '.txt',data,delimiter=' ')

"""
plt.figure(figsize=(10,5))
plt.subplots_adjust(0.1, 0.15, 0.99, 0.9)
plt.pcolormesh(x_axis.value, y_axis.value, ratio_12co21_13co21.value)
plt.yscale('log')
plt.xlim([10,300])
plt.ylim([1e3,1e6])
plt.xlabel('T_kin (K)')
plt.ylabel('log n_H2 (cm^-3)')
plt.title('CO(3-2)/CO(1-0) Intensity Ratio')
plt.colorbar()
plt.savefig('radex_example.png')
"""
