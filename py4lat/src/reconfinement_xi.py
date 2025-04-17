from lib import _plot
from lib import _bootstrap

import polars as pl
import matplotlib.pyplot as plt
import numpy as np

def analysis(path):
    df = pl.read_csv(f"{path}L96_0/data/dati_0.003000_0.dat"
                     , has_header=False
                     , skip_rows = 1
                     , separator=" "
                     , new_columns=["Us", "Ut", "ReP", "ImP", "G0", "typo1", "Gmin", "TrP**2", "typo2"])
    
    df = df.drop(["typo1", "typo2"])
    
    ReP_t0 = df["ReP"].to_numpy()
            
    _bootstrap.bootstrap_analysis(t0 = ReP_t0
                                  , n_samples = 200
                                  , block_size_0 = 2
                                  , block_size_step = 10
                                  , seed = 0)
    
    