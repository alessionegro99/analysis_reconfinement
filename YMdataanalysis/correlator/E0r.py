from pseudo_header import *

# plots the values of E0 for different Nt as a function of the minimum fit range, in order to check fit stability

Nt = np.array([7, 8, 9, 10, 11, 12, 13, 14])
color = ["greY", "purple", "red", "black", "magenta", "orange", "blue", "brown"]

E0r = []
sE0r = []

for i in range(len(Nt)):
    E0r.append([])
    sE0r.append([])
    with open("/home/anegro99/Documents/thesis/analysis/data/correlator/corr_24_" + str(Nt[i]) + "_96_0.007/data/fitparams.dat", 'r') as file:
        lines = file.readlines()
        for line in lines:
            values = line.split()
            E0r[i].append(float(values[3]))
            sE0r[i].append(float(values[4]))

for y, sy, t, c in zip(E0r, sE0r, Nt, color):

    x = np.arange(1,20)

    plt.xlabel("$r_{min}$")
    plt.ylabel("$E_0(N_t,h = 0.007)$")
    plt.title("$E_0(N_t, h = 0.007)$ as a function of $r_{min}$")
    plt.plot(x, y, marker = ".", color = c, markersize = 10, linestyle = 'None', label = "$N_t=$" + str(t))
    plt.errorbar(x, y, sy, linestyle = 'None', color = c, capsize = 10, capthick = 2)
    plt.legend(bbox_to_anchor = (1,1), markerscale = 3)
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/correlator/E0Nt(rmin)007", facecolor = 'w')
plt.close()

# plots the values of E0 for different h as a function of the minimum fit range, in order to check fit stability

h = np.array([0.0045, 0.00475, 0.005, 0.00525, 0.0055, 0.00575, 0.006])
color = ["purple", "red", "black", "magenta", "blue", "violet", "brown"]

E0r = []
sE0r = []

for i in range(len(h)):
    E0r.append([])
    sE0r.append([])
    with open("/home/anegro99/Documents/thesis/analysis/data/correlator/corr_24_10_96_" + str(h[i]) + "/data/fitparams.dat", 'r') as file:
        lines = file.readlines()
        for line in lines:
            values = line.split()
            E0r[i].append(float(values[3]))
            sE0r[i].append(float(values[4]))

for y, sy, t, c in zip(E0r, sE0r, h, color):

    x = np.arange(1,20)

    plt.xlabel("$r_{min}$")
    plt.ylabel("$E_0(N_t = 10,h)$")
    plt.title("$E_0(N_t = 10, h)$ as a function of $r_{min}$")
    plt.plot(x, y, marker = ".", color = c, markersize = 10, linestyle = 'None', label = "$h =$" + str(t))
    plt.errorbar(x, y, sy, linestyle = 'None', color = c, capsize = 10, capthick = 2)
    plt.legend(bbox_to_anchor = (1,1), markerscale = 3)
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/E0h(rmin)", facecolor = 'w')
plt.close()
