import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import holoviews as hv
hv.extension()

Edes = 150e3 #j/mol

T = np.arange(100,600,0.1)
# dNdT = np.zeros(T.shape)
nu = 1e13 #first order
init_coverage=[1e15, 5e14, 2e14]

order =1
beta = 3

def polanyi_wigner(T, init_coverage, Edes, beta, order, nu):
    R = 8.314  # j/molK
    dNdT = np.zeros((T.shape[0], len(init_coverage)))
    coverage = init_coverage
    for idx1, coverage in enumerate(init_coverage):

        for idx, val in enumerate(T):

            dNdT[idx][idx1] = nu/(beta)*(coverage**order)*np.exp(-Edes/(R*val))
            if coverage <=0:
                coverage = 0
            else:
                coverage -= val*dNdT[idx][idx1]

    fig, ax = plt.subplots()
    ax.plot(T, dNdT)

    # return hv.Curve(polanyi_wigner(T, init_coverage, Edes, beta, order, nu))
    return 0


out = polanyi_wigner(T, init_coverage, Edes, beta, order, nu)
