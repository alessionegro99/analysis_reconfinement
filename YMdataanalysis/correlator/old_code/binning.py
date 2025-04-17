from pseudo_header import *

path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + sys.argv[1]
data = pd.read_csv(path + "/data/dati.dat", sep = ' ', header = None)
data = data.drop(data.columns[-1], axis=1)

column_index_start = 4
column_index_end = data.shape[1] - 1
R_corr = (column_index_end - column_index_start)//2 + 1
indexList = list(range(0, R_corr))

df = data.loc[:,column_index_start::2]
df = df.set_axis(indexList, axis=1)

G = [0] * df.shape[1]
stdG = [0] * df.shape[1]

KLIST = np.arange(100, df.shape[0]//8, 100)

# binning primary observable

for i in range(df.shape[1]):
    stdG[i] = []

for K in tqdm(KLIST):
    for i in range(df.shape[1]):
        G[i] = []

    for j in range(len(df)//K):
        for i in range(df.shape[1]):
            G[i].append(df[i].iloc[j*K:(K*(j+1))].mean())

    for i in range(df.shape[1]):
        stdG[i].append(np.std(G[i])/(np.sqrt(len(df)//K)))

# binning for secondary observable

stdsigmaK_12 = []

for K in KLIST:

    GK1_centered = []
    GK2_centered = []

    for j in range(len(df)//K):
        GK1_centered.append(df[1].iloc[j*K:(K*(j+1))] - df[1].iloc[j*K:(K*(j+1))].mean())
        GK2_centered.append(df[2].iloc[j*K:(K*(j+1))] - df[2].iloc[j*K:(K*(j+1))].mean())

    GK1_centered = np.array(GK1_centered)
    GK1_centered = np.array(GK2_centered)

    sigmaK_12 = []

    for j in range(len(df)//K):
        sigmaK_12.append(np.sum(GK1_centered[j]*GK2_centered[j]))

    sigmaK_12 = np.array(sigmaK_12)

    sigmaK_12 *= 1/(K-1)

    stdsigmaK_12.append(np.std(sigmaK_12)/(np.sqrt(len(df)//K)))

x = [K for K in KLIST]
        
for i in range(df.shape[1]):
    y = stdG[i]
    plt.xlabel('K')
    plt.ylabel('Err(G)')
    plt.title('G error as a function of the binsize')
    plt.grid()
    plt.plot(x, y, marker = "o", markersize = 0, linewidth = 1)
    plt.savefig(path + "/plots/binning/" + "binning_G(" + str(i) + ").png", facecolor='w')
    plt.close()

y = stdsigmaK_12
plt.xlabel('K')
plt.ylabel('Err(sigma_12)')
plt.title('sigma_12 error as a function of the binsize')
plt.grid()
plt.plot(x, y, marker = "o", markersize = 0, linewidth = 1)
plt.savefig(path + "/plots/binning/" + "binning_sigma_12.png", facecolor='w')
plt.close()
        



