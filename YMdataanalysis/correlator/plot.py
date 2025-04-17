from pseudo_header import *

directory_path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" 

start_value = 15

G = []
sG = []

name_list = os.listdir(directory_path)
name_list.remove("corr_24_6_96_0.006")

for count, filename in enumerate(name_list):
        components = filename.split('_')
        R = int(components[1])
        Nt = int(components[2])
        Ns = int(components[3])
        h = float(components[4])

        with open("/home/anegro99/Documents/thesis/analysis/data/correlator/" + filename + "/data/fitparams.dat", 'r') as file:
            line = file.readlines()[start_value-1]
            values = line.split()
            rmin = float(values[0])
            a = float(values[1])
            sa = float(values[2])
            E0 = float(values[3])
            sE0 = float(values[4])

        r = np.arange(R)
        G.append(np.mean(np.load(directory_path + filename +"/data/means.npy"), axis = 0))
        sG.append(np.mean(np.load(directory_path + filename +"/data/errs.npy"), axis = 0))

        rplot = np.linspace(start_value,23,100)

        plt.xlabel("$r$")
        plt.ylabel("$G(r)$")
        plt.title("Two point Polyakov loop correlation function")
        plt.plot(r, G[count], marker = ".", color = "purple", markersize = 5, linestyle = 'None', label = "$G(r)$")
        plt.errorbar(r, G[count], sG[count], linestyle = 'None', capsize = 5, capthick = 2, color = "purple")
        plt.plot(rplot, K0(rplot, a, E0), color = "orange", linewidth = 2, label = "$aK_0(br)$")
        plt.legend(markerscale = 4)
        plt.savefig("/home/anegro99/Documents/thesis/analysis/data/correlator/" + filename + "/plots/aK0(br).png", facecolor = 'w')
                
        plt.close()

RGB = ["purple", "black", "red", "magenta", "green", "orange", "blue", "brown"]

filenames = []
Nt = []
G_tmp = []
sG_tmp = []

for count, filename in enumerate(name_list):
    components = filename.split('_')
    if float(components[4]) == 0.006:
        filenames.append(filename)
        Nt.append(int(components[2]))
        G_tmp.append(G[count])
        sG_tmp.append(sG[count])

combined_arrays = list(zip(filenames, Nt, G_tmp, sG_tmp))
sorted_combined_arrays = sorted(combined_arrays, key=lambda x: x[1])

filenames_sorted, Nt_sorted, G_sorted, sG_sorted = zip(*sorted_combined_arrays)

plt.xlabel("$r$")
plt.ylabel("$G(r)$")
plt.title("Two point Polyakov loop correlation function")
for count, filename in enumerate(filenames_sorted):
    if count >0:
        plt.plot(r, G_sorted[count], marker = ".", color = RGB[count], markersize = 5, linestyle = 'None', label = "Nt = " + str(Nt_sorted[count]))
        plt.errorbar(r, G_sorted[count], sG_sorted[count], linestyle = 'None', capsize = 5, capthick = 1, color = RGB[count])
        plt.legend(markerscale = 4, bbox_to_anchor = (1,1))
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/correlator/G(Nt)_007.png", facecolor = 'w')
plt.close()

