from pseudo_header import *

directory_path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" 

# plot and fit for E_0(Nt, h=0.006)

param_line = 15

Ntarr = []
E0Nt = []
sE0Nt = []

for filename in os.listdir(directory_path):
    components = filename.split('_')
    R = int(components[1])
    Nt = int(components[2])
    Ns = int(components[3])
    h = float(components[4])

    if h==0.006 and Nt>7:
        with open(directory_path + filename + "/data/fitparams.dat", 'r') as file:
            line = file.readlines()[param_line]
            values = line.split()
            Ntarr.append(Nt)
            E0Nt.append(float(values[3]))
            sE0Nt.append(float(values[4]))

combined_arrays = list(zip(Ntarr, E0Nt, sE0Nt))
sorted_combined_arrays = sorted(combined_arrays, key=lambda x: x[0])

Ntarr_sorted, E0Nt_sorted, sE0Nt_sorted = zip(*sorted_combined_arrays)

# NG string fit

start = 0

x1 = np.array(Ntarr_sorted[start:])
x1plot = np.linspace(x1[0],x1[-1], 100)
y1 = np.array(E0Nt_sorted[start:])
sy1 = np.array(sE0Nt_sorted[start:])

p, cov = curve_fit(NGNt, x1, y1, sigma = sy1, absolute_sigma = True)

print("Nambu goto string:")
print("chi^2/nu:")
print(rchisq(NGNt(x1, p[0]), y1, sy1, len(x1)-len(p)))
print("Parameters")
for i, parameter in enumerate(p):
    print(str(parameter)+"(" + str(np.sqrt(cov[i][i])) + ")")
print("\n")

pmod, covmod = curve_fit(NGNtmod, x1, y1, sigma = sy1, absolute_sigma = True)

print("Nambu goto mod string:")
print("chi^2/nu:")
print(rchisq(NGNtmod(x1, pmod[0], pmod[1], pmod[2]), y1, sy1, len(x1)-len(pmod)))
print("Parameters")
for i, parameter in enumerate(pmod):
    print(str(parameter)+"(" + str(np.sqrt(covmod[i][i])) + ")")
print("\n")

starta = 2

x1a = np.array(Ntarr_sorted[starta:])
x1aplot = np.linspace(x1a[0],x1a[-1], 100)
y1a = np.array(E0Nt_sorted[starta:])
sy1a = np.array(sE0Nt_sorted[starta:])

pa, cova = curve_fit(linear, x1a, y1a, sigma = sy1a, absolute_sigma = True)

print("Area law string:")
print("chi^2/nu:")
print(rchisq(linear(x1a, pa[0], pa[1]), y1a, sy1a, len(x1a)-len(pa)))
print("Parameters")
for i, parameter in enumerate(pa):
    print(str(parameter)+"(" + str(np.sqrt(cova[i][i])) + ")")
print("\n")

plt.xlabel("$N_t$")
plt.ylabel("$E_0(N_t, h=0.006)$")
plt.title("$E_0$ as a function of $N_t$ at fixed $h=0.006$")
plt.plot(Ntarr, E0Nt, marker = ".", color = "purple", markersize = 10, linestyle = 'None', label = "$E_0(N_t, h=0.006)$")
plt.errorbar(Ntarr, E0Nt, sE0Nt, linestyle = 'None',color = "purple", capsize = 10, capthick = 2)

#plt.plot(x1plot, NGNt(x1plot, p[0]), color = "orange", linewidth = 2, label = "$E_0(N_t)$ Nambu-Goto")
#plt.plot(x1plot, NGNtmod(x1plot, pmod[0], pmod[1], pmod[2]), color = "red", linewidth = 2, label = "$E_0(N_t)$ 3 parameters")
plt.plot(x1aplot, linear(x1aplot, pa[0], pa[1]), color = "green", linewidth = 2, label = "Area law")

plt.legend()
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/correlator/E0(Nt,006)_NG.png", facecolor = 'w')                
plt.close()

# rigid string fit

start = 1

x1 = np.array(Ntarr_sorted[start:])
x1plot = np.linspace(x1[0],x1[-1], 100)
y1 = np.array(E0Nt_sorted[start:])
sy1 = np.array(sE0Nt_sorted[start:])

lower_bounds = [0.0, -np.inf]
upper_bounds = [np.inf, np.inf]
bounds = (lower_bounds, upper_bounds)

p, cov = curve_fit(E0Makeenko, x1, y1, sigma = sy1, absolute_sigma = True, bounds = bounds, p0 = [0.8, 0.001] , maxfev = 5000)

print("Makeenko rigid string:")

print("chi^2/nu:")
print(rchisq(E0Makeenko(x1, p[0], p[1]), y1, sy1, len(x1)-len(p)))
print("Parameters")
for i, parameter in enumerate(p):
    print(str(parameter)+"(" + str(np.sqrt(cov[i][i])) + ")")
print("\n")


plt.xlabel("$N_t$")
plt.ylabel("$E_0(N_t, h=0.007)$")
plt.title("$E_0$ as a function of $N_t$ at fixed $h=0.007$")
plt.plot(Ntarr, E0Nt, marker = ".", color = "purple", markersize = 10, linestyle = 'None', label = "$E0(Nt, h=0.007)$")
plt.errorbar(Ntarr, E0Nt, sE0Nt, linestyle = 'None',color = "purple", capsize = 10, capthick = 2)

plt.plot(x1plot, E0Makeenko(x1plot, p[0], p[1]), color = "orange", linewidth = 2, label = "$E_0(N_t)$ rigid string")

plt.legend()
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/correlator/E0(Nt,007)_RS.png", facecolor = 'w')                
plt.close()

# plot and fit for E_0(Nt = 10, h)

harr = []
E0h = []
sE0h = []

for filename in os.listdir(directory_path):
    components = filename.split('_')
    R = int(components[1])
    Nt = int(components[2])
    Ns = int(components[3])
    h = float(components[4])

    if Nt == 10 and h>0.0040:
        with open(directory_path + filename + "/data/fitparams.dat", 'r') as file:
            line = file.readlines()[14]
            values = line.split()
            harr.append(h)
            E0h.append(float(values[3]))
            sE0h.append(float(values[4]))

combined_arrays = list(zip(harr, E0h, sE0h))
sorted_combined_arrays = sorted(combined_arrays, key=lambda x: x[0])

harr_sorted, E0h_sorted, sE0h_sorted = zip(*sorted_combined_arrays)

start = 0

x1 = np.array(harr_sorted[start:])
x1plot = np.linspace(x1[0],x1[-1], 100)
y1 = np.array(E0h_sorted[start:])
sy1 = np.array(sE0h_sorted[start:])

p, cov = curve_fit(linear, x1, y1, sigma = sy1, absolute_sigma = True)

print(rchisq(linear(x1, p[0], p[1]), y1, sy1, len(x1)-len(p)))

for i, parameter in enumerate(p):
    print(parameter)
    print(np.sqrt(cov[i][i]))

plt.xlabel("$h$")
plt.ylabel("$E_0(N_t=10, h)$")
plt.title("$E_0$ as a function of $h$ at fixed $N_t$=10")
plt.plot(harr, E0h, marker = ".", color = "purple", markersize = 10, linestyle = 'None', label = "$E0(N_t=10, h)$")
plt.errorbar(harr, E0h, sE0h, linestyle = 'None',color = "purple", capsize = 10, capthick = 2)

#plt.plot(x1plot, linear(x1plot, p[0], p[1]), color = "orange", linewidth = 2, label = "$E_0(h) = a + b*h$")


plt.legend()
plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/correlator/E0(10,h).png", facecolor = 'w')                
plt.close()
