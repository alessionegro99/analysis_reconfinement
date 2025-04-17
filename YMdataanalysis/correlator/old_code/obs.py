from re import S
from pseudo_header import *

# parameters 

runName = sys.argv[1]
binsize = int(sys.argv[2])

NBS = 200

path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + runName

# data acquisition

data = np.loadtxt(path + '/data/dati.dat')

N = len(data[0])

G_colind = np.arange(4, N, 2)

# observables calculation

# G

G = []
G_blocks = []

for count, i in enumerate(G_colind):
    G.append(data[:,i])
    G_blocks.append(np.mean(get_blocks(G[count], binsize), axis = 1))

R = len(G)

n = len(G_blocks[0])

G_mean = np.mean(G_blocks, axis = 1)
errG_mean = np.sqrt(np.var(G_blocks, axis = 1, ddof = 1)/n)

# correlation matrix

G_centered = []

for i in range(R):
    G_centered.append(G[i] - np.mean(G[i]))


sigma = [[0 for _ in range(R)] for _ in range(R)]
sigma_blocks = [[0 for _ in range(R)] for _ in range(R)]
sigma_blocks_BS = [[0 for _ in range(R)] for _ in range(R)]
errsigma = [[0 for _ in range(R)] for _ in range(R)]

# blocking for correlation matrix

for i in range(R):
    for j in range(i+1):
        sigma_blocks[i][j] = np.mean(get_blocks(G_centered[i]*G_centered[j], binsize), axis = 1)
        sigma_blocks_BS[i][j] = bootstrap(sigma_blocks[i][j], NBS)

        # sigma_ij = 1/N-1 sum_i((x_ki-<x_k>)(x_kj-<x_j>))
        sigma[i][j] = np.mean(np.sum(sigma_blocks_BS[i][j], axis = 1)/(n-1))
        errsigma[i][j] = np.var(np.sum(sigma_blocks_BS[i][j], axis = 1)/(n-1))

        # matrice simmetrica
        sigma[j][i] = sigma[i][j]
        errsigma[j][i] = errsigma[i][j]

vec1 = [i for i in range(R)]
vec2 = G_mean
vec3 = errG_mean

nome_file = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + runName +"/data/output.txt"
scrivi_su_file(vec1, vec2, vec3, nome_file)
np.savetxt("/home/anegro99/Documents/thesis/analysis/data/correlator/" + runName +"/data/cov.txt", sigma)
np.savetxt("/home/anegro99/Documents/thesis/analysis/data/correlator/" + runName +"/data/errcov.txt", errsigma)