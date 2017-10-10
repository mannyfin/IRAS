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


# Param
shiftdown = True

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

# nist_spectrum = 'F:/PythonProjects/IRAS_plot/IRAS/Furfural work/Pt(100)/IR data/Furfural_liquid_IR_nist.jdx'

nist = pd.read_csv(file_path1[0], sep=' ', skiprows=37, skipfooter=1, header=None, index_col=0, engine='python' )
# nist = pd.read_csv(nist_spectrum, sep=' ', skiprows=37, skipfooter=2, names =['wave', 'freq1', 'freq2', 'freq3', 'freq4', 'freq5'],index_col = 0, engine='python' )

# convert transmittance to absorbance using: A = 2-log10(%T)
dx = 0.954330
wave = np.concatenate(np.array(list(map(lambda x: np.array(x)+dx*np.array([0,1,2,3,4]), nist.index.values))))
wave = wave.reshape((len(wave), 1))

nist = np.ndarray.flatten(nist.values)
nist = nist.reshape((len(nist),1))

nist_absorb = 2 - np.log10(nist*100)
# rm nan vals
nist_absorb = nist_absorb[~np.isnan(nist_absorb)]
nist_absorb = nist_absorb.reshape((len(nist_absorb),1))

wave = wave[:len(nist_absorb)]
# normalize the FTIR plot
nist_absorb_norm = preprocessing.MinMaxScaler().fit_transform(nist_absorb)

if shiftdown is True:
    # shift the baseline down by taking avg of points at the end, which are approx flat
    shifted = nist_absorb_norm[np.where(wave>3700)[0]].mean()
    nist_absorb_norm = nist_absorb_norm - shifted


# Select the rest
root = tk.Tk()
root.withdraw()
file_path1 = filedialog.askopenfilenames(filetypes=(('All files', '*.*'), ('JCamp files', '*.jdx'), ('Data files', '*.dpt')),
                                         title='Select Input File(s)')
colnames = ['wave', 'amp']
# current_palette = sns.color_palette("Paired", max(len(file_path1), 8))
# sns.set_palette(current_palette, n_colors=max(len(file_path1), 8))

fig, ax = plt.subplots(num='IR Overlay')
ax.plot(wave,nist_absorb_norm, label='NIST Reference Spectrum -- Liquid')

for file in file_path1:
    IR_df = pd.read_csv(file, sep='\t', header=None, names=colnames)
    IR_df.set_index('wave', inplace=True)
    IR_df = IR_df.loc[:700]
    # normalize wrt v(C=O) ald stretch
    ir_df_normalizing_val = IR_df.loc[IR_df.loc[1715:1660].idxmax()]
    normalized_IR = normalize_wrt(IR_df, ir_df_normalizing_val)

    label = ospath.basename(file)
    # label = re.findall('(\d\.\d .*?)\.', label)[0]

    if shiftdown is True:
        # shift the baseline down by taking avg of points at the end, which are approx flat
        shifted = normalized_IR.loc[:3700].mean()
        normalized_IR = normalized_IR - shifted


    ax.plot(normalized_IR, label=label)

plt.legend()
plt.show()