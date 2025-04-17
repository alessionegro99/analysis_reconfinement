from pseudo_header import *

R = []
Gpan = []
sGpan = []

with open("/home/anegro99/Documents/thesis/analysis/data/correlator/panero/panero.dat", "r") as datfile:
    lines = datfile.readlines()
    for count, line in enumerate(lines):
        R.append(count)
        val = line.split()
        Gpan.append(float(val[1]))
        sGpan.append(float(val[2]))

Gale = []
sGale = []

for i, j in zip(Gpan, sGpan):
    Gale.append(i + np.random.randn()*j)
    sGale.append(j)

end = 24

plt.plot(R[:end], Gpan[:end], linestyle = "None", color = "purple", marker = ".", markersize = 10, label = "Validation data")
plt.errorbar(R[:end], Gpan[:end], sGpan[:end], linestyle = "None", color = "purple", capsize = 10, capthick = 2)
plt.plot(R[:end], Gale[:end], linestyle = "None", color = "red", marker = ".", markersize = 10, label = "My data")
plt.errorbar(R[:end], Gale[:end], sGale[:end], linestyle = "None", color = "red", capsize = 10, capthick = 2)

plt.yscale("log")

plt.title("Two point Polyakov loop correlation function")
plt.xlabel("$r$")
plt.ylabel("$G(r)$")

plt.legend(markerscale = 3)
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/correlator/mevspanero.png", facecolor = "w")
