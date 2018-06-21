import matplotlib.pyplot as plt
import pandas as pd


def norm_df(df):
    norm_ = (df - df.min())/(df.max() - df.min())
    return norm_

bigdose = pd.read_csv('GUA_1E-08_140 sec_big dose.0 - Copy.dpt', sep='\t')
vapor = pd.read_csv("gua vapor1.0.dpt", sep='\t')
k100 = pd.read_csv('GUA_8e-09_90 sec _seq anneal_anneal to 100 K.0.dpt', sep='\t')
liquid= pd.read_csv('Guaiacol_Thin_Area.csv', header=None)
dft = pd.read_csv('Guaiacol - Spectrum.csv',header=None, usecols=[4, 5])

col = ['freq', 'inten']

bigdose.columns = col
vapor.columns = col
k100.columns = col
liquid.columns = col
dft.columns = col

# vap = vapor.loc[vapor['freq'] > 900].copy()
vap = vapor.copy()

bigdose['inten'] = norm_df(bigdose['inten'])
vap['inten'] = norm_df(vap['inten'])
k100['inten'] = norm_df(k100['inten'])
liquid['inten'] = norm_df(liquid['inten'])
dft['inten'] = norm_df(dft['inten'])

fig, ax = plt.subplots()

# bigdose.plot(x='freq', y='inten', ax=ax, label='bigdose')
vap.plot(x='freq', y='inten', ax=ax, label='vapor')
# k100.plot(x='freq', y='inten', ax=ax, label='100 K')
liquid.plot(x='freq', y='inten', ax=ax, label='liquid')
# dft.plot(x='freq', y='inten', ax=ax, label='dft')

plt.show()