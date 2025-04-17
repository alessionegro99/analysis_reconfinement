from pseudo_header import *

#file_names = ["corr_24_10_96_0.003","corr_24_10_96_0.0035", "corr_24_10_96_0.004", "corr_24_10_96_0.0045", "corr_24_10_96_0.00475", "corr_24_10_96_0.005", "corr_24_10_96_0.00525", "corr_24_10_96_0.0055", "corr_24_10_96_0.00575", "corr_24_10_96_0.006" ]
#RGB = ["Red", "Blue", "Green", "Black", "Yellow", "Orange", "Purple", "Pink", "Turquoise", "Brown"]
#N_t = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
#L = [96, 96, 96, 96, 96, 96, 96, 96, 96, 96]
#info = ["24_10x96x96_0.003","24_10x96x96_0.0035", "24_10x96x96_0.004", "24_10x96x96_0.0045", "24_10x96x96_0.00475", "24_10x96x96_0.005", "24_10x96x96_0.00525", "24_10x96x96_0.0055", "24_10x96x96_0.00575", "24_10x96x96_0.006"]

# basic info

file_names = ["corr_24_7_96_0.006","corr_24_8_96_0.006", "corr_24_9_96_0.006", "corr_24_10_96_0.006", "corr_24_11_96_0.006", "corr_24_12_96_0.006"]
RGB = ["Red", "Blue", "Green", "Black", "Magenta", "Orange"]
N_t = np.array([7, 8, 9, 10, 11, 12])
L = [96, 96, 96, 96, 96, 96]
info = ["$7\times96^2$","$8\times96^2$", "$9\times96^2$", "$10\times96^2$", "$11\times96^2$", "$12\times96^2$"]

# Loading observables from files

R = [0] * len(file_names)
G = [0] * len(file_names)
sG = [0] * len(file_names)

# observables upload

for count, name in enumerate(file_names):
	file_path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + name + "/data/output_BS.txt"

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

# Plot G

for i in range (len(file_names)):
	
    x = R[i]
    y = G[i]    
    sy = sG[i]
	
    xlabel = "r"
    ylabel = "G(r)"
    title = "Two point correlation function as a function of lattice spacing"
    savepath = "/home/anegro99/Documents/thesis/analysis/data/correlator/"
    dir = savepath + file_names[i] + "/plots"
	
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.plot(x, y, marker = ".", color = RGB[i], markersize = 7, linestyle = "None" , label = info[i])
    plt.errorbar(x, y, sy, color = RGB[i], linestyle = "None" ,capsize = 8)
    plt.legend()
    plt.savefig(dir + "/G(r).png", facecolor = 'w')
    plt.close()

# fitting data = uncorrelated

for i in range(len(file_names)):

    # rchisq minimum finding

    rchisqarr = []
	
    for fit_start in range(1,20):
        x = np.array(R[i][fit_start:])
        y = G[i][fit_start:]
        sy = sG[i][fit_start:]

        p_K0, cov_K0 = curve_fit(K0, x, y, sigma = sy, absolute_sigma = True, maxfev = 10000)
        rchisqarr.append(rchisq(K0(x, p_K0[0], p_K0[1]), y,  sy, n = len(x)-2))

    rchisqarr = np.array(rchisqarr)

    min = rchisqarr[np.abs(rchisqarr-1).argmin()]

    for count, fit_start in enumerate(range(1,20)):
          if min == rchisqarr[count]:
                start = count+1

    x = np.array(R[i][start:])
    y = G[i][start:]
    sy = sG[i][start:]

    p_K0, cov_K0 = curve_fit(K0, x, y, sigma = sy, absolute_sigma = True)

    p_K0, cov_K0 = curve_fit(K0, x, y, sigma = sy, absolute_sigma = True, maxfev = 10000)
    print("fit G(r) = a*K_0(b*r):")
    print("a: %.12f" %p_K0[0] + " +- " + "%.12f" % np.sqrt(cov_K0[0][0]) + " (%.2f" % abs(np.sqrt(cov_K0[0][0])/p_K0[0]*100) + "%)") 
    print("b: %.12f" %p_K0[1] + " +- " + "%.12f" % np.sqrt(cov_K0[1][1]) + " (%.2f" % abs(np.sqrt(cov_K0[1][1])/p_K0[1]*100) + "%)")
    print("Fitted range [R_min, R_max] = " + "[" + str(int(x[0])) + ", " + str(int(x[-1])) + "]")
    print("Reduced chi squared: ")
    print(rchisq(K0(x, p_K0[0], p_K0[1]), y,  sy, n = len(x)-2))
    print("\n")
    
    plt.xlabel("r")
    plt.ylabel("G(r)")
    plt.title("Two point correlation function as a function of lattice spacing")
    plt.plot(R[i], G[i], marker = ".", color = "blue", markersize = 7, linestyle = 'None', label = "G(r)")
    plt.errorbar(R[i], G[i], sG[i], linestyle = 'None',color = "blue", capsize = 7)
    plt.plot(x, K0(x, p_K0[0], p_K0[1]), color = "orange", linewidth = 1, label = "a*K_0(b*r)")
    plt.legend()
    plt.savefig("/home/anegro99/Documents/thesis/analysis/data/correlator/" + file_names[i] + "/plots/a*K0(br).png", facecolor = 'w')
    
    plt.close()
      

for i in range (len(file_names)):
    x = R[i]
    y = G[i]
    sy = sG[i]
    xlabel = "$r$"
    ylabel = "$G(r)$"
    title = "Two point correlation function for different $N_t$"
    savepath = "/home/anegro99/Documents/thesis/analysis/plots/correlator/G(r,Nt).png"

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.plot(x, y, marker = ".", color = RGB[i], markersize = 7, linestyle = "None" , label = info[i])
    plt.errorbar(x, y, sy, color = RGB[i], linestyle = "None" ,capsize = 8)
    plt.legend()
    plt.savefig(savepath, facecolor = 'w')
plt.close()

# fitting data = correlated

