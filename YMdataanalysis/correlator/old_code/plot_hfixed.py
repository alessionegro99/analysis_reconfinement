from pseudo_header import *

# 

directory_path = "/home/anegro99/Documents/thesis/analysis/data/correlator/"

# initializing lists

R, G, sG = [], [], []

for file_names in os.listdir(directory_path):
    components = file_names.split('_')
    r_tot = float(components[1])
    Nt = float(components[2])
    Ns = float(components[3])
    h = float(components[4])
    if h == 0.006: # picks only files with fixed h = 0.006
        
