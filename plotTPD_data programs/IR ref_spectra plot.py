import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import seaborn as sns
import os.path as ospath
import re
sns.set()
sns.set_context("poster")

"for reading and normalizing NIST IR spectra"

# Param
shiftdown = False

def normalize_wrt(X, x_max_val):
    """
    Leaving this as a function in case i need it in the future... Normalizes with respect to the value you want. Not
    necessarily the max value in the column
    :param X:
    :param x_max_val:
    :return:
    """
    # TODO may need to fix normalization
    x_norm = (X - X.min(axis=0)) / float((x_max_val.values - X.min(axis=0).values))

    return x_norm

# Main begins
root = tk.Tk()
root.withdraw()
file_path1 = filedialog.askopenfilenames(filetypes=(('All files', '*.*'), ('JCamp files', '*.jdx'), ('Data files', '*.dpt')),
                                         title='Select Input File(s)')

# nist_spectrum = '~/PythonProjects/IRAS_plot/IRAS/Furfural work/Pt(100)/IR data/Furfural_liquid_IR_nist.jdx'
molname = pd.read_csv("anisole IR_solution.jdx",delimiter=None,nrows=0).columns

if len(molname) ==2:
    # assumes len(molname) == 2 potential breakage here...
    molname = molname[0].strip('##TITLE=') + molname[1]
else:
    molname = molname[0].strip('##TITLE=')

nist = pd.read_csv(file_path1[0], sep=' ', skiprows=37, skipfooter=1, header=None, index_col=0, engine='python' )
# nist = pd.read_csv(nist_spectrum, sep=' ', skiprows=37, skipfooter=2, names =['wave', 'freq1', 'freq2', 'freq3', 'freq4', 'freq5'],index_col = 0, engine='python' )

# convert transmittance to absorbance using: A = 2-log10(%T)
dx = 0.921377
# dx = 0.954330
wave = np.concatenate(np.array(list(map(lambda x: np.array(x)+dx*np.array([0,1,2,3,4]), nist.index.values))))
wave = wave.reshape((len(wave), 1))

nist = np.ndarray.flatten(nist.values)
nist = nist.reshape((len(nist),1))
# rm nans
nist = nist[~np.isnan(nist)]
wave= wave[:len(nist)]

nist_absorb = 2 - np.log10(nist*100)
# rm nan vals
nist_absorb = nist_absorb[~np.isnan(nist_absorb)]
nist_absorb = nist_absorb.reshape((len(nist_absorb),1))

wave = wave[:len(nist_absorb)]
# normalize the FTIR plot
# nist_absorb_norm = preprocessing.MinMaxScaler().fit_transform(nist_absorb)
fig, ax = plt.subplots(num='IR Overlay')
molecule = file_path1[0].rsplit('/')[-1].rstrip('.0.dpt').split(' ')[0]




plt.legend()
plt.show()