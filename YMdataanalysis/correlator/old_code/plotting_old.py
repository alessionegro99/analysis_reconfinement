from multiprocessing import allow_connection_pickling
from operator import inv
from pseudo_header import *

path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + sys.argv[1]

file_names = ["corr_24_10_96_0.006"]
RGB = ["magenta"]
N_t = np.array([10])
L = [96]
info = ["24_10x96x96_0.006"]

R = [0] * len(file_names)
G = [0] * len(file_names)
sG = [0] * len(file_names)

for count, name in enumerate(file_names):
	file_path = path + "/data/output.txt"

	R[count] = []
	G[count] = []
	sG[count] = []
	
	with open(file_path, "r") as txtfile:
		for line in txtfile:

			columns = line.split()

			R[count].append(float(columns[0])) 
			G[count].append(float(columns[1]))
			sG[count].append(float(columns[2]))
			
G = np.array(G)
sG = np.array(sG)

# G

for i in range (len(file_names)):
	
	xlabel = 'R'
	ylabel = 'G(R)'
	title = 'Two point correlation function as a function of lattice spacing'
	savepath = "/home/anegro99/Documents/thesis/analysis/plots/correlator"

	plotting(R[i], G[i], sG[i], RGB[i], info[i], xlabel, ylabel, title, savepath)
	
plt.close()

G_log = -1/N_t*np.log(G)
sG_log = abs(1/N_t*1/G*sG)

# G_log T=0

for i in range (len(file_names)):
	
	xlabel = 'R'
	ylabel = '-1/N_t*log(G(R))'
	title = 'Interquark potential'
	savepath = "/home/anegro99/Documents/thesis/analysis/plots/correlator_log"

	plotting(R[i], G_log[i], sG_log[i], RGB[i], info[i], xlabel, ylabel, title, savepath)
	
plt.close()

if int(sys.argv[2]) == 0:

	# fit a T = 0

	x = np.array(R[0][5:])
	y = G_log[0][5:]
	sy = sG_log[0][5:]

	p_V_0, cov_V_0 = curve_fit(V_0, x, y, sigma = sy, absolute_sigma = True)
	print("fit V = a + b*R + c*1/R:")
	print("a: %f" %p_V_0[0] + " +- " + "%f" % np.sqrt(cov_V_0[0][0]) + " (%.2f" % abs(np.sqrt(cov_V_0[0][0])/p_V_0[0]*100) + "%)")
	print("b: %f" %p_V_0[1] + " +- " + "%f" % np.sqrt(cov_V_0[1][1]) + " (%.2f" % abs(np.sqrt(cov_V_0[1][1])/p_V_0[1]*100) + "%)")
	print("c: %f" %p_V_0[2] + " +- " + "%f" % np.sqrt(cov_V_0[2][2]) + " (%.2f" % abs(np.sqrt(cov_V_0[2][2])/p_V_0[2]*100) + "%)")
	print("Fitted range [R_min, R_max] = " + "[" + str(int(x[0])) + ", " + str(int(x[-1])) + "]")
	print("Reduced chi squared: ")
	print(rchisq(V_0(x, p_V_0[0], p_V_0[1], p_V_0[2]), y,  sy, n = len(x)-3))

	for i in range (len(file_names)):

		plt.grid()
		plt.xlabel("R", fontsize = 20)
		plt.ylabel("-1/N_t*log(G(R))", fontsize = 20)
		plt.title("Two point correlation function as a function of lattice spacing", fontsize = 20)
		plt.plot(R[i], G_log[i], marker = "^", color = "red", markersize = 5, linestyle = 'None', label = "-1/N_t*log(G(R))")
		plt.errorbar(R[i], G_log[i], sG_log[i], color = "red", linestyle = 'None', capsize = 5)
		plt.plot(x, V_0(x, p_V_0[0], p_V_0[1], p_V_0[2]), color = "green", linewidth = 1, label = "a + b*R + c*1/R")
		plt.legend(fontsize = "20")
		plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/fit_0", facecolor = 'w')

	plt.close()

if int(sys.argv[2]) == 3:

	fit_start = 3

	with open("/home/anegro99/Documents/thesis/analysis/data/correlator/" + sys.argv[1] +"/data/cov.txt", 'r') as file:
		sigma_matrix = []
		
		for line in file:
			values = [float(x) for x in line.strip().split()]
			sigma_matrix.append(values) 
	sigma_matrix = np.array(sigma_matrix)

	print(sigma_matrix[fit_start:, fit_start:])

	x = np.array(R[0][fit_start:])
	y = G[0][fit_start:]
	sy = sG[0][fit_start:]

	print(sigma_matrix)

	p_V_complete, cov_V_complete = curve_fit(V_complete, x, y, sigma = sy, absolute_sigma = True, maxfev = 10000)
	print("fit V = a*K_0(b*R):")
	print("a: %f" %p_V_complete[0] + " +- " + "%f" % np.sqrt(cov_V_complete[0][0]) + " (%.2f" % abs(np.sqrt(cov_V_complete[0][0])/p_V_complete[0]*100) + "%)")
	print("b: %f" %p_V_complete[1] + " +- " + "%f" % np.sqrt(cov_V_complete[1][1]) + " (%.2f" % abs(np.sqrt(cov_V_complete[1][1])/p_V_complete[1]*100) + "%)")
	print("Fitted range [R_min, R_max] = " + "[" + str(int(x[0])) + ", " + str(int(x[-1])) + "]")
	print("Reduced chi squared: ")
	print(rchisq(V_complete(x, p_V_complete[0], p_V_complete[1]), y,  sy, n = len(x)-2))

	p_V_complete_mod, cov_V_complete_mod = curve_fit(V_complete, x, y, p0 = [0.02, 0.02],  absolute_sigma = True)
	print("fit V = a*K_0(b*R) with correlation matrix:")
	print("a: %f" %p_V_complete_mod[0] + " +- " + "%f" % np.sqrt(cov_V_complete_mod[0][0]) + " (%.2f" % abs(np.sqrt(cov_V_complete_mod[0][0])/p_V_complete_mod[0]*100) + "%)")
	print("b: %f" %p_V_complete_mod[1] + " +- " + "%f" % np.sqrt(cov_V_complete_mod[1][1]) + " (%.2f" % abs(np.sqrt(cov_V_complete_mod[1][1])/p_V_complete_mod[1]*100) + "%)")
	print("Fitted range [R_min, R_max] = " + "[" + str(int(x[0])) + ", " + str(int(x[-1])) + "]")
	print("Reduced chi squared: ")
	print(rchisq(V_complete(x, p_V_complete_mod[0], p_V_complete_mod[1]), y,  sy, n = len(x)-2))

	for i in range (len(file_names)):

		plt.grid()
		plt.xlabel("R", fontsize = 20)
		plt.ylabel("G(R)", fontsize = 20)
		plt.title("Two point correlation function as a function of lattice spacing", fontsize = 20)
		plt.plot(R[i], G[i], marker = "^", color = "blue", markersize = 5, linestyle = 'None', label = "G(R)")
		plt.errorbar(R[i], G[i], sG[i], linestyle = 'None',color = "blue", capsize = 5)
		plt.plot(x, V_complete(x, p_V_complete[0], p_V_complete[1]), color = "orange", linewidth = 1, label = "a*K_0(b*R)")
		#plt.plot(x, V_complete(x, p_V_complete_mod[0], p_V_complete_mod[1]), color = "green", linewidth = 1, label = "a*K_0(b*R)_correlation")
		plt.legend(fontsize = "20")
		plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/fit_T_finite_k0", facecolor = 'w')

	plt.close()
