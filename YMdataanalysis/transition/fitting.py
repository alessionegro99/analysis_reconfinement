from pseudo_header import *

# parameters to be set manually

STARTFIT = [3, 3, 3, 1, 3]
ENDFIT = [7, 7, 7, 8, 8]
NDATA = [2, 2, 2, 2]
HTRDFMIN = [0.003625, 0.003875, 0.004125, 0.004375]
DHTRDF = [0.000125, 0.000125, 0.000125, 0.000125]
runName = ['run_tracedef_2507_108_0', 'run_tracedef_2507_108_1', 'run_tracedef_2507_108_2', 'run_tracedef_2507_108_3']
RGB = ["green", "blue", "red", "orange", "cyan"]
L = [108, 108, 108, 108]
latticeDim= ["10x108x108", "10x108x108", "10x108x108", "10x108x108", "10x108x108"]

#########################################

HTRDFMAX = [HTRDFMIN[0] + DHTRDF[0]*(NDATA[0]-1), HTRDFMIN[1] + DHTRDF[1]*(NDATA[1]-1), HTRDFMIN[2] + DHTRDF[2]*(NDATA[2]-1), HTRDFMIN[3] + DHTRDF[3]*(NDATA[3]-1)]

x1 = np.linspace(HTRDFMIN[0], HTRDFMAX[0], NDATA[0]).tolist()
x2 = np.linspace(HTRDFMIN[1], HTRDFMAX[1], NDATA[1]).tolist()
x3 = np.linspace(HTRDFMIN[2], HTRDFMAX[2], NDATA[2]).tolist()
x4 = np.linspace(HTRDFMIN[3], HTRDFMAX[3], NDATA[3]).tolist()
#x5 = np.linspace(HTRDFMIN[4], HTRDFMAX[4], NDATA[4]).tolist() 
#X = [x1, x2, x3, x4, x5]
X = [x1, x2, x3, x4]

x = [0]*len(NDATA)
y = [0]*len(NDATA)
sy = [0]*len(NDATA)

iperarr = [0]*len(NDATA)

#np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})

for i in range (0, len(NDATA)):

	mainPath = homeDir + '/Documents/thesis/simulation_analysis/simulation_data/' + runName[i]
	filew = mainPath + '/' + runName[i] + '_stripped.csv'
	iperarr[i] = np.loadtxt(filew, usecols = range(0, NDATA[i]))

for i in range(len(NDATA)):
	print("############################")
	print("N_s=")
	print(L[i])
	print("h")
	print(X[i])
	print("Chi(h)")
	print(np.array(iperarr[i][2]))
	print("s_chi(h)")
	print(np.array(iperarr[i][3]))

print("############################")

#########################################

# TrP plot

for i in range (0, len(NDATA)):

	arr = iperarr[i]
	
	xlabel = 'h'
	ylabel = '|TrP|'
	title = 'Polyakov loop (trace of) as a function of h'
	savepath = homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/TrP(L)'

	plotting(X[i], arr[0], arr[1], RGB[i], latticeDim[i], xlabel, ylabel, title, savepath)
	
plt.close()

# chi plot
	
for i in range (0, len(NDATA)):

	arr = iperarr[i]
	
	xlabel = 'h'
	ylabel = '$\chi$'
	title = 'Susceptibility as a function of h'
	savepath = homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/chi(L)'

	plotting(X[i], arr[2], arr[3], RGB[i], latticeDim[i], xlabel, ylabel, title, savepath)
	
plt.close()

# binder plot
	
for i in range (0, len(NDATA)):

	arr = iperarr[i]
	
	xlabel = 'h'
	ylabel = '$Q$'
	title = "Binder's cumulant as a function of h"
	savepath = homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/binder(L)'

	plotting(X[i], arr[4], arr[5], RGB[i], latticeDim[i], xlabel, ylabel, title, savepath)

plt.close()
  
'''

# quadratic fitting

h_pc = list()
sh_pc = list()
rchisq_vec = list()
chimax = list()
schimax = list()

for i in range (0, len(NDATA)):

	arr = iperarr[i]
	
	xlabel = 'h'
	ylabel = '$\chi$'
	title = 'Susceptibility as a function of h'
	savepath = homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/chi(L)_fit'

	xfit = np.array(X[i][STARTFIT[i]:ENDFIT[i]])
	yfit = np.array(arr[2][STARTFIT[i]:ENDFIT[i]])
	syfit = np.array(arr[3][STARTFIT[i]:ENDFIT[i]])

	print(xfit)

	p_chi, cov_chi = curve_fit(quadratic, xfit, yfit, p0 = [30, 0, 0.004], sigma = syfit, absolute_sigma = True)

	xplot = np.linspace(xfit[0], xfit[-1], 100)
	yplot = quadratic(xplot, p_chi[0], p_chi[1], p_chi[2])
	
	plt.rcParams["figure.figsize"] = [16, 9]
	plt.rcParams["figure.autolayout"] = True
	plt.grid()
	plt.xlabel(xlabel, fontsize = 12)
	plt.ylabel(ylabel, fontsize = 12)
	plt.title(title, fontsize = 12)
	plt.plot(X[i], arr[2], marker = "^", color = RGB[i], markersize = 5, linewidth = 0.5, label = latticeDim[i])
	plt.errorbar(X[i], arr[2], arr[3], color = RGB[i], capsize = 5)
	plt.plot(xplot, yplot, color = "purple", linewidth = 3)
	plt.legend(fontsize = "20")
	plt.savefig(savepath, facecolor = 'w')

	print("a: %f" %p_chi[0] + " +- " + "%f" % np.sqrt(cov_chi[0][0]) + " (%.2f" % abs(np.sqrt(cov_chi[0][0])/p_chi[0]*100) + "%)")
	print("b: %f" %p_chi[1] + " +- " + "%f" % np.sqrt(cov_chi[1][1]) + " (%.2f" % abs(np.sqrt(cov_chi[1][1])/p_chi[1]*100) + "%)")
	print("c: %f" %p_chi[2] + " +- " + "%f" % np.sqrt(cov_chi[2][2]) + " (%.2f" % abs(np.sqrt(cov_chi[2][2])/p_chi[2]*100) + "%)")
	print(" ")

	rchisq_vec.append(rchisq(quadratic(xfit, p_chi[0], p_chi[1], p_chi[2]), yfit, syfit,(len(yfit)-3)))

	chimax.append(p_chi[0])
	schimax.append(np.sqrt(cov_chi[0][0]))

	h_pc.append(p_chi[2])
	sh_pc.append(np.sqrt(cov_chi[2][2]))
plt.close()

print("reduced chi squared:")
print(rchisq_vec)
print(" ")

print("pseudo critic h:")
print(h_pc)
print(" ")

print("error on pseudo critic h: ")
print(sh_pc)
print(" ")

print("chi max:")
print(chimax)
print(" ")

print("error on chi max:")
print(schimax)
print(" ")

p_nu, cov_nu = curve_fit(f_scaling, L, h_pc, p0 = [0.004, 0, 1], maxfev = 5000, sigma = sh_pc, absolute_sigma=True)
print("parametri del fit h_pc = h_c + x_0/L^(-1/nu):")
print("h_c: %f" %p_nu[0] + " +- " + "%f" % np.sqrt(cov_nu[0][0]) + " (%.2f" % abs(np.sqrt(cov_nu[0][0])/p_nu[0]*100) + "%)")
print("x_0: %f" %p_nu[1] + " +- " + "%f" % np.sqrt(cov_nu[1][1]) + " (%.2f" % abs(np.sqrt(cov_nu[1][1])/p_nu[1]*100) + "%)")
print("1/nu: %f" %p_nu[2] + " +- " + "%f" % np.sqrt(cov_nu[2][2]) + " (%.2f" % abs(np.sqrt(cov_nu[2][2])/p_nu[2]*100) + "%)")
print("reduced chi squared:")
print(rchisq(f_scaling(L, p_nu[0], p_nu[1], p_nu[2]), h_pc, sh_pc,len(h_pc)-3))

print(" ")

p_gammanu, cov_gammanu = curve_fit(f_scaling, L, chimax, sigma = schimax, absolute_sigma=True)
print("parametri del fit chimax = A + B*L^(gamma/nu):")
print("A: %f" %p_gammanu[0] + " +- " + "%f" % np.sqrt(cov_gammanu[0][0]) + " (%.2f" % abs(np.sqrt(cov_gammanu[0][0])/p_gammanu[0]*100) + "%)")
print("B: %f" %p_gammanu[1] + " +- " + "%f" % np.sqrt(cov_gammanu[1][1]) + " (%.2f" % abs(np.sqrt(cov_gammanu[1][1])/p_gammanu[1]*100) + "%)")
print("gamma/nu: %f" %p_gammanu[2] + " +- " + "%f" % np.sqrt(cov_gammanu[2][2]) + " (%.2f" % abs(np.sqrt(cov_gammanu[2][2])/p_gammanu[2]*100) + "%)")
print("reduced chi squared:")
print(rchisq(f_scaling(L, p_gammanu[0], p_gammanu[1], p_gammanu[2]), chimax, schimax,len(chimax)-3))

print(" ")

Lplot = np.linspace(L[0], L[-1], 100)

plt.rcParams["figure.figsize"] = [16, 9]
plt.rcParams["figure.autolayout"] = True
plt.grid()
plt.xlabel("$N_s$", fontsize = 12)
plt.ylabel("$h_{pc}$", fontsize = 12)
plt.title("$h_{pc}(L)$", fontsize = 12)
plt.plot(L, h_pc, marker = "^", color = "red", markersize = 5, linewidth = 0.5, label = "$h_{pc}(L)$")
plt.errorbar(L, h_pc, sh_pc, color = "red", capsize = 5)
plt.plot(Lplot, f_scaling(Lplot, p_nu[0], p_nu[1], p_nu[2]), color = "purple", linewidth = 3)
plt.legend(fontsize = "20")
plt.savefig(homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/h_pc(L)', facecolor = 'w')
plt.close()

plt.rcParams["figure.figsize"] = [16, 9]
plt.rcParams["figure.autolayout"] = True
plt.grid()
plt.xlabel("$N_s$", fontsize = 12)
plt.ylabel("$\chi_M$", fontsize = 12)
plt.title("$\chi_M(L)$", fontsize = 12)
plt.plot(L, chimax, marker = "^", color = "red", markersize = 5, linewidth = 0.5, label = "$\chi_M(L)$")
plt.errorbar(L, chimax, schimax, color = "red", capsize = 5)
plt.plot(Lplot, f_scaling(Lplot, p_gammanu[0], p_gammanu[1], p_gammanu[2]), color = "purple", linewidth = 3)
plt.legend(fontsize = "20")
plt.savefig(homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/chi_max(L)', facecolor = 'w')
plt.close()

# finite size scaling chi

#for i in range(0, len(NDATA)):

#    arr = iperarr[i]

#    x[i], y[i], sy[i] = FSS(L[i], arr[2], arr[3], 1.365, 1, 0.0039, HTRDFMIN[i], HTRDFMAX[i], DHTRDF[i])

#    xlabel = '(h-$h_c)L^{1/\u03BD}$'
#    ylabel = '$\chi$ $L^{-\u03B3/\u03BD}}$'
#    title = 'Susceptibility as a function of h'
#    savepath = homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/simul_plot_chi_FSS'

#    plotting(x[i], y[i], sy[i], RGB[i], latticeDim[i], xlabel, ylabel, title, savepath)
	
#####################


#gamma_nu = np.log(iperarr[1][2][4]/iperarr[2][2][4])/np.log(L[1]/L[2])
#print(gamma_nu)
	 
ascissona = np.reciprocal([30., 40., 50., 72., 96.])
ordinatona = [0.00429, 0.00434, 0.00424, 0.00410, 0.0039]
errorone = [0.00004, 0.00007, 0.00004, 0.00005, 0.0001]

def funzionona(x, A, B):
	return  A + B*x

ordinatona_fit = ordinatona[1:]
ascissona_fit = ascissona[1:]
errorone_fit = errorone[1:]

parametrone, covarione = curve_fit(funzionona, ascissona_fit, ordinatona_fit, sigma = errorone_fit, absolute_sigma=True)
print("Linear fit: y = A+B1/L:")
print("A: %f" %parametrone[0] + " +- " + "%f" % np.sqrt(covarione[0][0]) + " (%.2f" % abs(np.sqrt(covarione[0][0])/parametrone[0]*100) + "%)")
print("B: %f" %parametrone[1] + " +- " + "%f" % np.sqrt(covarione[1][1]) + " (%.2f" % abs(np.sqrt(covarione[1][1])/parametrone[1]*100) + "%)")
print("Reduced chi squared: ")
print(rchisq(funzionona(ascissona_fit, parametrone[0], parametrone[1]), ordinatona_fit,  errorone_fit, n = 2))

print(" ")

plt.rcParams["figure.figsize"] = [16, 9]
plt.rcParams["figure.autolayout"] = True
plt.xlim(0., 0.035)
plt.ylim(0.0032, 0.0047)
plt.grid()
plt.xlabel("$1/{N_s}$", fontsize = 12)
plt.ylabel("$h_{pc}$", fontsize = 12)
plt.title("$h_{pc}(1/N_s))$", fontsize = 12)
plt.plot(ascissona, ordinatona, marker = "^", color = "red", markersize = 5, linewidth = 0, label = "chi_max(L)")
plt.errorbar(ascissona, ordinatona, errorone, color = "red", capsize = 5)
plt.plot(ascissona_fit, funzionona(ascissona_fit, parametrone[0], parametrone[1]), color = "purple", linewidth = 3)
plt.legend(fontsize = "20")
plt.savefig(homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/h_pc_2Dising(L)', facecolor = 'w')
plt.close()

chimax_tmp = chimax[1:]
schimax_tmp = schimax[1:]
L_tmp = L[1:]
Lplot_tmp = Lplot[10:]

p_gammanu_tmp, cov_gammanu_tmp = curve_fit(f_scaling, L_tmp, chimax_tmp, sigma = schimax_tmp, absolute_sigma=True)
print("parametri del fit chimax = A + B*L^(gamma/nu) con sample size = 4:")
print("A: %f" %p_gammanu_tmp[0] + " +- " + "%f" % np.sqrt(cov_gammanu_tmp[0][0]) + " (%.2f" % abs(np.sqrt(cov_gammanu_tmp[0][0])/p_gammanu_tmp[0]*100) + "%)")
print("B: %f" %p_gammanu_tmp[1] + " +- " + "%f" % np.sqrt(cov_gammanu_tmp[1][1]) + " (%.2f" % abs(np.sqrt(cov_gammanu_tmp[1][1])/p_gammanu_tmp[1]*100) + "%)")
print("gamma/nu: %f" %p_gammanu_tmp[2] + " +- " + "%f" % np.sqrt(cov_gammanu_tmp[2][2]) + " (%.2f" % abs(np.sqrt(cov_gammanu_tmp[2][2])/p_gammanu_tmp[2]*100) + "%)")
print("reduced chi squared:")
print(rchisq(f_scaling(L_tmp, p_gammanu_tmp[0], p_gammanu_tmp[1], p_gammanu_tmp[2]), chimax_tmp, schimax_tmp,len(chimax_tmp)-3))

plt.rcParams["figure.figsize"] = [16, 9]
plt.rcParams["figure.autolayout"] = True
plt.grid()
plt.xlabel("$N_s$", fontsize = 12)
plt.ylabel("$\chi_M$", fontsize = 12)
plt.title("$\chi_M(L)$", fontsize = 12)
plt.plot(L_tmp, chimax_tmp, marker = "^", color = "red", markersize = 5, linewidth = 0.5, label = "$\chi_M(L)$")
plt.errorbar(L_tmp, chimax_tmp, schimax_tmp, color = "red", capsize = 5)
plt.plot(Lplot_tmp, f_scaling(Lplot_tmp, p_gammanu_tmp[0], p_gammanu_tmp[1], p_gammanu_tmp[2]), color = "purple", linewidth = 3)
plt.savefig(homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/chi_max_rmv(L)', facecolor = 'w')
plt.close()

def chi_ising2D(x, A, B):
	return A + B*np.array(x)**1.75

x2D = [40, 50, 72, 96]
chi2D = [43.4, 59.9, 100.1, 149]
schi2D = [0.5, 0.7, 1.5, 3.9]

p_2D, cov_2D = curve_fit(chi_ising2D, x2D, chi2D, sigma = schi2D, absolute_sigma = True)
print("2D ising fit: y = A+Bx**(1.75) 4 punti:")
print("A: %f" %p_2D[0] + " +- " + "%f" % np.sqrt(cov_2D[0][0]) + " (%.2f" % abs(np.sqrt(cov_2D[0][0])/p_2D[0]*100) + "%)")
print("B: %f" %p_2D[1] + " +- " + "%f" % np.sqrt(cov_2D[1][1]) + " (%.2f" % abs(np.sqrt(cov_2D[1][1])/p_2D[1]*100) + "%)")
print("Reduced chi squared: ")
print(rchisq(chi_ising2D(x2D, p_2D[0], p_2D[1]), chi2D,  schi2D, n = 2))

p_2D_0, cov_2D_0 = curve_fit(chi_ising2D, L, chimax, sigma = schimax, absolute_sigma = True)
print("2D ising fit: y = A+Bx**(1.75) 5 punti:")
print("A: %f" %p_2D_0[0] + " +- " + "%f" % np.sqrt(cov_2D_0[0][0]) + " (%.2f" % abs(np.sqrt(cov_2D_0[0][0])/p_2D_0[0]*100) + "%)")
print("B: %f" %p_2D_0[1] + " +- " + "%f" % np.sqrt(cov_2D_0[1][1]) + " (%.2f" % abs(np.sqrt(cov_2D_0[1][1])/p_2D_0[1]*100) + "%)")
print("Reduced chi squared: ")
print(rchisq(chi_ising2D(L, p_2D_0[0], p_2D_0[1]), chimax,  schimax, n = 2))

plt.rcParams["figure.figsize"] = [16, 9]
plt.rcParams["figure.autolayout"] = True
plt.grid()
plt.xlabel("$N_s$", fontsize = 12)
plt.ylabel("$\chi_M$", fontsize = 12)
plt.title("$\chi_M(L)$", fontsize = 12)
plt.plot(L, chimax, marker = "^", color = "red", markersize = 5, linewidth = 0.5, label = "$\chi_M(L)$")
plt.errorbar(L, chimax, schimax, color = "red", capsize = 5)
plt.plot(x2D, chi_ising2D(x2D, p_2D[0], p_2D[1]), color = "yellow", linewidth = 3, label = "[40, 50, 72, 96]")
plt.plot(L, chi_ising2D(L, p_2D_0[0], p_2D_0[1]), color = "purple", linewidth = 3, label = "[30, 40, 50, 72, 96]")
plt.legend()
plt.savefig(homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/chi_max_Ising2D(L)', facecolor = 'w')
plt.close()
'''






	
