from pseudo_header import *

file_names = ["corr_24_7_96_0.006","corr_24_8_96_0.006","corr_24_9_96_0.006","corr_24_10_96_0.006","corr_24_11_96_0.006", "corr_24_12_96_0.006"]
RGB = ["magenta", "red", "blue", "green", "purple", "orange"]
N_t = np.array([7,8,9,10,11,12])
L = [96, 96, 96, 96, 96, 96]
info = ["24_7x96x96_0.006","24_10x96x96_0.006","24_9x96x96_0.006","24_10x96x96_0.006","24_11x96x96_0.006","24_12x96x96_0.006"]

R = [0] * len(file_names)
G = [0] * len(file_names)
sG = [0] * len(file_names)

for count, name in enumerate(file_names):
	file_path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + name + "/data/output.txt"

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

V = []
sV = []

for i in range(len(N_t)):
    V.append(-1/N_t[i]*np.log(G[i]))
    sV.append(abs(1/N_t[i]*1/G[i]*sG[i]))

# G

for i in range (len(file_names)):
	
    x = R[i]
    y = G[i]    
    sy = sG[i]
	
    xlabel = "r"
    ylabel = "G(r)"
    title = "Two point correlation function as a function of lattice spacing"
    savepath = "/home/anegro99/Documents/thesis/analysis/plots/correlator/"
    dir = savepath + file_names[i]

    # Verifica se la cartella non esiste
    if not os.path.exists(dir):
        os.makedirs(dir)

	
    plt.xlabel(xlabel, fontsize = 20)
    plt.ylabel(ylabel, fontsize = 20)
    plt.title(title, fontsize = 20)
    plt.plot(x, y, marker = ".", color = RGB[i], markersize = 7, linestyle = "None" , label = info[i])
    plt.errorbar(x, y, sy, color = RGB[i], linestyle = "None" ,capsize = 8)
    plt.legend(fontsize = "20")
    plt.savefig(dir + "/G(r).png", facecolor = 'w')
    plt.close()

# V

for i in range(len(file_names)):
	
    x = R[i]
    y = V[i]
    sy = sV[i]
	
    xlabel = "r"
    ylabel = "-1/N_t*log(G(r))"
    title = "Interquark potential"
    savepath = "/home/anegro99/Documents/thesis/analysis/plots/correlator/"

    dir = savepath + file_names[i]

    plt.xlabel(xlabel, fontsize = 20)
    plt.ylabel(ylabel, fontsize = 20)
    plt.title(title, fontsize = 20)
    plt.plot(x, y, marker = ".", color = RGB[i], markersize = 7, linestyle = "None" , label = info[i])
    plt.errorbar(x, y, sy, color = RGB[i], linestyle = "None",capsize = 8)
    plt.legend(fontsize = "20")
    plt.savefig(dir + "/V(r).png", facecolor = 'w')	
    plt.close()


# fitting 

for i in range(len(file_names)):

    rchisqarr = []
	
    for fit_start in range(1,20):
        x = np.array(R[i][fit_start:])
        y = G[i][fit_start:]
        sy = sG[i][fit_start:]

        p_V_complete, cov_V_complete = curve_fit(V_complete, x, y, sigma = sy, absolute_sigma = True, maxfev = 5000)
        rchisqarr.append(rchisq(V_complete(x, p_V_complete[0], p_V_complete[1]), y,  sy, n = len(x)-2))

    rchisqarr = np.array(rchisqarr)

    min = rchisqarr[np.abs(rchisqarr-1).argmin()]

    for count, fit_start in enumerate(range(1,20)):
          if min == rchisqarr[count]:
                start = count+1

    x = np.array(R[i][start:])
    y = G[i][start:]
    sy = sG[i][start:]

    p_V_complete, cov_V_complete = curve_fit(V_complete, x, y, sigma = sy, absolute_sigma = True)

    p_V_complete, cov_V_complete = curve_fit(V_complete, x, y, sigma = sy, absolute_sigma = True, maxfev = 10000)
    print("fit V = a*K_0(b*R):")
    print("a: %.12f" %p_V_complete[0] + " +- " + "%.12f" % np.sqrt(cov_V_complete[0][0]) + " (%.2f" % abs(np.sqrt(cov_V_complete[0][0])/p_V_complete[0]*100) + "%)") 
    print("b: %.12f" %p_V_complete[1] + " +- " + "%.12f" % np.sqrt(cov_V_complete[1][1]) + " (%.2f" % abs(np.sqrt(cov_V_complete[1][1])/p_V_complete[1]*100) + "%)")
    print("Fitted range [R_min, R_max] = " + "[" + str(int(x[0])) + ", " + str(int(x[-1])) + "]")
    print("Reduced chi squared: ")
    print(rchisq(V_complete(x, p_V_complete[0], p_V_complete[1]), y,  sy, n = len(x)-2))

for i in range (len(file_names)):

	plt.xlabel("r", fontsize = 20)
	plt.ylabel("G(r)", fontsize = 20)
	plt.title("Two point correlation function as a function of lattice spacing", fontsize = 20)
	plt.plot(R[i], G[i], marker = "^", color = "blue", markersize = 7, linestyle = 'None', label = "G(r)")
	plt.errorbar(R[i], G[i], sG[i], linestyle = 'None',color = "blue", capsize = 7)
	plt.plot(x, V_complete(x, p_V_complete[0], p_V_complete[1]), color = "orange", linewidth = 1, label = "a*K_0(b*r)")
	plt.legend(fontsize = "20")
	plt.savefig("/home/anegro99/Documents/thesis/analysis/plots/correlator/" + file_names[i] + "/a*K0(br).png", facecolor = 'w')

	plt.close()

if sys.argv[1] == 1:
    E0 = p_V_complete[1]
    dE0 = cov_V_complete[1][1]
    Nt = N_t[0]
    pi = np.pi

    sigma0 = (pi+np.sqrt(pi**2+(6*E0*Nt)**2))/(6*Nt**2)

    E1 = 1/Nt*np.sqrt(4/3*pi**2+4/3*pi*np.sqrt(pi**2+(6*E0*Nt)**2)+(E0*Nt)**2)
    print("\n")
    print("E1:")
    print(E1)
    print("\n")
    print("dE1:")
    dE1 = dE0*E0*Nt*(1+(48*pi)/(np.sqrt(pi**2+(6*E0*Nt)**2)))/(np.sqrt(4/3*pi**2+4/3*pi*np.sqrt(pi**2+(6*E0*Nt)**2)+(E0*Nt)**2))
    print(dE1)

