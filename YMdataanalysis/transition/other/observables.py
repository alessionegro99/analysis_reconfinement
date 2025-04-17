from pseudo_header import *

runName = sys.argv[1]
L = int(sys.argv[2])
binsize = int(sys.argv[3])

path = "/home/anegro99/Documents/thesis/analysis/data/transition/" + runName
S_dim = 2

meanTrPJK = list()
stdTrPJK = list()
meanchiJK = list()
stdchiJK = list()
meanbinderJK = list()
stdbinderJK = list()

sorted_names = sorted(os.listdir(path + '/data/'), key=lambda x: float(x.split('_')[1].split('.dat')[0]))

for count, filename in enumerate(sorted_names):
    data = pd.read_csv(path + '/data/' + filename, sep=' ', header=None)
    df = data.loc[:,[2,3]]
    df[4] = (df[2]**2 + df[3]**2)**(1/2)
    df[5] = df[4]**2
    df[6] = df[4]**4

    TrPblocked = list()
    TrP2blocked = list()
    TrP4blocked = list()

    for i in range(len(df.index)//binsize):
        TrPblocked.append(df[4].iloc[i*binsize:(binsize*(i+1)-1)].mean())
        TrP2blocked.append(df[5].iloc[i*binsize:(binsize*(i+1)-1)].mean())
        TrP4blocked.append(df[6].iloc[i*binsize:(binsize*(i+1)-1)].mean())
    
    tmp = [0] * (len(df.index)//binsize)
    tmp2 = [0] * (len(df.index)//binsize)
    tmp4 = [0] * (len(df.index)//binsize)
    
    TrP = [0] * (len(df.index)//binsize + 1)
    chi = [0] * (len(df.index)//binsize + 1)
    binder = [0] * (len(df.index)//binsize + 1)
    
    for i in range(len(df.index)//binsize):
        tmp = TrPblocked.copy()
        tmp2 = TrP2blocked.copy()
        tmp4 = TrP4blocked.copy()

        tmp.remove(tmp[i])
        tmp2.remove(tmp2[i])
        tmp4.remove(tmp4[i])

        TrP[i] = np.mean(tmp)
        chi[i] = (np.mean(tmp2)-np.mean(tmp)**2)*(L**(S_dim))
        binder[i] = np.mean(tmp4)/(np.mean(tmp2))**2
    
    TrP[len(df.index)//binsize] = np.mean(TrPblocked)   
    chi[len(df.index)//binsize] = (np.mean(TrP2blocked)-np.mean(TrPblocked)**2)*(L**(S_dim))
    binder[len(df.index)//binsize] = np.mean(TrP4blocked)/(np.mean(TrP2blocked))**2
    
    meanTrPJK.append(np.mean(TrP))
    meanchiJK.append(np.mean(chi))
    meanbinderJK.append(np.mean(binder))
    
    for j in range(len(df.index)//binsize):
        if j==0:
            tmpTrP = (meanTrPJK[count]-TrP[j])**2
            tmpchi = (meanchiJK[count]-chi[j])**2
            tmpbinder = (meanbinderJK[count]-binder[j])**2
        else:
            tmpTrP += (meanTrPJK[count]-TrP[j])**2
            tmpchi += (meanchiJK[count]-chi[j])**2
            tmpbinder += (meanbinderJK[count]-binder[j])**2

    stdTrPJK.append(np.sqrt((tmpTrP*(len(df.index)//binsize-1)/(len(df.index)//binsize))))
    stdchiJK.append(np.sqrt((tmpchi*(len(df.index)//binsize-1)/(len(df.index)//binsize))))
    stdbinderJK.append(np.sqrt(tmpbinder*(len(df.index)//binsize-1)/(len(df.index)//binsize)))

# saving results in a file

TrP = meanTrPJK
s_TrP = stdTrPJK
chi = meanchiJK
s_chi = stdchiJK
binder = meanbinderJK
s_binder = stdbinderJK

observables = [TrP, s_TrP, chi, s_chi, binder, s_binder]

try:
    os.remove(path + '/' + runName + '.csv')
except:
    pass
             
for obs in observables:
    file = open(path + '/' + runName + '.csv', "a")
    file.write(f"{obs}\n")
    file.close()

file_prefix = list()
for file_name in sorted_names:
    file_prefix.append(float(file_name.split("_")[1].split(".dat")[0]))

filer = path + '/' + runName + '.csv'
filew = path + '/' + runName + '_stripped.csv'

with open(filer ,'r') as infile, open(filew, 'w') as outfile:
    data = infile.read()
    data = data.replace(",", "")
    data = data.replace("[", "")
    data = data.replace("]", "")
    outfile.write(data)

os.rename(filew, filer)

x = file_prefix

# |TrP| plot

y = meanTrPJK
plt.grid()
plt.xlabel("h", fontsize=20)
plt.ylabel("|TrP|", fontsize=20)
plt.title('|TrP| plot JK', fontsize=20)
plt.plot(x, y, marker = "o", markersize = 10, linewidth = 1)
plt.errorbar(x, y, stdTrPJK, capsize = 10)
plt.savefig(path + '/plots/observables/TrP', facecolor='w')
plt.close()

#Susceptibility plot

y = meanchiJK
plt.grid()
plt.xlabel('h', fontsize=20)
plt.ylabel('$\chi$', fontsize=20)
plt.title('Susceptibility plot JK', fontsize=20)
plt.plot(x, y, marker = "o", markersize = 10, linewidth = 1)
plt.errorbar(x,y,stdchiJK, capsize = 10)
plt.savefig(path + '/plots/observables/Susceptibility', facecolor='w')
plt.close()

#Binder's cumulant plot

y = meanbinderJK
plt.grid()
plt.xlabel('h', fontsize=20)
plt.ylabel('Q', fontsize=20)
plt.title('Binder cumulant plot JK', fontsize=20)
plt.plot(x, y, marker = "o", markersize = 10, linewidth = 0.5)
plt.errorbar(x,y,stdbinderJK, capsize = 5)
plt.savefig(path + '/plots/observables/Binder', facecolor='w')
plt.close()


