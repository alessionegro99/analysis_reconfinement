from pseudo_header import *

directory_path = "/home/anegro99/Documents/thesis/analysis/"

chimax = np.array([24.79, 43.2, 59.8, 77.1, 99.3, 147.4])
schimax = np.array([0.16, 0.4, 0.8, 0.5, 0.8, 1.3])
Ns = np.array([30, 40, 50, 60, 72, 96])

colors = ["orange", "red", "green", "brown"]

plt.xlabel('$N_s$')
plt.ylabel('$\chi_M$')
plt.title('$\chi_M$ as a function of the spatial lattice size $N_s$')

for count, colore in enumerate(colors):
    Nsplot = np.linspace(Ns[count:], Ns[-1], 100)
    p, cov = curve_fit(gammanu, Ns[count:], chimax[count:], sigma = schimax[count:], absolute_sigma = True)
    plt.plot(Nsplot, gammanu(Nsplot, p[0], p[1]), color = colore, linewidth = 2)
    for i in range(len(p)):
        print(str(p[i]) + "(" + str(np.sqrt(cov[i][i])) + ")")
    if count <4:
        print(rchisq(gammanu(Ns[count:], p[0], p[1]), chimax[count:], schimax[count:],len(Ns[count:])-len(p)))
    print("\n")

plt.plot(Ns, chimax, color = "purple", marker = ".", markersize = 5, linestyle = "None", label = "$\chi_M$")
plt.errorbar(Ns, chimax, schimax, color = "purple", capsize = 5, capthick = 2, linestyle = "None")
plt.legend(markerscale = 3)
plt.savefig(directory_path + "plots/transition/chimaxFSSising.png", facecolor='w')
plt.close()

