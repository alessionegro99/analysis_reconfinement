import numpy as np
import pyerrors as pe
from matplotlib import pyplot as plt
from scipy.special import k0

import InlineArgPars
# import corr_reader
import fit_wrapper2
import IBM_plot_palette as palette

with InlineArgPars.InlineArgPars() as parser:
    x_min = parser.next_arg('min_distance', int, 15)
    therm = parser.next_arg('thermalization', int, 2000)
    N_boot = parser.next_arg('bootstrap_samples', int, 500)
    boot_block = parser.next_arg('bootstrap_block', int, 1000)
    N_s = parser.next_arg('space_side', int, 96)
    nreplica = parser.next_arg('num_replica', int, 48)
    x_max = parser.next_arg('max_distance', int, 24)

    cor_fit = not parser.look_for_option('uncorrelated', 'u')
    human_out = parser.look_for_option('human_out', 'o')

data_file_list = [f'roughdata/dati_{i}.dat' for i in range(nreplica)]
'''
0              1              2        3       4        5        6        7
plaqs          plaqt          poly_re  poly_im pp_re(0) pp_im(0) pp_re(1) pp_im(1) ...
0.956857552388 0.956854677147 0.758461789074 0 0.60820464571 0   0.581870588724 0  0.577177716657 0 0.575967147783 0 0.575759224156 0 0.575121881029 0 0.575314077538 0 0.574966454238 0 0.575463328408 0 0.57524751978 0 0.574738728988 0 0.575265655248 0 0.575651100694 0 0.575963235927 0 0.57547984533 0 0.575322723342 0 0.575020089165 0 0.575422924822 0 0.575519403118 0 0.575237769625 0 0.575464965741 0 0.575360432699 0 0.575061878728 0 0.57488234508 0 
'''

cols = np.arange(2 * x_min, 2 * x_max, 2) + 4
dist = np.arange(x_min, x_max)

data_cols = np.empty((len(dist), 0))
for data_fn in data_file_list:
    data_run = np.loadtxt(data_fn, usecols=cols, unpack=True, skiprows=therm)
    start = data_run.shape[1] % boot_block
    data_cols = np.concatenate((data_cols, data_run[:, start:]), axis=1)

use_pyerrors = False

min_eig_val = np.empty(N_boot)
ampl_boot = np.empty(N_boot)
ener_boot = np.empty(N_boot)
cpar_boot = np.empty((N_boot, 2, 2))
chi2_boot = np.empty(N_boot)

dist_num = data_cols.shape[0]
stat = data_cols.shape[1]
n_blocks = stat // boot_block

def fit_func(x, ener, ampl):
    return ampl * (k0(ener * x) + k0(ener * (N_s - x)))
p0 = np.asarray([1, 1], float)
bounds = 0, np.inf

plt.figure('boots')
for i in range(N_boot):
    print(f'{i} / {N_boot}', end = '\r')

    chosen = np.random.randint(0, n_blocks, size=n_blocks)
    # chosen = np.repeat(chosen, boot_block)
    data_col_boot = np.reshape(data_cols, (dist_num, n_blocks, boot_block))[:, chosen, :]
    data_col_boot = np.reshape(data_col_boot, (dist_num, n_blocks * boot_block))

    if use_pyerrors:
        obs_list = []
        for d, _ in enumerate(dist):
            obs = pe.Obs([data_col_boot[d]], ['ens'])
            obs_list.append(obs)

        poly_corr = corr_reader.MyCorr(obs_list, N_s, dist)

        x_fit = poly_corr.dist_to_numpy()
        y_fit = poly_corr.value_to_numpy()
        c_fit = poly_corr.covariance()

    else:
        x_fit = dist
        y_fit = data_col_boot.mean(axis=1)

        blocked_data_col = data_col_boot.reshape(len(dist), n_blocks, boot_block).mean(axis=-1)
        errors = np.std(blocked_data_col, axis=1) / n_blocks**0.5
        c_fit = errors[:, None] * np.corrcoef(data_col_boot) * errors[None, :]

    plt.scatter(x_fit, y_fit, color=palette.color_dict[1])
    min_eig_val[i] = np.linalg.eigvalsh(c_fit)[0]

    fit_res = fit_wrapper2.correlated_fit(fit_func, x_fit, y_fit, c_fit, p0=p0, bounds=bounds)
    ener_boot[i], ampl_boot[i] = fit_res.opt
    cpar_boot[i] = fit_res.cov
    chi2_boot[i] = fit_res.chi_sqr / fit_res.num_dof

    p0 = fit_res.opt

blocked_data_col = data_cols.reshape(len(dist), n_blocks, boot_block).mean(axis=-1)
errors = np.std(blocked_data_col, axis=1) / n_blocks**0.5
c_fit = errors[:, None] * np.corrcoef(data_cols) * errors[None, :]

x_fit = dist
y_fit = data_cols.mean(axis=1)
plt.scatter(x_fit, y_fit, color=palette.color_dict[0])

fit_res = fit_wrapper2.correlated_fit(fit_func, x_fit, y_fit, c_fit, p0=p0, bounds=bounds)
ener_og, ampl_og = fit_res.opt
err_ener_og, err_ampl_og = fit_res.err_opt
chi_sqr_og = fit_res.chi_sqr / fit_res.num_dof

plt.figure('first_histo')
plt.plot(data_col_boot[0], '.')
plt.plot(data_cols[0], '.')

min_eig_og = np.linalg.eigvalsh(c_fit)[0]

plt.figure('min_eig_histo')
plt.hist(min_eig_val, 50)
print('min eig', boot_block, min_eig_val.mean(), min_eig_val.std(), min_eig_og)

plt.figure('ener_histo')
plt.hist(ener_boot, 50, color=palette.bright_color_dict[1])
ylim = plt.ylim()
height = 0.8 * ylim[1]
plt.errorbar(ener_og, height, xerr=err_ener_og, **palette.data(2), label='original sample')
height = 0.9 * ylim[1]
plt.errorbar(ener_boot.mean(), height, xerr=ener_boot.std(), **palette.data(1), label='bootstrap')
print('energy', ener_boot.mean(), ener_boot.std(), cpar_boot[:, 0, 0].mean()**0.5, ener_og, err_ener_og)
plt.xlabel(r'$E_0$')
plt.legend()

plt.figure('chi_sqr')
plt.hist(chi2_boot, 50)
print('chi_sqr', chi2_boot.mean(), chi2_boot.std(), chi_sqr_og)

plt.show()
