import matplotlib.pyplot as plt
import numpy as np

def file_path(Ns):
    return f"/home/negro/projects/reconfinement/analysis_reconfinement/02_output/L{str(Ns)}/xi_L.txt"

def main(NSS):
    plt.figure(figsize=(19.2, 10.8), dpi=100)
    colors = ['purple', 'orange', 'darkgreen', 'darkblue', 'orange']
    markers = ['o', 's', 'D', '^', 'v']

    for i, Ns in enumerate(NSS):
        try:
            with open(file_path(Ns), 'r') as file:
                HH = []
                xi_L = []
                d_xi_L = []
                
                for line in file:
                    values = line.strip().split()
                    HH.append(float(values[1]))
                    xi_L.append(float(values[2]))
                    d_xi_L.append(float(values[3]))
                
                plt.errorbar(HH, xi_L, yerr=d_xi_L, fmt=markers[i % len(markers)], color=colors[i % len(colors)], 
                             ecolor=colors[i % len(colors)], capsize=5, label=f'Ns={Ns}', markersize=12, markerfacecolor='none')
        except FileNotFoundError:
            print(f"File not found: {file_path(Ns)}")
            continue

    plt.xlabel('HH', fontsize=20)
    plt.ylabel('xi_L', fontsize=20)
    plt.title('Plot of xi_L with error bars for different Ns', fontsize=24)
    plt.legend(fontsize=16)
    plt.savefig('/home/negro/projects/reconfinement/analysis_reconfinement/02_output/xi_L_plot.png', bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    NSS = [64, 80, 96]
    main(NSS)