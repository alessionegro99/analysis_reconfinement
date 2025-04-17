from pseudo_header import *

directory_path = "/home/anegro99/Documents/thesis/analysis/"

hpc = np.array([0.00429, 0.00435, 0.00425, 0.00414, 0.00415, 0.00405])
shpc = np.array([0.00004, 0.00005, 0.00003, 0.00002, 0.00002, 0.00002])
Ns = np.array([30, 40, 50, 60, 72, 96])

colors = ["orange", "red", "magenta", "brown"]

plt.xlabel('$N_s$')
plt.ylabel('$h_{pc}$')
plt.title('$h_{pc}$ as a function of the spatial lattice size $N_s$')

for count, colore in enumerate(colors):
    Nsplot = np.linspace(Ns[count:], Ns[-1], 100)
    p, cov = curve_fit(nu, Ns[count:], hpc[count:], sigma = shpc[count:], absolute_sigma = True, maxfev = 5000)
    plt.plot(Nsplot, nu(Nsplot, p[0], p[1]), color = colore, linewidth = 2)
    for i in range(len(p)):
        print(str(p[i]) + "(" + str(np.sqrt(cov[i][i])) + ")")
    if count <4:
        print(rchisq(nu(Ns[count:], p[0], p[1]), hpc[count:], shpc[count:],len(Ns[count:])-len(p)))
    print("\n")

plt.plot(Ns, hpc, color = "purple", marker = ".", markersize = 5, linestyle = "None", label = "$h_{pc}$")
plt.errorbar(Ns, hpc, shpc, color = "purple", capsize = 5, capthick = 2, linestyle = "None")
plt.legend(markerscale = 3, bbox_to_anchor = (1,1))
plt.savefig(directory_path + "plots/transition/hpcFSSising.png", facecolor='w')
plt.close()

