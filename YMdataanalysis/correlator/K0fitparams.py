from pseudo_header import *

directory_path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" 

initial_fit = 1
final_fit = 20

for start in tqdm(range(initial_fit,final_fit)):
    for filename in os.listdir(directory_path):
        if filename != "corr_24_6_96_0.006":
            components = filename.split('_')
            R = int(components[1])
            Nt = int(components[2])
            Ns = int(components[3])
            h = float(components[4])

            G_BS = []
            sG_BS = []

            G_BS = np.load(directory_path + filename +"/data/means.npy")
            sG_BS = np.load(directory_path + filename +"/data/errs.npy")

            # fitting data with correlations

            r = np.arange(0,R)
            a_array = []
            E0_array = []
            chi_array = []

            for G, sG in zip(G_BS, sG_BS):
                x = np.array(r[start:])
                y = G[start:]
                sy = sG[start:]

                p_K0, cov_K0 = curve_fit(K0sym, x, y, sigma = sy, absolute_sigma = True, maxfev = 5000)
                a_array.append(p_K0[0])
                E0_array.append(p_K0[1])
                chi_array.append(rchisq(K0sym(x, p_K0[0], p_K0[1]), y, sy, len(x)-len(p_K0)))

            a = np.mean(a_array)
            sa = np.std(a_array)

            E0 = np.mean(E0_array)
            sE0 = np.std(E0_array)

            chi = np.mean(chi_array)

            if start == initial_fit:
                if os.path.exists(directory_path + filename +"/data/fitparams.dat"):
                    os.remove(directory_path + filename +"/data/fitparams.dat")

            with open(directory_path + filename +"/data/fitparams.dat", "a") as outputfile:
                riga = f"{start}\t{a}\t{sa}\t{E0}\t{sE0}\t{chi}\n" 
                outputfile.write(riga)


