from pseudo_header import *

path = "/home/anegro99/Documents/thesis/analysis/data/transition/" + sys.argv[1]

# bootstrap parameter
NBS = 200

for filename in tqdm(os.listdir(path + '/data/')):
    # loading data file
    data = np.loadtxt(path + '/data/' + filename)

    # real and imaginary part of the Polyakov loop
    ReTrP = np.array(data[:, 2])
    ImTrP = np.array(data[:, 3])

    # primary observables

    TrP = (ReTrP**2 + ImTrP**2)**0.5
    TrP2 = TrP**2
    TrP4 = TrP2**2

    # len(TrP) = len(TrP2) = len(TrP4) = N
    n = len(TrP)
    K = np.arange(100, n//20 + n//1000, n//1000)

    errTrP = []
    errchi = []
    errQ = []

    for k in K:
        # blocking for primary observables
        TrP_blocks = get_blocks(TrP, k)
        TrP2_blocks = get_blocks(TrP2, k)
        TrP4_blocks = get_blocks(TrP4, k)

        errTrP.append(np.sqrt(np.var(np.mean(TrP_blocks, axis = 1))/(n//k)))

        # blocking for secondary observables
        TrP_BS = bootstrap(np.mean(TrP_blocks, axis = 1), NBS)
        TrP2_BS = bootstrap(np.mean(TrP2_blocks, axis = 1), NBS)
        TrP4_BS = bootstrap(np.mean(TrP4_blocks, axis = 1), NBS)

        chi = np.mean(TrP2_BS, axis = 1) - np.mean(TrP_BS, axis = 1)**2
        Q = np.mean(TrP4_BS, axis = 1)/np.mean(TrP2_BS, axis = 1)**2

        errchi.append(np.sqrt(np.var(chi)))
        errQ.append(np.sqrt(np.var(Q)))

    filename = filename.replace('.dat', '.png')

    plt.xlabel('K')
    plt.ylabel('$err_{P}$')
    plt.title('$P$ error as a function of the block size $K$')
    plt.plot(K, errTrP, marker = "o", markersize = 0, linewidth = 2)
    plt.savefig(path + "/plots/binning/TrP_" + filename, facecolor='w')
    plt.close()

    plt.xlabel('K')
    plt.ylabel('$err_{\chi}$')
    plt.title('$\chi$ error as a function of the block size $K$')
    plt.plot(K, errchi, marker = "o", markersize = 0, linewidth = 2)
    plt.savefig(path + "/plots/binning/chi_" + filename, facecolor='w')
    plt.close()

    plt.xlabel('K')
    plt.ylabel('$err_{Q}$')
    plt.title('$Q$ error as a function of the block size $K$')
    plt.plot(K, errQ, marker = "o", markersize = 0, linewidth = 2)
    plt.savefig(path + "/plots/binning/Q_" + filename, facecolor='w')
    plt.close()








    