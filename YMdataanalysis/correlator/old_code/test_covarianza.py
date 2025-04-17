from re import S
from pseudo_header import *

runName = sys.argv[1]
binsize = int(sys.argv[2])
#NBOOTSTRAP = int(sys.argv[3])

path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + runName

# Creating nameList

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


# covariance matrix sigma_11
GK1_centered = df[1]-np.mean(df[1])

GK1sq_centered = GK1_centered*GK1_centered

print(df[1])
print("\n")
print(GK1_centered)
print("\n")
print(GK1sq_centered)

blocks = []

for j in range (len(GK1sq_centered)//binsize):
    blocks.append(np.mean(GK1sq_centered[j*binsize:(j+1)*binsize:1]))

sigma11 = np.sqrt(np.mean(blocks))

print("JK result:")
print(stdGJK[1])
print("Matrice di covarianza:")
print(sigma11)
print(np.sqrt(np.var(df[1])/len(df[1])))

#invece che calcolare l'equivalente della devstd della media con jackknife posso fare l'equivalente della deviazione standard mean(x^2)-meanx^2 calcolato con bootstrap
#moltiplicare  per il numero di bin l'errore