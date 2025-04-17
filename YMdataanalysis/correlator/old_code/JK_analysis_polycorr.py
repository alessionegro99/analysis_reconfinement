from pseudo_header import *

# Parameters to change everytime ###########

NFILES = 48

L = 96
S_dim = 2

KBINNING_VEC = [1000, 1000, 1000]
THERM = 10000

runName = 'run_tracedef_1605_2'

##############################################

HTRDFMAX = HTRDFMIN + DHTRDF*(NFILES-1)
mainPath = homeDir + '/Documents/thesis/simulation_analysis/simulation_data/' + runName
x_range = np.linspace(HTRDFMIN, HTRDFMAX, NFILES).tolist()

# Creating nameList

nameList = list()

for i in range(NFILES):
    aux = x_range[i]
    nameList.append(mainPath + "/data/dati_" + "%.6f" % aux +".dat")

# Jackknife analysis

meanTrPJK = list()
stdTrPJK = list()
meanchiJK = list()
stdchiJK = list()
meanbinderJK = list()
stdbinderJK = list()

for datiIndex in range(NFILES):
    data = pd.read_csv(nameList[datiIndex], sep=' ', header=None)
    df = data.loc[:,[2,3]]
    df[4] = (df[2]**2 + df[3]**2)**(1/2)
    df[5] = df[4]**2
    df[6] = df[4]**4

    #Dropping data according to thermalization computer time
    
    df.drop(index=df.index[:THERM], axis=0, inplace=True)
    
    #Binning implementation (different for different power of |TrP|)
    
    TrPblocked = list()
    TrP2blocked = list()
    TrP4blocked = list()
    
    #Bin size
    
    if datiIndex < (NFILES//2 + NFILES//4):
        KBINNING = KBINNING_VEC[0]
    else:
        KBINNING = KBINNING_VEC[1]


    for i in range(len(df.index)//KBINNING):
        TrPblocked.append(df[4].iloc[i*KBINNING:(KBINNING*(i+1))].mean())
        TrP2blocked.append(df[5].iloc[i*KBINNING:(KBINNING*(i+1))].mean())
        TrP4blocked.append(df[6].iloc[i*KBINNING:(KBINNING*(i+1))].mean())
    
    tmp = [0] * (len(df.index)//KBINNING)
    tmp2 = [0] * (len(df.index)//KBINNING)
    tmp4 = [0] * (len(df.index)//KBINNING)
    
    TrP = [0] * (len(df.index)//KBINNING+1)
    chi = [0] * (len(df.index)//KBINNING+1)
    binder = [0] * (len(df.index)//KBINNING+1)
    
    for i in range(len(df.index)//KBINNING):
        tmp = TrPblocked.copy()
        tmp2 = TrP2blocked.copy()
        tmp4 = TrP4blocked.copy()

        tmp.remove(tmp[i])
        tmp2.remove(tmp2[i])
        tmp4.remove(tmp4[i])

        TrP[i] = np.mean(tmp)
        chi[i] = (np.mean(tmp2)-np.mean(tmp)**2)*(L**(S_dim))
        binder[i] = np.mean(tmp4)/(np.mean(tmp2))**2
        
    TrPori = np.mean(TrPblocked)    
    chiori = (np.mean(TrP2blocked)-np.mean(TrPblocked)**2)*(L**(S_dim))
    binderori = np.mean(TrP4blocked)/(np.mean(TrP2blocked))**2
    
    TrP[len(df.index)//KBINNING] = TrPori
    chi[len(df.index)//KBINNING] = chiori
    binder[len(df.index)//KBINNING] = binderori
    
    meanTrPJK.append(np.mean(TrP))
    meanchiJK.append(np.mean(chi))
    meanbinderJK.append(np.mean(binder))
    
    for j in range(len(df.index)//KBINNING):
        if j==0:
            tmpTrP = (meanTrPJK[datiIndex]-TrP[j])**2
            tmpchi = (meanchiJK[datiIndex]-chi[j])**2
            tmpbinder = (meanbinderJK[datiIndex]-binder[j])**2
        else:
            tmpTrP += (meanTrPJK[datiIndex]-TrP[j])**2
            tmpchi += (meanchiJK[datiIndex]-chi[j])**2
            tmpbinder += (meanbinderJK[datiIndex]-binder[j])**2

    stdTrPJK.append(np.sqrt((tmpTrP*(len(df.index)//KBINNING-1)/(len(df.index)//KBINNING))))
    stdchiJK.append(np.sqrt((tmpchi*(len(df.index)//KBINNING-1)/(len(df.index)//KBINNING))))
    stdbinderJK.append(np.sqrt(tmpbinder*(len(df.index)//KBINNING-1)/(len(df.index)//KBINNING)))

# Plots

#|TrP| plot

plt.rcParams["figure.figsize"] = [15, 8]
plt.rcParams["figure.autolayout"] = True
x = x_range
y = meanTrPJK
plt.grid()
plt.xlabel("h", fontsize=12)
plt.ylabel("|TrP|", fontsize=12)
plt.title('|TrP| plot JK', fontsize=12)
plt.plot(x, y, marker = "o", markersize = 10, linewidth = 1)
plt.errorbar(x,y,stdTrPJK, capsize = 10)
plt.savefig(mainPath + '/plots/TrP_' + runName, facecolor='w')
plt.close()

#Susceptibility plot

plt.rcParams["figure.figsize"] = [15, 8]
plt.rcParams["figure.autolayout"] = True
x = x_range
y = meanchiJK
plt.grid()
plt.xlabel('h', fontsize=12)
plt.ylabel('$\chi$', fontsize=12)
plt.title('Susceptibility plot JK', fontsize=12)
plt.plot(x, y, marker = "o", markersize = 10, linewidth = 1)
plt.errorbar(x,y,stdchiJK, capsize = 10)
plt.savefig(mainPath + '/plots/Susceptibility_' + runName, facecolor='w')
plt.close()

#Binder's cumulant plot

plt.rcParams["figure.figsize"] = [15, 8]
plt.rcParams["figure.autolayout"] = True
x = x_range
y = meanbinderJK
plt.grid()
plt.xlabel('h', fontsize=12)
plt.ylabel('Q', fontsize=12)
plt.title('Binder cumulant plot JK', fontsize=12)
plt.plot(x, y, marker = "o", markersize = 10, linewidth = 0.5)
plt.errorbar(x,y,stdbinderJK, capsize = 5)
plt.savefig(mainPath + '/plots/Binder_' + runName, facecolor='w')
plt.close()

#Saving results in a file

TrP = meanTrPJK
s_TrP = stdTrPJK
chi = meanchiJK
s_chi = stdchiJK
binder = meanbinderJK
s_binder = stdbinderJK

observables = [TrP, s_TrP, chi, s_chi, binder, s_binder]
             
for obs in observables:
    file = open(mainPath + '/' + runName + '.csv', "a")
    file.write(f"{obs}\n")
    file.close()
