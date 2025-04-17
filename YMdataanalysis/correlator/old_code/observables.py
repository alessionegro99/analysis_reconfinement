from re import S
from pseudo_header import *

runName = sys.argv[1]
L = int(sys.argv[2])
binsize = int(sys.argv[3])
NBOOTSTRAP = int(sys.argv[4])

path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + runName

data = pd.read_csv(path + "/data/dati.dat", sep = ' ', header = None)
data = data.drop(data.columns[-1], axis=1)

colStart = 4 
colEnd = data.shape[1] - 1
R_corr = (colEnd-colStart)//2 + 1
indexList = list(range(R_corr))

df = data.loc[0:,colStart:colEnd:2]
df = df.set_axis(indexList, axis=1)

meanGJK = [0] * df.shape[1]
stdGJK = [0] * df.shape[1]
G_binned = [0] * df.shape[1]
G_tmp = [0] * df.shape[1]
G = [0] * df.shape[1]

# binning

for i in range(df.shape[1]):
    G_binned[i] = list()
    G_tmp[i] = [0] * (len(df.index)//binsize)
    G[i] = [0] * (len(df.index)//binsize + 1)

for j in range(len(df.index)//binsize):
    for i in range(df.shape[1]):
        G_binned[i].append(df[i].iloc[j*binsize:(binsize*(j+1))].mean())

# Jackknife

for j in range(len(df.index)//binsize):
    for i in range(df.shape[1]):
        G_tmp[i] = G_binned[i].copy()

        G_tmp[i].remove(G_tmp[i][j])

        G[i][j] = np.mean(G_tmp[i])

for i in range(df.shape[1]):
    G[i][len(df.index)//binsize] = np.mean(G_binned[i])

for i in range(df.shape[1]):
    meanGJK[i] = np.mean(G[i])

for j in range (len(df.index)//binsize):
    if j==0:
        for i in range(df.shape[1]):
            G_tmp[i] = (meanGJK[i] - G[i][j])**2
    else:
        for i in range(df.shape[1]):
            G_tmp[i] += (meanGJK[i] - G[i][j])**2

for i in range(df.shape[1]):
    stdGJK[i] = np.sqrt((G_tmp[i]*(len(df.index)//binsize-1)/(len(df.index)//binsize)))

# covariance matrix sigma_ij with bootstrap

sigma_bs = [0] * NBOOTSTRAP

for i in range(NBOOTSTRAP):

    G_bs = [0] * len(G)

    for k in range(len(G)):
        G_bs[k] = [0] * len(G[0])

        for j in range(len(G[0])):

            r = random.randint(0, len(G[k]) - 1)

            G_bs[k][j] = G[k][r]

        G_bs[k] = np.array(G_bs[k])

    sigma_bs[i] = np.cov(G_bs)

sigma = np.sum(sigma_bs, axis=0)*1/NBOOTSTRAP

err = (1/NBOOTSTRAP*np.sum((sigma_bs - sigma)**2, axis = 0))**0.5

x = [i for i in range(R_corr)]
y = meanGJK
plt.grid()
plt.xlabel("R", fontsize = 20)
plt.ylabel("G(R)", fontsize = 20)
plt.title("Two point correlation function as a function of lattice spacing", fontsize = 20)
plt.plot(x, y, marker = "^", color = "red", markersize = 10, linewidth = 1)
plt.errorbar(x, y, stdGJK, color = "green",capsize = 10)
plt.savefig(path + '/plots/corr', facecolor='w')
plt.close()

x = [i for i in range(R_corr)]
y = meanGJK
plt.yscale('log')
plt.grid()
plt.xlabel("R", fontsize = 20)
plt.ylabel("G(R)", fontsize = 20)
plt.title("Two point correlation function as a function of lattice spacing", fontsize = 20)
plt.plot(x, y, marker = "^", color = "red", markersize = 10, linewidth = 1)
plt.errorbar(x, y, stdGJK, color = "green",capsize = 10)
plt.savefig(path + '/plots/corr_log', facecolor='w')
plt.close()

def scrivi_su_file(vettore1, vettore2, vettore3, nome_file):
    with open(nome_file, 'w') as file_output:
        for valore1, valore2, valore3 in zip(vettore1, vettore2, vettore3):
            riga = f"{valore1}\t{valore2}\t{valore3}\n"  
            file_output.write(riga)

vettore1 = [i for i in range(R_corr)]
vettore2 = meanGJK
vettore3 = stdGJK

nome_file = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + runName +"/data/output.txt"
scrivi_su_file(vettore1, vettore2, vettore3, nome_file)
np.savetxt("/home/anegro99/Documents/thesis/analysis/data/correlator/" + runName +"/data/covariance_matrix.txt", sigma)
