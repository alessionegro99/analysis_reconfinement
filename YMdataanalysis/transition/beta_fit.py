from pseudo_header import *
from sympy import *

N_t = np.array([4, 5, 6, 7, 8, 9])

beta = np.array([6.53661, 8.07042, 9.60265, 11.1194, 12.6348, 14.1418])
s_beta = np.array([0.00013, 0.00038, 0.00049, 0.00029, 0.00040, 0.00068])

def linear(x, a, b):
    return a + b*x

def a_SU2(beta):
    return 1.324/beta + 1.20/beta**2

def T_s(a, N_t):
    return 1/(a*N_t)

p, cov = curve_fit(linear, N_t, beta, sigma = s_beta, absolute_sigma = True)

a = p[0]
b = p[1]
s_a = np.sqrt(cov[0][0])
s_b = np.sqrt(cov[1][1])

y = linear(N_t, a, b)

plt.rcParams["figure.figsize"] = [16, 9]
plt.rcParams["figure.autolayout"] = True
plt.grid
plt.xlabel('N_t')
plt.ylabel('beta_c')
plt.title('beta_c(N_t)')
plt.plot(N_t, beta, color = "orange", marker = "^", markersize = 3, linewidth = 1)
plt.errorbar(N_t, beta, s_beta, color = "orange", capsize = 5)
plt.plot(N_t, linear(N_t, a, b), color = "purple", linewidth = 3)
plt.savefig(homeDir + '/Documents/thesis/simulation_analysis/simulation_plots/beta_c(N_t).png', facecolor='w')
plt.close()

beta_6 = a + b*6

print(a_SU2(9.60265))

T = 1/(a_SU2(9.60265)*6)*0.62

print(1/(a_SU2(9.60265)*6)*0.62)

x, y = symbols('x y') 

y = x**2-x*6*T*1.324-1.20*6*T

result = solve(Eq(y, 0))
print(result)