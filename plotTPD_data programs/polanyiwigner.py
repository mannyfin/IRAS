import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import holoviews as hv
hv.extension()
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


def params_dict(params):
    """
    set some default parameters into the params dict
    :return:
    """

    params_default = {'model': 'None', 'Edes': 50, 'beta': 3, 'nu': 1e+28, 'order': 0, 'A': 0, 'B': 0, 'C': 0, 'U': 0,
                      'monolayer': 1e15}
    for v in params:
        # params_default[k] = v
        params_default[v] = params[v]
    return params_default


def models(coverage, val, R, params):
    """
    Calculates dNdT for various models defined below
    :param model: Choices are: 'None', 'Linear', 'Albano', 'Modified Albano', 'Work Function', 'Power'
    :param params: parameters to the model
    :return: dNdT
    """
    prefactor = (params['nu'] / params['beta']) * (coverage ** params['order'])
    fractional_cov = coverage/params['monolayer']
    model_list = {'None': prefactor * np.exp(-params['Edes'] / (R * val)),
                  'Linear': prefactor * np.exp(-(params['Edes']- params['A']*fractional_cov) / (R * val)),
                  'Albano': prefactor * np.exp(-(params['Edes']-(9*(params['U']**2)*(fractional_cov**(3/2))/((1+9*params['A']*(fractional_cov**(3/2)))**2)))/(R * val)),
                  'Modified Albano': prefactor * np.exp(-(params['Edes'] - 9*((params['A']*fractional_cov + params['B'])**2)*(fractional_cov**(3/2))) / (R * val)),
                  'Work Function': prefactor * np.exp(-(params['Edes']- (params['A']*fractional_cov**3 + params['B']*fractional_cov**2 + params['C'] * fractional_cov))/ (R * val)),
                  'Power': prefactor * np.exp(-(params['Edes'] - params['A']*fractional_cov**params['B'])/ (R * val))
                  }
    try:
        # params['model'] = 'None'
        return model_list[params['model']]


    except ValueError as e:
        print('model not listed or used correctly. Check inputs')

# def polanyi_wigner(T, init_coverage, Edes, beta, order, nu=None, disp=False):
def polanyi_wigner(T, init_coverage, params, disp=False):
    # TODO unpack orders if multiple are given as args

    # nu, order = params['nu'], params['order']

    R = 8.314/1e3  # kj/molK
    order_dict = {0: 1e28, 0.5: 3e20, 1: 1e13, 2: 1e-2}
    # if params['nu'] is None:
    params['nu'] = order_dict.get(params['order'] , 1e13)

    params = params_dict(params)

    dNdT = np.zeros((T.shape[0], len(init_coverage)))

    coverage_lst = np.zeros((T.shape[0], len(init_coverage)))
    dT = np.concatenate(([0], np.diff(T)))
    # for looping over multiple coverages
    for idx1, coverage in enumerate(init_coverage):
        # for a particular coverage, loop over T
        for idx, val in enumerate(T):

            # TODO: issue for zero order in that at some point coverage = 0 but the exp decreases as T increases
            # dNdT[idx][idx1] = nu / (beta) * (coverage ** order) * np.exp(-Edes / (R * val))
            dNdT[idx][idx1] = models(coverage, val, R, params)



            # print(dNdT[idx][idx1])
            # dNdT[idx][idx1] = nu/(beta)*(np.float_power(coverage,order))*np.exp(-Edes/(R*val))

            # this may be needed for debugging:
            # if idx % 5 == 0:
            #     print(dNdT[idx][idx1])
            #     print('nu: {0}, \nbeta: {1},\ncoverage: {2},\nexp term: {3}, \nT: {4}'
            #           .format(nu, beta, coverage,np.exp(-Edes / (R * val)), val))
            if coverage <= 0:
                coverage = 0
                dNdT[idx][idx1] = 0
                coverage_lst[idx][idx1] = coverage
                break
            else:
                coverage_lst[idx][idx1] = coverage
                # coverage -= val * dNdT[idx][idx1]  #this was incorrect. It should be dT* dN/dT, not T*dN/dT
                coverage -= dT[idx]* dNdT[idx][idx1]
    # # test
    # fig2, ax2 = plt.subplots()
    # cov = np.array(coverage_lst)
    # out = cov[:,np.newaxis]*dNdT
    # ax2.plot(T,out)
    Tmax = [T[np.argmax(dNdT[:, i])] for i in range(len(init_coverage))]
    print(*Tmax, sep=' K\n')
    # print(Tmax, sep='\n')

    if disp is True:
        fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(5, 7))
        ax1.plot(T, dNdT)
        ax1.set_xlabel('Temperature')
        ax1.set_ylabel(('-dN/dT'))

        ax2.plot(T, coverage_lst)
        ax2.set_xlabel('Temperature')
        ax2.set_ylabel('N(T)')
        # fig, ax = plt.subplots(1,1)
        # ax.plot(T, dNdT)
        # plt.xlabel('Temperature')
        # plt.ylabel('dN/dT')
        # fig1, ax1 = plt.subplots()
        # ax1.plot(T, coverage_lst)

        plt.show()
    else:
        return Tmax, T, dNdT

    # assert len(out) == len(T)
    # fig2, ax2 = plt.subplots()
    # ax2.plot(T,out)

    # return hv.Curve(polanyi_wigner(T, init_coverage, Edes, beta, order, nu))
    return Tmax, T, dNdT

# order = 0
# Edes = 50 #kj/mol, a good value is 50e3
T = np.linspace(100,500,10000)
initial_coverage=[1e15, 5e14, 2e14, 5e13]
# initial_coverage=[1.6e14]
# beta = 3  # K/s

"""
if using anything other than 'None' model, the monolayer coverage MUST BE PROVIDED  
"""
monolayer_coverage = 1.1e15
params = {'model':'None', 'Edes': 51, 'beta': 3, 'order': 1, 'A':2, 'B':3, 'C':4, 'monolayer': monolayer_coverage}

# initial_coverage=[2e14]
# beta = 3

# out = polanyi_wigner(T, initial_coverage, Edes, beta, order, disp=True)
out = polanyi_wigner(T, initial_coverage, params, disp=True)

# for Edes in np.arange(48, 55, 0.1):
#     out = polanyi_wigner(T, initial_coverage, Edes, beta, order, disp=False)
# #     print(out)
# #     print(Edes)
#     print('Edes: {0:4.2f} kJ/mol, Tpeak: {1:0.2f} K'.format(Edes, out[0][0]))
#     if (np.abs(out[0][0]-200)<=0.2):
#         print('Edes is: ' +str(Edes))
#         break
#     elif out[0][0]>200:
#         break