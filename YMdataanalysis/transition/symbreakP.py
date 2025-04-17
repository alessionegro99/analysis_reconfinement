from pseudo_header import *

file_path= "/home/anegro99/Documents/thesis/analysis/data/correlator/corr_24_7_96_0.007/data/dati.dat"

P = []

with open(file_path, "r") as inputfile:
    lines = inputfile.readlines()
    for line in lines:
        P.append(float(line.split()[2]))

n_bins = 50

print(np.mean(P), np.std(P))

plt.hist(P, n_bins)
plt.xlabel("P")
plt.ylabel("Number of measures")
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/correlator/symbreakingP.png")