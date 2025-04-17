from pseudo_header import *

# calculates means and error on two point Polyakov loop correlation value and stores it along with NBS statistical bootstrap copies

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
G_blocks_BSsamples = []
means = []
errs = []

# data blocking

for count, i in enumerate(G_colind):
    G.append(data[:,i])
    G_blocks.append(np.mean(get_blocks(G[count], binsize), axis = 1))

# statistical bootstrap

G_blocks_BS = bootstrap(np.array(G_blocks).T, NBS)

# new parameters
n = np.shape(G_blocks_BS)[1]

for i in range(np.shape(G_blocks_BS)[0]):
    means.append(np.mean(G_blocks_BS[i], axis = 0))
    errs.append(np.sqrt(np.var(G_blocks, axis = 1, ddof = 1)/n))

means = np.array(means)
errs = np.array(errs)

np.save(path + "/data/means", means)
np.save(path + "/data/errs", errs)





