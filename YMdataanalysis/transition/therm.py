from pseudo_header import *

path = "/home/anegro99/Documents/thesis/analysis/data/transition/" + sys.argv[1]

for filename in os.listdir(path + '/roughdata/'):
    components = filename.split('_')[2].split('.')
    if int(components[0]) == 0:
        data = pd.read_csv(path + '/roughdata/' + filename , sep=' ', header=None)
        df = data.iloc[0:,[2,3]]
        df[4] = (df[2]**2 + df[3]**2)**(1/2)

        NDATA = df.shape[0]

        x = [i for i in range(len(df[4]))]
        y = df[4]

        plt.ylim(0,1)
        plt.xlabel('iterations')
        plt.ylabel('$P$')
        plt.title('Thermalization')
        plt.plot(x, y, marker = "o", markersize = 2, linewidth = 0.1)
        filename = filename.replace('.dat', '.png')
        plt.savefig(path + '/plots/thermalization/thermalization_' + filename, facecolor='w')
        plt.close()