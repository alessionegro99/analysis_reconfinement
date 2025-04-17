from pseudo_header import *

# path to the rough data
path = "/home/anegro99/Documents/thesis/analysis/data/correlator/" + sys.argv[1]
filename = random.choice(os.listdir(path + '/roughdata/'))

# file column number for which the data starts being G(0) G(1) ... G(R-1)
column_index_start = 4

with open(path + '/roughdata/' + filename, "r") as datfile:
    for count, line in enumerate(datfile):

        columns = line.split()

        if count == 1:  # definition of G vector 
            G = [0] * ((len(columns)-column_index_start)//2)

            for i in range(len(G)):
                G[i] = []

            for i in range (column_index_start, len(columns), 2):
                G[(i-column_index_start)//2].append(float(columns[i-column_index_start]))

            R_corr = (len(columns)-column_index_start)//2

        if count > 1: # vector filling
            for i in range (column_index_start, len(columns), 2):
                G[(i-column_index_start)//2].append(float(columns[i-column_index_start]))

indexList = list(range(R_corr)) # list of values {r = 0, ... ,R-1}
x = [j for j in range(len(G[0]))]

for i in range(R_corr): # plotting of values to gauge thermalization 
    y = G[i]
    plt.grid
    plt.xlabel('iterations')
    plt.ylabel('G(' + str(i) + ')')
    plt.title('Thermalization')
    plt.plot(x, y, marker = "o", markersize = 3, linewidth = 0.5)
    filename = filename.replace('.dat', '')
    plt.savefig(path + '/plots/thermalization/thermalization_' + filename + '_G(' + str(i) + ').png', facecolor='w')
    plt.close()
