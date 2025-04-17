from pseudo_header import *

path = "/home/anegro99/Documents/thesis/analysis/data/transition/"

# parameters to be set manually

file_names = ["tran_10_72_23.3805_claudio", "tran_10_72_23.3805", "tran_10_96_23.3805", "tran_10_108_23.3805", "tran_10_120_23.3805"]
RGB = ["magenta", "orange", "red", "green", "blue"]
L = [72, 72, 96, 108, 120]
latticeDim= ["10x72x72_claudio", "10x72x72", "10x96x96", "10x108x108", "10x120x120"]

#########################################

h_array = [0] * len(file_names)
TrP_array = [0] * len(file_names)
sTrP_array = [0] * len(file_names)
chi_array = [0] * len(file_names)
schi_array = [0] * len(file_names)
binder_array = [0] * len(file_names)
sbinder_array = [0] * len(file_names)

for count, name in enumerate(file_names):
	file_path = path + name + "/" + name + ".csv"

	h_array[count] = []
	TrP_array[count] = []
	sTrP_array[count]= []
	chi_array[count] = []
	schi_array[count] = []
	binder_array[count] = []
	sbinder_array[count] = []
	
	with open(file_path, "r") as csvfile:
		for line in csvfile:

			columns = line.split()

			h_array[count].append(float(columns[0])) 
			TrP_array[count].append(float(columns[1]))
			sTrP_array[count].append(float(columns[2]))
			chi_array[count].append(float(columns[3]))
			schi_array[count].append(float(columns[4]))
			binder_array[count].append(float(columns[5]))
			sbinder_array[count].append(float(columns[6]))

#########################################

# TrP plot

for i in range (len(file_names)):
	
	xlabel = 'h'
	ylabel = '|TrP|'
	title = 'Polyakov loop (trace of) as a function of h'
	savepath = "/home/anegro99/Documents/thesis/analysis/plots/polyakov"

	plotting(h_array[i], TrP_array[i], sTrP_array[i], RGB[i], latticeDim[i], xlabel, ylabel, title, savepath)
	
plt.close()

# chi plot
	
for i in range (len(file_names)):

	xlabel = 'h'
	ylabel = '$\chi$'
	title = 'Susceptibility as a function of h'
	savepath = "/home/anegro99/Documents/thesis/analysis/plots/susceptibility"

	plotting(h_array[i], chi_array[i], schi_array[i], RGB[i], latticeDim[i], xlabel, ylabel, title, savepath)
	
plt.close()

# binder plot
	
for i in range (0, len(file_names)):
	
	xlabel = 'h'
	ylabel = '$Q$'
	title = "Binder's cumulant as a function of h"
	savepath = "/home/anegro99/Documents/thesis/analysis/plots/binder"

	plotting(h_array[i], binder_array[i], sbinder_array[i], RGB[i], latticeDim[i], xlabel, ylabel, title, savepath)

plt.close()
  