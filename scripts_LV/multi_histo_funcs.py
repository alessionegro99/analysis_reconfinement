import numpy as np
from scipy import special

def update_log_z(boltzmann_func, old_log_z, betas, data_cols):
    stat = np.array([data.shape[1] for data in data_cols])
    new_log_z = np.empty_like(old_log_z)

    for k, beta_tg in enumerate(betas): # loop over beta target
        log_numer = np.empty_like(old_log_z)
        for i, dat_i in enumerate(data_cols): # numerator loop over datasets
            log_denom = np.empty((len(betas), stat[i]))
            for j, bj in enumerate(betas): # denominator loop over dataset
                boltz_diff = boltzmann_func(dat_i, bj) - boltzmann_func(dat_i, beta_tg)
                log_denom[j] = np.log(stat[j]) - old_log_z[j] + boltz_diff
            # sum ove j in denominator and over sample of i in numerator
            log_numer[i] = special.logsumexp(-special.logsumexp(log_denom, axis=0)) 
        new_log_z[k] = special.logsumexp(log_numer) # sum over i
    
    return new_log_z

def compute_new_log_z(target_beta, boltzmann_func, old_log_z, betas, data_cols):
    target_beta = np.atleast_1d(target_beta)

    stat = np.array([data.shape[1] for data in data_cols])
    new_log_z = np.empty(len(target_beta))

    for k, beta_tg in enumerate(target_beta): # loop over beta target
        log_numer = np.empty_like(old_log_z)
        for i, dat_i in enumerate(data_cols): # numerator loop over datasets
            log_denom = np.empty((len(betas), stat[i]))
            for j, bj in enumerate(betas): # denominator loop over dataset
                boltz_diff = boltzmann_func(dat_i, bj) - boltzmann_func(dat_i, beta_tg)
                log_denom[j] = np.log(stat[j]) - old_log_z[j] + boltz_diff
            # sum ove j in denominator and over sample of i in numerator
            log_numer[i] = special.logsumexp(-special.logsumexp(log_denom, axis=0)) 
        new_log_z[k] = special.logsumexp(log_numer) # sum over i
    
    return new_log_z

def compute_observable(target_beta, obs_func, boltzmann_func, target_log_z, old_log_z, betas, data_cols):
    target_beta = np.atleast_1d(target_beta)

    stat = np.array([data.shape[1] for data in data_cols])
    log_obs = np.empty(len(target_beta))

    for k, beta_tg in enumerate(target_beta): # loop over beta target
        log_numer = np.empty_like(old_log_z)
        for i, dat_i in enumerate(data_cols): # numerator loop over datasets
            log_denom = np.empty((len(betas), stat[i]))
            for j, bj in enumerate(betas): # denominator loop over dataset
                boltz_diff = boltzmann_func(dat_i, bj) - boltzmann_func(dat_i, beta_tg)
                log_denom[j] = np.log(stat[j]) - old_log_z[j] + boltz_diff
            # sum ove j in denominator and over sample of i in numerator
            log_numer[i] = special.logsumexp(np.log(obs_func(dat_i)) - special.logsumexp(log_denom, axis=0)) 
        log_obs[k] = special.logsumexp(log_numer) # sum over i

    return np.exp(log_obs - target_log_z)
