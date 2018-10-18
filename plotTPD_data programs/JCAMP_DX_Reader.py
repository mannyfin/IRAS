import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


os.chdir('HOAc work\\HOAc vapor phase 642018')
fname = 'NIST 64-19-7-IR.jdx'

# extract header information
header_info = pd.read_csv(fname, sep='##', header=0, nrows = 36, engine='python')
temp = header_info.iloc[:,1]
temp.dropna(inplace=True)

molecule_name = temp.name[len('TITLE='):]
# nrows = temp.shape[0]

for row in temp:
    if 'DELTAX=' in row:
        dx = float(row[len('DELTAX='):])

data = pd.read_csv(fname, sep=' ', skiprows=37, skipfooter=1, header=None, index_col=0, engine='python')


wave = np.concatenate(np.array(list(map(lambda x: np.array(x)+dx*np.array([0,1,2,3,4]), data.index.values))))
wave = wave.reshape((len(wave), 1))

nist = np.ndarray.flatten(data.values)
nist = nist.reshape((len(nist),1))
# rm nans
nist = nist[~np.isnan(nist)]
wave= wave[:len(nist)]

nist_absorb = 2 - np.log10(nist*100)
# rm nan vals
nist_absorb = nist_absorb[~np.isnan(nist_absorb)]
nist_absorb = nist_absorb.reshape((len(nist_absorb),1))

wave = wave[:len(nist_absorb)]


# read raw gas phase HOAc data

os.chdir("vapor phase 642018")
raw_data = pd.read_excel("IR gas phase HOAc.xlsx")


fig, ax = plt.subplots(num=molecule_name)
nist_plot, = ax.plot(wave, nist_absorb, label='nist')
experiment_plot, = ax.plot(raw_data['Wavenumber'].iloc[:3250], raw_data['Intensity'].iloc[:3250], label='experiment')
plt.legend(handles=[nist_plot, experiment_plot])
plt.show()