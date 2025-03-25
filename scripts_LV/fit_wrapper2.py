import numpy as np
from scipy.optimize import curve_fit, least_squares
from scipy.stats import chi2

from format_output import format_uncertainty

class Fit_results:
    def __init__(self,
                 opt: np.ndarray,
                 cov: np.ndarray,
                 err_opt: np.ndarray,
                 chi_sqr: float, 
                 num_dof: int):
        
        self.opt = opt
        self.cov = cov

        self.err_opt = err_opt
        self.chi_sqr = chi_sqr
        self.num_dof = num_dof

    @property
    def p_value(self):
        return 1 - chi2.cdf(self.chi_sqr, self.num_dof)

    def __str__(self) -> str:
        return " ".join(format_uncertainty(val, err) for val, err in zip(self.opt, self.err_opt))
    
    def verbose_print(self):
        print("Best fit parameters:")
        print(self)
        print()
        print("Covariance matrix:")
        print(self.cov)
        print()
        print(f"chi_sqr = {self.chi_sqr:.2f}, num_dof = {self.num_dof}, p_value = {self.p_value:.2%}")
        print()

    def __iter__(self):
        yield self.opt
        yield self.cov
        yield self.err_opt
        yield self.chi_sqr
        yield self.num_dof
        yield self.p_value
    
class Simple_fit_results(Fit_results):
    def __init__(self, opt: np.ndarray, cov: np.ndarray, chi_sqr: float, num_dof: int):
        self.opt = opt
        self.cov = cov

        self.chi_sqr = chi_sqr
        self.num_dof = num_dof

    @property
    def err_opt(self):
        return np.sqrt(self.cov.diagonal())

def uncorrelated_fit(fun, x_data, y_data, err_y, err_x=None, fun_deriv=None, data_container=None, print_results=False, **kwargs) \
    -> Simple_fit_results:

    if data_container is not None:
        x_data = data_container[x_data]
        y_data = data_container[y_data]
        err_y  = data_container[err_y]

        if err_x is not None:
            err_x = data_container[err_x]

    opt, cov = curve_fit(fun, x_data, y_data, sigma=err_y, absolute_sigma=True, **kwargs)

    if err_x is not None:
        if fun_deriv is None:
            raise ValueError("to take into account errors on x, the derivative (fun_deriv) is needed")
        eff_err = np.sqrt(err_y**2 + fun_deriv(x_data, *opt)**2 * err_x**2)
        opt, cov = curve_fit(fun, x_data, y_data, sigma=eff_err, absolute_sigma=True, **kwargs)
    else:
        eff_err = err_y

    residuals = (y_data - fun(x_data, *opt))
    chi_sqr = np.sum((residuals / eff_err)**2)
    num_dof = len(y_data) - len(opt)

    results = Simple_fit_results(opt, cov, chi_sqr, num_dof)

    if print_results: results.verbose_print()

    return results

def correlated_fit(fun, x_data, y_data, cov_y, print_results=False, **kwargs) -> Simple_fit_results:
    
    opt, cov = curve_fit(fun, x_data, y_data, sigma=cov_y, absolute_sigma=True, **kwargs)

    residuals = (y_data - fun(x_data, *opt))
    chi_sqr = np.sum(residuals * (np.linalg.inv(cov_y) @ residuals))
    num_dof = len(y_data) - len(opt)

    results = Simple_fit_results(opt, cov, chi_sqr, num_dof)

    if print_results: results.verbose_print()

    return results

def _norm_residuals(opt, fun, fun_deriv, x_data, y_data, err_x, err_y):
    eff_err = np.sqrt(err_y**2 + fun_deriv(x_data, *opt)**2 * err_x**2)
    return (fun(x_data, *opt) - y_data) / eff_err

def x_errors_exact_fit(fun, x_data, y_data, err_y, err_x, fun_deriv, p0=None, data_container=None, print_results=False, **kwargs) \
    -> Simple_fit_results:

    if data_container is not None:
        x_data = data_container[x_data]
        y_data = data_container[y_data]
        err_y  = data_container[err_y]
        err_x  = data_container[err_x]

    if p0 is None:
        p0 = [0] * (fun.__code__.co_argcount - 1)

    res = least_squares(lambda opt: _norm_residuals(opt, fun, fun_deriv, x_data, y_data, err_x, err_y), p0, **kwargs)
    opt = res.x

    chi_sqr = 2 * res.cost
    num_dof = len(y_data) - len(opt)

    cov = np.linalg.inv(res.jac.T @ res.jac)

    results = Simple_fit_results(opt, cov, chi_sqr, num_dof)

    if print_results: results.verbose_print()

    return results

if __name__ == '__main__':
    
    import pandas as pd
    
    size = 100

    pure_x = np.linspace(1, 4, size)
    pure_y = pure_x**2

    data = {    'x': pure_x,
                'y': pure_y,
            'err_x': 0.1 * np.ones(shape=(size,)),
            'err_y': np.linspace(0.1, 0.4, size)
            }
    
    data = pd.DataFrame(data)
    data.x += data.err_x * np.random.normal(size=data.x.size)
    data.y += data.err_y * np.random.normal(size=data.y.size)

    def direct_fun(x, *pars):
        return pars[0] + pars[1] * x**2
    
    def direct_der(x, *pars):
        return 2 * pars[1] * x
    
    def inverse_fun(y, *pars):
        return np.sqrt((y - pars[0]) / pars[1])

    def inverse_der(y, *pars):
        return 1. / (2 * pars[1] * inverse_fun(y, *pars))

    p0 = [0, 1]

    fit_res = np.zeros

    fit_res1 = uncorrelated_fit(direct_fun, 'x', 'y', 'err_y', data_container=data, p0=p0)
    print("no x error:", fit_res1)

    fit_res2 = uncorrelated_fit(direct_fun, 'x', 'y', 'err_y', err_x='err_x', fun_deriv=direct_der, data_container=data, p0=p0)
    print("direct:    ", fit_res2)

    fit_res3 = uncorrelated_fit(inverse_fun, 'y', 'x', 'err_x', err_x='err_y', fun_deriv=inverse_der, data_container=data, p0=p0)
    print("inverse:   ", fit_res3)

    fit_res4 = uncorrelated_fit(inverse_fun, 'y', 'x', 'err_x', data_container=data, p0=p0)
    print("no y error:", fit_res4)

    fit_res5 = x_errors_exact_fit(direct_fun, 'x', 'y', 'err_y', 'err_x', direct_der, data_container=data, p0=p0)
    print("xt direct: ", fit_res5)

    fit_res6 = x_errors_exact_fit(inverse_fun, 'y', 'x', 'err_x', 'err_y', inverse_der, data_container=data, p0=p0)
    print("xt inverse:", fit_res6)