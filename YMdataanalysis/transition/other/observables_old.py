from pseudo_header import *

# parameters to be set by hand

L = int(sys.argv[2])
S_dim = 2

binTrP = [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000]
binchi = [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]
binbinder = [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000]

################################

runName = sys.argv[1]
path = "/home/anegro99/Documents/thesis/analysis/data/transition/" + runName 

meanTrPJK = list()
stdTrPJK = list()
meanchiJK = list()
stdchiJK = list()
meanbinderJK = list()
stdbinderJK = list()

sorted_names = sorted(os.listdir(path + '/data/'), key=lambda x: float(x.split('_')[1].split('.dat')[0]))

for count, filename in enumerate(sorted_names):

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
    
    TrP = (ReTrP**2 + ImTrP**2)**(0.5)

    # blocking for primary observables

    TrPblocked = list()

    for i in range(len(TrP)//binTrP[count]):
        TrPblocked.append(np.mean(TrP[i*binTrP[count]:(binTrP[count]*(i+1)-1)]))
    if TrP[(binTrP[count]*(i+1)):].size != 0:
        TrPblocked.append(np.mean(TrP[(binTrP[count]*(i+1)):]))

    tmp = [0] * (len(TrPblocked))
    
    TrP_obs = [0] * (len(TrPblocked) + 1)

    for i in range(len(TrPblocked)):
        tmp = TrPblocked.copy()

        tmp.remove(tmp[i])
        
        TrP_obs[i] = np.mean(tmp)

    TrP_obs[-1] = np.mean(TrPblocked)

    meanTrPJK.append(np.mean(TrP_obs))

    for j in range(len(TrPblocked)):
        if j==0:
            tmpTrP = (meanTrPJK[count]-TrP_obs[j])**2
        else:
            tmpTrP += (meanTrPJK[count]-TrP_obs[j])**2

    stdTrPJK.append(np.sqrt((tmpTrP*(len(TrPblocked)-1)/(len(TrPblocked)))))

    # secondary observables

    TrP2 = TrP**2
    TrP4 = TrP2**2

    #chi

    TrPblocked = list()
    TrP2blocked = list()

    for i in range(len(TrP)//binchi[count]):
        TrPblocked.append(np.mean(TrP[i*binchi[count]:(binchi[count]*(i+1)-1)]))
        TrP2blocked.append(np.mean(TrP2[i*binchi[count]:(binchi[count]*(i+1)-1)]))
    if TrP[(binchi[count]*(i+1)):].size != 0:
        TrPblocked.append(np.mean(TrP[(binchi[count]*(i+1)):]))
        TrP2blocked.append(np.mean(TrP2[(binchi[count]*(i+1)):]))

    tmp = [0] * (len(TrPblocked))
    tmp2 = [0] * (len(TrP2blocked))  

    chi = [0] * (len(TrPblocked) + 1)

    for i in range(len(TrPblocked)):
        tmp = TrPblocked.copy()
        tmp2 = TrP2blocked.copy()

        tmp.remove(tmp[i])
        tmp2.remove(tmp2[i])

        chi[i] = (np.mean(tmp2)-np.mean(tmp)**2)*(L**(S_dim))

    chi[-1] = (np.mean(TrP2blocked)-np.mean(TrPblocked)**2)*(L**(S_dim))

    meanchiJK.append(np.mean(chi))

    for j in range(len(TrPblocked)):
        if j==0:
            tmpchi = (meanchiJK[count]-chi[j])**2
        else:
            tmpchi += (meanchiJK[count]-chi[j])**2

    stdchiJK.append(np.sqrt((tmpchi*(len(TrPblocked)-1)/(len(TrPblocked)))))

    # binder

    TrP2blocked = list()
    TrP4blocked = list()

    for i in range(len(TrP2)//binbinder[count]):
        TrP2blocked.append(np.mean(TrP2[i*binbinder[count]:(binbinder[count]*(i+1)-1)]))
        TrP4blocked.append(np.mean(TrP4[i*binbinder[count]:(binbinder[count]*(i+1)-1)]))
    if TrP2[(binbinder[count]*(i+1)):].size != 0:
        TrP2blocked.append(np.mean(TrP2[(binbinder[count]*(i+1)):]))
        TrP4blocked.append(np.mean(TrP4[(binbinder[count]*(i+1)):]))

    tmp2 = [0] * (len(TrP2blocked))
    tmp4 = [0] * (len(TrP4blocked))  

    binder = [0] * (len(TrP2blocked) + 1)

    for i in range(len(TrP2blocked)):
        tmp2 = TrP2blocked.copy()
        tmp4 = TrP4blocked.copy()

        tmp2.remove(tmp2[i])
        tmp4.remove(tmp4[i])

        binder[i] = np.mean(tmp4)/(np.mean(tmp2))**2

    binder[-1] = np.mean(TrP4blocked)/(np.mean(TrP2blocked))**2

    meanbinderJK.append(np.mean(binder))

    for j in range(len(TrP2blocked)):
        if j==0:
            tmpbinder = (meanbinderJK[count]-binder[j])**2
        else:
            tmpbinder += (meanbinderJK[count]-binder[j])**2

    stdbinderJK.append(np.sqrt((tmpbinder*(len(TrP2blocked)-1)/(len(TrP2blocked)))))

TrP = meanTrPJK
s_TrP = stdTrPJK
chi = meanchiJK
s_chi = stdchiJK
binder = meanbinderJK
s_binder = stdbinderJK

observables = [TrP, s_TrP, chi, s_chi, binder, s_binder]

file_prefix = list()
for file_name in sorted_names:
    file_prefix.append(float(file_name.split("_")[1].split(".dat")[0]))

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

try:
    os.remove(path + '/' + runName + '.csv')
except:
    pass

file = open(path + '/' + runName + '.csv', "a")
for count, h in enumerate(file_prefix):
    file.write(f"{h} {TrP[count]} {s_TrP[count]} {chi[count]} {s_chi[count]} {binder[count]} {s_binder[count]}\n")
file.close()