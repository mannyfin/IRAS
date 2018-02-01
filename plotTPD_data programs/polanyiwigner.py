import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import holoviews as hv
hv.extension()



def polanyi_wigner(T, init_coverage, Edes, beta, order, nu=None, disp=False):
    # TODO unpack orders if multiple are given as args
    R = 8.314  # j/molK
    order_dict = {0: 1e28, 0.5: 3e20, 1: 1e13, 2: 1e-2}
    if nu is None:
        nu  = order_dict.get(order,1e13)
    dNdT = np.zeros((T.shape[0], len(init_coverage)))

    coverage = init_coverage

    for idx1, coverage in enumerate(init_coverage):

        for idx, val in enumerate(T):

            dNdT[idx][idx1] = nu/(beta)*(coverage**order)*np.exp(-Edes/(R*val))
            # dNdT[idx][idx1] = nu/(beta)*(np.float_power(coverage,order))*np.exp(-Edes/(R*val))
            if coverage <=0:
                coverage = 0
            else:
                coverage -= val*dNdT[idx][idx1]

    fig, ax = plt.subplots()
    ax.plot(T, dNdT)

    if disp is True:
        plt.show()
    else:
        return

    # return hv.Curve(polanyi_wigner(T, init_coverage, Edes, beta, order, nu))
    return

order = 1
Edes = 100e3 #j/mol
T = np.arange(100,500,0.1)
initial_coverage=[1e15, 5e14, 2e14]
beta = 3

out = polanyi_wigner(T, initial_coverage, Edes, beta, order, disp=True)
