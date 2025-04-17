from pseudo_header import *

path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + sys.argv[1]

# bootstrap parameter
NBS = 200

# loading data
data = np.loadtxt(path + '/data/dati.dat')

# number of columns in the file
N = len(data[0])

# column index array
G_colind = np.arange(4, N, 2)

# initialize vector and insert data into vector
G = []

for count, i in enumerate(G_colind):
   G.append(data[:,i])

# setting parameters and initializing vector
R = len(G)
n = len(G[0])
K = np.arange(10, n//10 + 500, 500)

# initializing vector for the blocking of primary observable
G_blocks = [0] * R
errG = [0] * R
for i in range(R):
    errG[i] = []

# error of blocking of primary observable
for k in tqdm(K):
    for i in range(R):
        G_blocks[i] = np.mean(get_blocks(G[i],k), axis = 1)
        errG[i].append(np.sqrt(np.var(G_blocks[i])/(n//k)))

# plotting the results     
for i in range(R):
    plt.xlabel('K')
    plt.ylabel('$err_G$')
    plt.title('$G$ error as a function of the block size $K$')
    plt.plot(K, errG[i], marker = "o", markersize = 0, linewidth = 2)
    plt.savefig(path + "/plots/binning/" + "binning_G(" + str(i) + ").png", facecolor='w')
    plt.close()
