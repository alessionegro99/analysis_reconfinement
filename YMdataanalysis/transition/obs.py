from pseudo_header import *

runName = sys.argv[1]
blockTrP = int(sys.argv[2])
blockchi = int(sys.argv[3])
blockQ = int(sys.argv[4])

path = "/home/anegro99/Documents/thesis/analysis/data/transition/" + runName 

components = runName.split('_')
Ns = int(components[2])

NBS = 200

TrP = []
sTrP = []
chi = []
schi = []
Q = []
sQ = []

sorted_names = sorted(os.listdir(path + '/data/'), key=lambda x: float(x.split('_')[1].split('.dat')[0]))

for count, filename in tqdm(enumerate(sorted_names)):

    file_path = path + "/data/" + filename 

    column1_index = 2
    column2_index = 3

    ReTrP = []
    ImTrP = []

    with open(file_path, 'r') as datfile:
        for line in datfile:
            
            columns = line.split()  
            
            if len(columns) > max(column1_index, column2_index):
                ReTrP.append(float(columns[column1_index]))
                ImTrP.append(float(columns[column2_index]))

    ReTrP = np.array(ReTrP)
    ImTrP = np.array(ImTrP)
    
    absTrP = (ReTrP**2 + ImTrP**2)**(0.5)
    absTrP2 = absTrP**2
    absTrP4 = absTrP**4

    # primary observables

    TrPblocks = np.mean(get_blocks(absTrP, blockTrP), axis = 1)
    nTrP = len(TrPblocks)

    TrP.append(np.mean(TrPblocks))
    sTrP.append(np.sqrt(np.var(TrPblocks, ddof = 1)/nTrP))

    # secondary observables

    TrP2blocks = np.mean(get_blocks(absTrP2, blockTrP), axis = 1)
    TrP4blocks = np.mean(get_blocks(absTrP4, blockTrP), axis = 1)

    TrPblocks_BS, TrP2blocks_BS = np.array(bootstrap2(TrPblocks, TrP2blocks, NBS))

    chi_BS = Ns**2*(np.mean(TrP2blocks_BS, axis = 1) - np.mean(TrPblocks_BS, axis = 1)**2)

    chi.append(np.mean(chi_BS))
    schi.append(np.std(chi_BS))

    TrP2blocks_BS, TrP4blocks_BS = np.array(bootstrap2(TrP2blocks, TrP4blocks, NBS))

    Q_BS = np.mean(TrP4blocks_BS, axis = 1)/np.mean(TrP2blocks_BS, axis = 1)**2 

    Q.append(np.mean(Q_BS))
    sQ.append(np.std(Q_BS))

h = []
for file_name in sorted_names:
    h.append(float(file_name.split("_")[1].split(".dat")[0]))

# plot of P

plt.xlabel("$h$")
plt.ylabel("P")
plt.title("Polyakov loop as a function of $h$")
plt.plot(h, TrP, marker = "o", markersize = 10, color = "purple", linestyle = "None")
plt.errorbar(h, TrP, sTrP, capsize = 10, capthick = 2, linestyle = "None", color = "purple")
plt.savefig(path + '/plots/observables/TrP', facecolor = 'w')
plt.close()

# plot of chi

plt.xlabel("$h$")
plt.ylabel("$\chi$")
plt.title("Susceptibility $\chi$ as a function of $h$")
plt.plot(h, chi, marker = "o", markersize = 10, color = "purple", linestyle = "None")
plt.errorbar(h, chi, schi, capsize = 10, capthick = 2, linestyle = "None", color = "purple")
plt.savefig(path + '/plots/observables/chi', facecolor = 'w')
plt.close()

# plot of Q

plt.xlabel("$h$")
plt.ylabel("$Q$")
plt.title("Binder's cumulant Q as a function of $h$")
plt.plot(h, Q, marker = "o", markersize = 10, color = "purple", linestyle = "None")
plt.errorbar(h, Q, sQ, capsize = 10, capthick = 2, linestyle = "None", color = "purple")
plt.savefig(path + '/plots/observables/Q', facecolor = 'w')
plt.close()

try:
    os.remove(path + '/' + runName + '.csv')
except:
    pass

with open(path + '/' + runName + '.csv', "w") as outputfile:
    for x, y1, sy1, y2, sy2, y3, sy3 in zip(h, TrP, sTrP, chi, schi, Q, sQ):
        riga = f"{x}\t{y1}\t{sy1}\t{y2}\t{sy2}\t{y3}\t{sy3}\n"
        outputfile.write(riga)
