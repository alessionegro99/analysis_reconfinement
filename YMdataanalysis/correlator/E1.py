from pseudo_header import *

directory_path = "/home/anegro99/Documents/thesis/analysis/data/correlator/"

plt.xlabel("$r_{min}$")
plt.ylabel("$E_1$")
plt.title("$E_1$ as a function of $r_{min}$")

filenames = []
Nt = []

for filename in os.listdir(directory_path):
    components = filename.split('_')
    if float(components[4]) == 0.006:
        filenames.append(filename)
        Nt.append(int(components[2]))

combined_arrays = list(zip(filenames, Nt))
sorted_combined_arrays = sorted(combined_arrays, key=lambda x: x[1])

filenames_sorted, Nt_sorted = zip(*sorted_combined_arrays)

RGB = ["purple", "red", "blue", "magenta", "brown", "green"]

for count,filename in enumerate(filenames_sorted[3:]):
    components = filename.split('_')
    # Extract the values for R, Nt, Ns, and h from the components
    R = int(components[1])
    Nt = int(components[2])
    Ns = int(components[3])
    h = float(components[4])

    with open("/home/anegro99/Documents/thesis/analysis/data/correlator/" + filename + "/data/fitparams.dat", 'r') as file:
        lines = file.readlines()
        for it, line in enumerate(lines):
            if it  == 15:
                values = line.split()
                a = float(values[1])
                E0 = float(values[3])

    G_BS = []
    sG_BS = []

    r = np.arange(1,R)
    G_BS = np.load(directory_path + filename + "/data/means.npy")
    sG_BS = np.load(directory_path + filename + "/data/errs.npy")

    G = np.mean(G_BS, axis = 0)[1:] - K0sym(r, a, E0)
    sG = np.mean(sG_BS, axis = 0)[1:]

    for countz, z in enumerate(abs(G/sG)):
        if abs(z)<1.00:
            break
    end = countz

    ri = []
    rf = []
    b = []
    sb = []
    E1 = []
    sE1 = []

    for i in range(0, end-2):
        p_K1, cov_K1 = curve_fit(K1sym, r[i:end], G[i:end], sigma = sG[i:end], absolute_sigma = True)
        ri.append(r[i])
        rf.append(r[end])
        b.append(p_K1[0])
        sb.append(cov_K1[0][0])
        E1.append(p_K1[1])
        sE1.append(cov_K1[1][1])

    with open(directory_path + filename +"/data/fitE1.txt", "w") as outputfile:
        for xi, xf, p0, sp0, p1, sp1 in zip(ri, rf, b, sb, E1, sE1):
            riga = f"{xi}\t{xf}\t{p0}\t{sp0}\t{p1}\t{sp1}\n" 
            outputfile.write(riga)
    
    plt.plot(ri, E1, marker = ".", markersize = 15, color = RGB[count],linestyle = 'None', label = "$N_t$ = " + str(Nt))
    plt.errorbar(ri, E1, sE1, color = RGB[count], linewidth = 2.5, linestyle = 'None', capthick = 2, capsize = 15)

plt.legend(bbox_to_anchor=(1, 1))        
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/E1Nt.png", facecolor = 'w')     
plt.close()