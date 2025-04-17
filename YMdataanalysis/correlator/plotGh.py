from pseudo_header import *

directory_path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" 

file_list = os.listdir(directory_path)

filenames = []
h = []

for filename in os.listdir(directory_path):
    components = filename.split('_')
    if int(components[2]) == 10 and float(components[4])>0.004:
        filenames.append(filename)
        h.append(float(components[4]))

combined_arrays = list(zip(filenames, h))
sorted_combined_arrays = sorted(combined_arrays, key=lambda x: x[1])

filenames_sorted, h_sorted = zip(*sorted_combined_arrays)

x = np.arange(int(components[1]))

colors = [
    #(0.0, 0.0, 0.0),   # Black
    #(1.0, 0.0, 0.0),   # Red
    #(0.0, 1.0, 0.0),   # Green
    (0.0, 0.0, 1.0),   # Blue
    (0.5, 0.0, 0.5),   # Dark Purple
    (1.0, 0.0, 1.0),   # Magenta
    (0.0, 1.0, 1.0),   # Cyan
    (0.5, 0.5, 0.5),   # Gray
    (1.0, 0.5, 0.0),   # Orange
    (0.0, 1.0, 0.5)    # Teal
]

for count, filename in enumerate(filenames_sorted):
    G = np.mean(np.load(directory_path + filename +"/data/means.npy"), axis = 0)
    sG = np.mean(np.load(directory_path + filename +"/data/errs.npy"), axis = 0)
    plt.xlabel("$r$")
    plt.ylabel("$G(r)$")
    plt.title("Two point Polyakov loop correlation function")
    plt.plot(x, G, marker = ".", markersize = 15, linestyle = "None", label = "h = " + str(h_sorted[count]), color = colors[count])
    plt.errorbar(x, G, sG, capsize = 10, capthick = 2, linestyle = "None", color = colors[count])

plt.legend(markerscale = 2, bbox_to_anchor = (1,1))
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/correlator/Gh.png", facecolor = "w")
plt.close()