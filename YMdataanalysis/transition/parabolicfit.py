from pseudo_header import *

directory_path = "/home/anegro99/Documents/thesis/analysis/data/transition/"

Ns, h, P, sP, chi, schi, Q, sQ = [], [], [], [], [], [], [], []

files = os.listdir(directory_path)

files.remove("tran_10_108_23.3805")
files.remove("tran_10_120_23.3805")

for count, filename in enumerate(files):
    components = filename.split("_")
    Ns.append(components[2])

    with open(directory_path + filename + "/" + filename + ".csv", "r") as file:
        lines = file.readlines()
        h.append([])
        P.append([])
        sP.append([])
        chi.append([])
        schi.append([])
        Q.append([])
        sQ.append([])

        for line in lines:
            values = line.split()
            h[count].append(float(values[0]))
            P[count].append(float(values[1]))
            sP[count].append(float(values[2]))
            chi[count].append(float(values[3]))
            schi[count].append(float(values[4]))
            Q[count].append(float(values[5]))
            sQ[count].append(float(values[6]))


RGB = [
    (0.2, 0.2, 0.8),  # Dark Blue
    (0.8, 0.2, 0.2),  # Dark Red
    (0.2, 0.8, 0.2),  # Dark Green
    (0.8, 0.8, 0.2),  # Yellow
    (0.8, 0.2, 0.8),  # Magenta
    (0.8, 0.5, 0.2)   # Orange
]
combined_arrays = list(zip(Ns, h, P, sP, chi, schi, Q, sQ))
sorted_combined_arrays = sorted(combined_arrays, key=lambda x: x[0])

Ns, h, P, sP, chi, schi, Q, sQ= zip(*sorted_combined_arrays)

fitstart = [3, 3, 3, 0, 1, 0]
fitend = [7, 7, 7, 5, 5, 4]

plt.xlabel('$h$')
plt.ylabel('$\chi$')
plt.title('Susceptibility as a function of $h$')
for i, f, s, c, x, y, sy in zip(fitstart, fitend, Ns, RGB, h, chi, schi):

    p, cov = curve_fit(quadratic, x[i:f], y[i:f], sigma = sy[i:f], absolute_sigma = sy[i:f], p0 = [int(s), -10000000, 0.004])
    chinu = rchisq(quadratic(x[i:f], p[0], p[1], p[2]), y[i:f], sy[i:f], len(x[i:f])-3)

    xplot = np.linspace(x[i], x[f-1], 100)
    for count, val in enumerate(p):
        print(str(val) + "(" + str(np.sqrt(cov[count][count])) + ")" )
    print(chinu)
    print("\n")

    plt.plot(x, y, marker = "o", color = c, markersize = 5, label = "$N_s$ =" + s)
    plt.plot(xplot, quadratic(xplot, p[0], p[1], p[2]), color = "red", linewidth = 2) 
    plt.errorbar(x, y, sy, capsize = 5, capthick = 1, color = c)
plt.legend(markerscale = 3, bbox_to_anchor = (1,1))
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/transition/chiNs_fit.png", facecolor = "w")
plt.close()