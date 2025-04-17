import polars as pl
import numpy as np
import matplotlib.pyplot as plt

from lib import _plot

def blocking(t0, block_size, discard_end = False):
    """
    Subdivide a numeric vector into blocks and replace each block with its mean.

    Parameters:
    - t0 (list or np.ndarray): the input numeric vector.
    - block_size (int): the size of each block.
    - discard_end

    Returns:
    - np.ndarray: vector of block means.
    """
    
    df = pl.DataFrame({"t0":t0})
    n = df.height
    
    n_full = n // block_size
    remainder = n % block_size
    
    df = df.with_columns((pl.arange(0,n) // block_size).alias("block"))
        
    if discard_end and remainder != 0:
        df = df.filter(pl.col("block") < n_full)
    
    block_means = df.group_by("block").agg(
        pl.col("t0").mean().alias("mean")
        ).sort("block")
    
    return block_means["mean"].to_numpy()

def bootstrap_samples(t0, n_samples = 200, seed = 0):
    """
    Generate bootstrap samples from a numeric vector.
    
    Parameters:
    - t0 (list or np.ndarray): the original data.
    - n_samples (int): number of bootstrap samples.
    - seed (int): seed for reproducibility.
    
    Returns:
    - np.ndarray: returns n_samples bootstrap samples of the original data.
    """
    
    df = pl.DataFrame({"t0": t0})
    sample_size = df.height
    
    t = [
        df.sample(n = sample_size, with_replacement=True, seed=seed+i)
        .get_column("t0").to_numpy()
        for i in range(n_samples)]
    
    return t

def bootstrap_analysis(t0, n_samples = 200, block_size_0 = 2, block_size_step = 2, seed = 0):
    """
    Performs a bootstrap with blocking analysis of a timeseries and plots
    the result.
    
    Parameters:
    - t0 (list or np.ndarray): numerical vector containing the time series.
    - n_samples (int): number of bootstrap samples.
    - block_size_0 (int): starting block size.
    - seed (int): seed for reproducibility
    """
    
    b_t0_std_mean = []
    d_b_t0_std_mean = []
    for block_size in range(block_size_0, len(t0)//20, block_size_step):
        
        b_t0 = blocking(t0, block_size, discard_end = False)
        n_blocks = len(b_t0)
        
        b_t0_std_mean.append(np.std(b_t0)/np.sqrt(n_blocks))
        
        b_t = bootstrap_samples(b_t0, n_samples, seed)
        b_t_std_mean = np.std(b_t, axis = 1)/np.sqrt(n_blocks)
        d_b_t0_std_mean.append(np.std(b_t_std_mean))

        
    x = range(block_size_0, len(t0)//20, block_size_step)
    y = b_t0_std_mean
    d_y = d_b_t0_std_mean
    
    plt.figure()
    plt.errorbar(x, y, yerr = d_y
             , fmt = 'o-', capsize = 5
             , marker = 'o'
             , linestyle = '-', linewidth = 0.5
             , color = _plot.IBM_COLORS["blue"])
    
    plt.xlabel(r'$K$')
    plt.ylabel(r'$\sigma_{\overline{F(x)}}$', rotation = 0)
    plt.title("Standard deviation of the mean as a function of the blocksize.")
        
    plt.yscale('log')   
    
    plt.xticks(rotation=45)  
    plt.yticks(rotation=45) 
    
    plt.grid (True, which = 'both', linestyle = '--', linewidth = 0.5)
    
    plt.show()
        

