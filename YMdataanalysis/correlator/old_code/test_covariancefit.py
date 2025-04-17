from calendar import c
from pseudo_header import *

file_names = ["corr_24_10_96_0.006"]
RGB = ["magenta"]
N_t = np.array([10])
L = [96]
info = ["24_10x96x96_0.006"]

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

for i in range(len(file_names)):

    start = 19

    with open("/home/anegro99/Documents/thesis/analysis/data/correlator/" + file_names[i] +"/data/cov.txt", 'r') as file:
        sigma_matrix = []
		
        for line in file:
            values = [float(x) for x in line.strip().split()]
            sigma_matrix.append(values) 
    sigma_matrix = np.array(sigma_matrix)

    sigma_red = sigma_matrix[start:, start:]

    sigma_red /= 8911004
    print(np.sqrt(sigma_red))

    x = np.array(R[0][start:])
    y = G[0][start:]
    sy = sG[0][start:]

    offset = 1

    print(sigma_red)

    print("\n")

    np.fill_diagonal(sigma_red[offset+4:], 0)
    np.fill_diagonal(sigma_red[:, offset+4:], 0)

    np.fill_diagonal(sigma_red[offset+3:], 0)
    np.fill_diagonal(sigma_red[:, offset+3:], 0)

    np.fill_diagonal(sigma_red[offset+2:], 0)
    np.fill_diagonal(sigma_red[:, offset+2:], 0)

    np.fill_diagonal(sigma_red[offset+1:], 0)
    np.fill_diagonal(sigma_red[:, offset+1:], 0)

    print(sigma_red)

    p_K0, cov_K0 = curve_fit(V_complete, x, y, sigma = sigma_red, absolute_sigma = True)
    print("fit V = a*K_0(b*R):")
    print("a: %.12f" %p_K0[0] + " +- " + "%.12f" % np.sqrt(cov_K0[0][0]) + " (%.2f" % abs(np.sqrt(cov_K0[0][0])/p_K0[0]*100) + "%)") 
    print("b: %.12f" %p_K0[1] + " +- " + "%.12f" % np.sqrt(cov_K0[1][1]) + " (%.2f" % abs(np.sqrt(cov_K0[1][1])/p_K0[1]*100) + "%)")
    print("Fitted range [R_min, R_max] = " + "[" + str(int(x[0])) + ", " + str(int(x[-1])) + "]")
    print("Reduced chi squared: ")
    print(rchisq(V_complete(x, p_K0[0], p_K0[1]), y,  sy, n = len(x)-2))