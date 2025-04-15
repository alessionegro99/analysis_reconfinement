from lib import _plot

import polars as pl
import matplotlib.pyplot as plt
import numpy as np

def read(path):
    
    df = pl.read_csv(f"{path}L96_0/data/dati_0.003000_0.dat"
                     , has_header=False
                     , skip_rows = 1
                     , separator=" "
                     , new_columns=["Us", "Ut", "ReP", "ImP", "G0", "typo1", "Gmin", "TrP**2", "typo2"])
    
    df = df.drop(["typo1", "typo2"])
    
    Us = df["Us"].to_numpy()
    
    x = np.arange(0, len(Us), len(Us)//500)
    y = Us[x]
    
    plt.figure()
    plt.plot(x, y, linewidth = 0.5, color = _plot.IBM_COLORS["blue"])
    plt.xlabel(r'$t$', fontsize = 14)
    plt.ylabel(r'$U_s$', fontsize = 14, rotation = 0)
    plt.xticks(rotation=45)  # x-axis labels horizontal
    plt.yticks(rotation=45)  # y-axis labels horizontal
    plt.grid (True)
    plt.show()
    