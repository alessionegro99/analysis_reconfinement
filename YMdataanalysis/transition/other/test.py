from pseudo_header import *

print("TEST")
ics = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ipsilon = [10, 10.0001, 9.99999, 10, 10.0001, 9.99998, 10.0002, 10.0001, 9.99999, 10]
sipsilon = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

def const(x, a):
	return a

p_test, cov_test = curve_fit(const, ics, ipsilon, sigma = sipsilon, absolute_sigma = True)

print(p_test)
print(np.sqrt(cov_test))

print("TEST")