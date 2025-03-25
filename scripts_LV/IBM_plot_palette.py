#import logging

from matplotlib import pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', size=17)
plt.rc('font', family='serif') # usual LaTeX font

color_dict = {\
    0: '#000000',
    1: '#3D5ACA',
    2: '#A71D60',
    3: '#C78A00',
    4: '#4D3B79',
    5: '#BD4900',
    
}

bright_color_dict = {\
    0: '#000000',
    1: '#648fff',
    2: '#dc267f',
    3: '#ffb000',
    4: '#785ef0',
    5: '#fe6100',
}

marker_dict = {\
    0: 's',
    1: 'o',
    2: 'D',
    3: 'v',
    4: '^',
    5: 'p',
}

lines_dict = {\
    0: 'solid',
    1: 'dashed',
    2: 'dashdot',
    3: 'dotted',
    4: 'solid',
    5: 'dashed'
}

def data(palette_idx=1, **kwargs) -> dict:

    try:
        color = color_dict[palette_idx]
    except KeyError:
        color = 'darkblue'

    try:
        marker = marker_dict[palette_idx]
    except KeyError:
        marker = 'o'

    pars = dict()
    pars['linestyle'] = 'none'
    pars['color'] = color
    pars['marker'] = marker
    pars['markersize'] = 8
    pars['elinewidth'] = 1.5
    pars['capsize'] = 3.5
    pars['markeredgecolor'] = color
    pars['markerfacecolor'] = 'none'
    pars.update(kwargs)

    return pars

def fit(palette_idx=0, **kwargs):

    try:
        linestyle = lines_dict[palette_idx]
    except KeyError:
        linestyle = 'dashed'

    try:
        color = bright_color_dict[palette_idx]
    except KeyError:
        color = 'black'

    pars = dict()
    pars['linestyle'] = linestyle
    pars['color'] = color
    pars['linewidth'] = 1.2
    pars.update(kwargs)
    return pars

def results(palette_idx=-1, **kwargs):

    try:
        color = color_dict[palette_idx]
    except KeyError:
        color = 'red'

    try:
        marker = marker_dict[palette_idx]
    except KeyError:
        marker = 's'

    pars = dict()
    pars['linestyle'] = 'none'
    pars['color'] = color
    pars['marker'] = marker
    pars['markersize'] = 8
    pars['elinewidth'] = 1.5
    pars['capsize'] = 3.5
    pars['markeredgecolor'] = color
    pars['markerfacecolor'] = color
    pars.update(kwargs)

    return pars

def conf_band(palette_idx=1, **kwargs):

    try:
        color = bright_color_dict[palette_idx]
    except KeyError:
        color = 'blue'

    pars = dict()
    pars['facecolor'] = color
    pars['zorder'] = 1
    pars['alpha'] = 0.3
    pars.update(kwargs)
    return pars


if __name__ == '__main__':
    import numpy as np
    from scipy.special import chebyt
    xxx = np.linspace(-1, 1, 10)
    rrr = 0.01 * np.ones(xxx.size)
    yy1 = chebyt(1)(xxx) + rrr * np.random.normal(size=xxx.size)
    yy2 = chebyt(2)(xxx) + rrr * np.random.normal(size=xxx.size)
    yy3 = chebyt(3)(xxx) + rrr * np.random.normal(size=xxx.size)
    yy4 = chebyt(4)(xxx) + rrr * np.random.normal(size=xxx.size)
    yy5 = chebyt(5)(xxx) + rrr * np.random.normal(size=xxx.size)

    x_plot = np.linspace(-1, 1, 500)
    y_plo1 = chebyt(1)(x_plot)
    y_plo2 = chebyt(2)(x_plot)
    y_plo3 = chebyt(3)(x_plot)
    y_plo4 = chebyt(4)(x_plot)
    y_plo5 = chebyt(5)(x_plot)

    x00 = 2*np.pi
    r00 = 0.1
    y10 = 0
    y20 = 1

    plt.figure(0)
    plt.errorbar(xxx, yy1, rrr, **data(1), label='cheby1')
    plt.plot(x_plot, y_plo1, **fit(1))
    plt.errorbar(xxx, yy2, rrr, **data(2), label='cheby2')
    plt.plot(x_plot, y_plo2, **fit(2))
    plt.errorbar(xxx, yy3, rrr, **data(3), label='cheby3')
    plt.plot(x_plot, y_plo3, **fit(3))
    plt.errorbar(xxx, yy4, rrr, **data(4), label='cheby4')
    plt.plot(x_plot, y_plo4, **fit(4))
    plt.errorbar(xxx, yy5, rrr, **data(5), label='cheby5')
    plt.plot(x_plot, y_plo5, **fit(5))

    # plt.fill_between(x_plot, y_plot-0.1, y_plot+0.1, **conf_band())

    plt.legend()

    plt.show()
