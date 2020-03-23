# coding: utf-8

import numpy as np
from astropy import units as u

# RADEX moldat directory
moldat_dir = '/Users/saito/Radex/moldat'

# RADEX default parameters
radex_params = {}
radex_params['T_kin'] = 100*u.K
radex_params['n_H2']  = 1e3/u.cm**3
radex_params['N_mol'] = 1e13/u.cm**2
radex_params['dV']    = 20*(u.km/u.s)
radex_params['T_bg']  = 2.73*u.K
radex_params['out']   = 'radex.out'

# RADEX path (just spacify 'radex' if radex is added to $PATH)
radex_path = 'radex'

# URL of LAMDA database
moldat_url = 'http://home.strw.leidenuniv.nl/~moldata/datafiles'

# RADEX input format
radex_input = \
'''{mol}
{out}
{f_min:.3f} {f_max:.3f}
{T_kin:.3f}
1
H2
{n_H2:.3e}
{T_bg:.3f}
{N_mol:.3e}
{dV:.3f}
0'''

# Molecular name and corresponding molecular data
moldat = {
    'CO':      'co.dat',
    '13CO':    '13co.dat',
    'C17O':    'c17o.dat',
    'C18O':    'c18o.dat',
    'CS':      'cs@lique.dat',
    'HCl':     'hcl.dat',
    'OCS':     'ocs@xpol.dat',
    'SO':      'so@lique.dat',
    'SO2':     'so2.dat',
    'SiO':     'sio.dat',
    '29SiO':   '29sio.dat',
    'SiS':     'sis.dat',
    'SiC2':    'o-sic2.dat',
    'HCO+':    'hco+@xpol.dat',
    'H13CO+':  'h13co+@xpol.dat',
    'HC17O+':  'hc17o+@xpol.dat',
    'HC18O+':  'hc18o+@xpol.dat',
    'DCO+':    'dco+@xpol.dat',
    'N2H+':    'n2h+@xpol.dat',
    'HCS+':    'hcs+@xpol.dat',
    'HC3N':    'hc3n.dat',
    'HCN':     'hcn@xpol.dat',
    'H13CN':   'h13cn.dat',
    'HC15N':   'hc15n.dat',
    'HNC':     'hnc.dat',
    'p-C3H2':  'p-c3h2.dat',
    'o-C3H2':  'o-c3h2.dat',
    'p-H2O':   'ph2o@daniel.dat',
    'o-H2O':   'oh2o@daniel.dat',
    'p-H2CO':  'ph2co-h2.dat',
    'o-H2CO':  'oh2co-h2.dat',
    'OH':      'oh.dat',
    'e-CH3OH': 'e-ch3oh.dat',
    'a-CH3OH': 'a-ch3oh.dat',
    'p-NH3':   'p-nh3.dat',
    'o-NH3':   'o-nh3.dat',
    'p-NH2D':  'p-nh2d.dat',
    'a-NH2D':  'a-nh2d.dat',
    'HDO':     'hdo.dat',
    'p-H3O':   'p-h3o+.dat',
    'o-H3O':   'o-h3o+.dat',
    'HNCO':    'hnco.dat',
    'NO':      'no.dat',
    'CN':      'cn.dat',
    'CH3CN':   'ch3cn.dat',
    'O2':      'o2.dat',
    'HF':      'hf.dat',
    'p-H2S':   'ph2s.dat',
    'o-H2S':   'oh2s.dat',
    'p-H2CS':  'ph2cs.dat',
    'o-H2CS':  'oh2cs.dat',
    'OH+':     'oh+.dat',
    'C2H':     'c2h_h2_e.dat',
}
