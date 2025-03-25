import numpy as np
import pyerrors as pe
from matplotlib import pyplot as plt

import bonanno_plot_palette as palette
from InlineArgPars import InlineArgPars

import multi_histo_funcs as mh

with InlineArgPars() as parser:
    input_fn = parser.next_arg('input_file_name', str, 'data_files.txt')
    thermal  = parser.next_arg('thermalization',  int, 1000)
    N_s      = parser.next_arg('N_s',             int, 50)
    N_t      = parser.next_arg('N_t',             int, 10) 

pars_vals = []
data_cols = []
old_log_z = []

with open(input_fn) as input_f:
    for line in input_f:
        data_fn, beta, h, *log_z = line.split(' ')

        try:
            old_log_z.append(float(log_z[0]))
        except (IndexError, ValueError):
            old_log_z.append(0.)
        
        pars_vals.append((float(beta), float(h)))
        data_cols.append(np.loadtxt(data_fn, skiprows=thermal + 1, unpack=True))
pars_vals = np.asarray(pars_vals, float)
old_log_z = np.asarray(old_log_z, float)

poly_susc = np.empty(len(pars_vals))
err_poly_susc = np.empty(len(pars_vals))

poly_g0 = np.empty(len(pars_vals))
poly_gmin = np.empty(len(pars_vals))
err_poly_g0 = np.empty(len(pars_vals))
err_poly_gmin = np.empty(len(pars_vals))
xi_len = np.empty(len(pars_vals))
err_xi_len = np.empty(len(pars_vals))

def poly_func(data_col):
    return np.abs(data_col[4])

def poly_sqr_func(data_col):
    return data_col[4]**2

def poly_fourth_func(data_col):
    return data_col[4]**4

def poly_g0_func(data_col):
    return data_col[5]

def poly_gmin_func(data_col):
    return data_col[6]

def boltzmann_func(data_col, pars):
    SP_VOL = N_s**2
    VOL = SP_VOL * N_t
    return VOL * pars[0] * (data_col[1] + 2 * data_col[2]) - SP_VOL * pars[1] * data_col[3]

for i, dat_i in enumerate(data_cols):
    p_abs_obs = pe.Obs([poly_func(dat_i)], [f'ens_{i}'])
    p_sqr_obs = pe.Obs([poly_sqr_func(dat_i)], [f'ens_{i}'])
    chi_p_obs = p_sqr_obs - p_abs_obs**2
    chi_p_obs.gamma_method()

    poly_g0_obs = pe.Obs([poly_g0_func(dat_i)], [f'ens_{i}'])
    poly_gmin_obs =  pe.Obs([poly_gmin_func(dat_i)], [f'ens_{i}'])
    xi_len_obs = (poly_g0_obs - poly_gmin_obs) / poly_gmin_obs
    xi_len_obs.gamma_method()

    poly_g0_obs.gamma_method()
    poly_gmin_obs.gamma_method()
    poly_g0[i] = poly_g0_obs.value
    err_poly_g0[i] = poly_g0_obs.dvalue
    poly_gmin[i] = poly_gmin_obs.value
    err_poly_gmin[i] = poly_gmin_obs.dvalue

    # print(pars_vals[i])
    # chi_p_obs.details()

    poly_susc[i] = N_s**2 * chi_p_obs.value
    err_poly_susc[i] = N_s**2 * chi_p_obs.dvalue

    xi_len[i] = xi_len_obs.value
    err_xi_len[i] = xi_len_obs.dvalue

plt.figure('poly_susc')
plt.errorbar(pars_vals[:, 1], poly_susc, err_poly_susc, **palette.data())

delta = 1
n_iter = 0
while delta > 1e-15:
    new_log_z = mh.update_log_z(boltzmann_func, old_log_z, pars_vals, data_cols)
    new_log_z -= np.mean(new_log_z)
    n_iter += 1
    delta = np.sum(((new_log_z - old_log_z) / new_log_z)**2)

    old_log_z = np.copy(new_log_z)
    print(f'{n_iter = } {delta = :.6e}', end = '\r')
print()

h_vals = pars_vals[:, 1]
b_vals = pars_vals[:, 0]

print(new_log_z)
plt.figure('log_z')
plt.scatter(h_vals, new_log_z)

N_INTERP = 50
h_target = np.linspace(h_vals.min(), h_vals.max(), N_INTERP)
b_target = b_vals[0] * np.ones_like(h_target)
params_target = np.vstack([b_target, h_target]).T

log_z_target = mh.compute_new_log_z(params_target, boltzmann_func, old_log_z, pars_vals, data_cols)
p_frt_target = mh.compute_observable(params_target, poly_fourth_func, boltzmann_func, log_z_target, old_log_z, pars_vals, data_cols)
p_sqr_target = mh.compute_observable(params_target, poly_sqr_func, boltzmann_func, log_z_target, old_log_z, pars_vals, data_cols)
p_abs_target = mh.compute_observable(params_target, poly_func, boltzmann_func, log_z_target, old_log_z, pars_vals, data_cols)

chi_p_target = N_s**2 * (p_sqr_target - p_abs_target**2)

plt.figure('poly_abs')
plt.plot(h_target, p_abs_target)

plt.figure('poly_susc')
plt.plot(h_target, chi_p_target)

binder_p_target = p_frt_target / p_sqr_target**2
plt.figure('poly_binder')
plt.plot(h_target, binder_p_target)

poly_g0_target = mh.compute_observable(params_target, poly_g0_func, boltzmann_func, log_z_target, old_log_z, pars_vals, data_cols)
poly_gmin_target = mh.compute_observable(params_target, poly_gmin_func, boltzmann_func, log_z_target, old_log_z, pars_vals, data_cols)
xisqr_target = (poly_g0_target - poly_gmin_target) / poly_gmin_target

plt.figure('poly g')
plt.errorbar(h_vals, poly_g0, err_poly_g0, label='g0', **palette.data(1))
plt.plot(h_target, poly_g0_target, **palette.fit(1))
plt.errorbar(h_vals, poly_gmin, err_poly_gmin, label='gmin', **palette.data(2))
plt.plot(h_target, poly_gmin_target, **palette.fit(2))
plt.legend()

plt.figure('corr_len')
plt.plot(h_target, xisqr_target)
plt.errorbar(h_vals, xi_len, err_xi_len, **palette.data())

plt.show()

