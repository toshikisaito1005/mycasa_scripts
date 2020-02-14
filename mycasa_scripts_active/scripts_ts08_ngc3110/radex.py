# coding: utf-8

'''
Module: radex.py
Created by: Akio Taniguchi
Version: 1.0
'''

import os
import re
from copy import deepcopy
from urllib2 import urlopen
from itertools import product
from subprocess import Popen, PIPE
# dependent modules
import numpy as np
from astropy import units as u
# configuration
import radex_config as conf

available = conf.moldat.keys()

class RADEX(object):
    def __init__(self, mol):
        '''Create a RADEX calculator.

        Parameters
        ----------
        mol: str
            A molecular name for calculation decscibed in radex_config.
            If the corresponding data is not found in the moldat directory,
            this program will try to download it from LAMDA database.

        Examples
        ----------
        >>> import radex
        >>> calc = radex.RADEX('CO')
        '''
        self.mol = mol
        self.moldat = conf.moldat[mol]
        self.radex_input = deepcopy(conf.radex_input)
        self.default_params = deepcopy(conf.radex_params)
        moldat_url = '{}/{}'.format(conf.moldat_url, self.moldat)
        moldat_dir = os.path.expanduser(conf.moldat_dir)
        moldat_path = '{}/{}'.format(moldat_dir, self.moldat)

        # download a moldat (*.dat) if it is not found
        if self.moldat not in os.listdir(moldat_dir):
            print('{} is not in the RADEX moldat direcrory'.format(self.moldat))
            print('--> downloading {} from the LAMDA website'.format(self.moldat))
            r = urlopen(moldat_url)
            f = open(moldat_path, 'w')
            f.write(r.read())
            r.close()
            f.close()

        # read a moldat and extract information
        f = open(moldat_path, 'r')
        self._energy_levels = self._get_energy_levels(f)
        self._transitions = self._get_transitions(f)
        self.transitions = self._transitions.keys()
        f.close()

    def __call__(self, transition, **kwargs):
        '''Execute RADEX and return the values.

        Parameters
        ----------
        transition: str
            A transition described in transitions.
        kwargs: int or float with units
            You can change default parameters described in default_params.
            + T_kin: kinematic tempeature (K)
            + n_H2:  gas density (cm^-3)
            + N_mol: column density of molecule (cm^-2)
            + dV:    velocity width (km/s)
            + T_bg:  background temperature (K)

        Returns
        ----------
        params: dictionary
            Parameters used for Calculation.
        output: dictionary
            Values Calculated by RADEX.

        Examples
        ----------
        Calculate values of CO(3-2) at T_kin=100K and other parameters as default:
        >>> import radex
        >>> from astropy import units as u
        >>> calc = radex.RADEX('CO')
        >>> params, output = calc('3-2', T_kin=100*u.K)

        Calculate grid values of CO(3-2) at T_kin=[100,200,300] K,
        n_H2=[1e3,1e4,1e5] cm^-3, and other parameters as default:
        >>> params, output = calc('3-2', T_kin=[100,200,300]*u.K, n_H2=[1e3,1e4,1e5]/u.cm**3)
        '''
        # override parameters if spacified
        params = deepcopy(self.default_params)
        params.update(kwargs)

        # parameters related to molecule, transition
        f_rest = self._transitions[transition]['f_rest']
        params['mol'] = self.moldat
        params['f_min'] = f_rest - 0.01*u.GHz
        params['f_max'] = f_rest + 0.01*u.GHz

        # parameters related to grid calculation
        params['T_kin'], params['n_H2'], params['N_mol'], params['T_bg'], params['dV']\
        = np.meshgrid(
            params['T_kin'], params['n_H2'], params['N_mol'], params['T_bg'], params['dV'],
            indexing='ij'
        )

        # output formats
        output = {}
        shape  = params['T_kin'].shape
        output['E_u']     = np.zeros(shape) * u.K
        output['freq']    = np.zeros(shape) * u.GHz
        output['wavel']   = np.zeros(shape) * u.um
        output['T_ex']    = np.zeros(shape) * u.K
        output['tau']     = np.zeros(shape) * u.dimensionless_unscaled
        output['T_r']     = np.zeros(shape) * u.K
        output['pop_up']  = np.zeros(shape) * u.dimensionless_unscaled
        output['pop_low'] = np.zeros(shape) * u.dimensionless_unscaled
        output['I']       = np.zeros(shape) * (u.K*u.km/u.s)
        output['F']       = np.zeros(shape) * (u.erg/u.s/u.cm**2)

        for i in product(*map(range, shape)):
            # execute RADEX
            params_input = deepcopy(params)
            params_input['T_kin'] = params_input['T_kin'][i]
            params_input['n_H2']  = params_input['n_H2'][i]
            params_input['N_mol'] = params_input['N_mol'][i]
            params_input['T_bg']  = params_input['T_bg'][i]
            params_input['dV']    = params_input['dV'][i]
            params_input = self._remove_units(params_input)
            radex_input  = self.radex_input.format(**params_input)
            proc = Popen([conf.radex_path], stdin=PIPE, stdout=PIPE, shell=True)
            proc.communicate(input=radex_input)

            # read RADEX output and store values
            f = open(params_input['out'], 'r')
            kwd = ''
            pat = re.compile('calculation finished', re.I)
            while not pat.search(kwd):
                kwd = f.readline()

            f.readline()
            f.readline()
            elems = f.readline().rstrip('\n').split()
            output['E_u'][i]     = float(elems[3]) * u.K
            output['freq'][i]    = float(elems[4]) * u.GHz
            output['wavel'][i]   = float(elems[5]) * u.um
            output['T_ex'][i]    = float(elems[6]) * u.K
            output['tau'][i]     = float(elems[7]) * u.dimensionless_unscaled
            output['T_r'][i]     = float(elems[8]) * u.K
            output['pop_up'][i]  = float(elems[9]) * u.dimensionless_unscaled
            output['pop_low'][i] = float(elems[10]) * u.dimensionless_unscaled
            output['I'][i]       = float(elems[11]) * (u.K*u.km/u.s)
            output['F'][i]       = float(elems[12]) * (u.erg/u.s/u.cm**2)

        # remove RADEX output
        os.remove(params['out'])
        os.remove('radex.log')

        # remove redundancies
        params['T_kin'] = self._remove_redundancy(params['T_kin'])
        params['n_H2']  = self._remove_redundancy(params['n_H2'])
        params['N_mol'] = self._remove_redundancy(params['N_mol'])
        params['T_bg']  = self._remove_redundancy(params['T_bg'])
        params['dV']    = self._remove_redundancy(params['dV'])
        output = {key: np.squeeze(item) for key, item in output.items()}

        return params, output

    def _get_energy_levels(self, f):
        kwd = ''
        pat = re.compile('energy levels', re.I)
        while not pat.search(kwd):
            kwd = f.readline()

        n_level = int(f.readline().rstrip('\n'))
        f.readline()
        levels = []
        for i in range(n_level):
            elems = f.readline().rstrip('\n').split()
            level  = elems[3]
            energy = float(elems[1])/u.cm
            weight = float(elems[2])/u.dimensionless_unscaled
            levels.append({'level': level, 'energy': energy, 'weight': weight})

        return np.array(levels)

    def _get_transitions(self, f):
        kwd = ''
        pat = re.compile('radiative transitions', re.I)
        while not pat.search(kwd):
            kwd = f.readline()

        n_transition = int(f.readline().rstrip('\n'))
        f.readline()
        transitions = {}
        for i in range(n_transition):
            elems = f.readline().rstrip('\n').split()
            l_upper = self._energy_levels[int(elems[1])-1]['level']
            l_lower = self._energy_levels[int(elems[2])-1]['level']
            transition = '{}-{}'.format(l_upper, l_lower)
            A_ul = float(elems[3])/u.s
            f_rest = float(elems[4])*u.GHz
            E_u = float(elems[5])*u.K
            transitions[transition] = {'f_rest': f_rest, 'A_ul': A_ul, 'E_u': E_u}

        return transitions

    def _remove_units(self, params):
        params = deepcopy(params)
        for key in params.keys():
            try:
                params[key] = params[key].value
            except:
                params[key] = params[key]

        return params

    def _remove_redundancy(self, param):
        if len(np.unique(param)) == 1:
            return np.unique(param)[0]
        else:
            return np.squeeze(param)

    def __repr__(self):
        return 'RADEX({})'.format(self.mol)

    def __str__(self):
        return 'RADEX({})'.format(self.mol)
