import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

"quick plot of IR spectra"

colnames = ['Wavenumber', 'Intensity']

# Select the rest
root = tk.Tk()
root.withdraw()
file_path1 = filedialog.askopenfilenames(filetypes=(('All files', '*.*'), ('Data files', '*.dpt')),
                                         title='Select Input File(s)')
fig, ax = plt.subplots()
filelist = []
for file in file_path1:
    IR_spectra = pd.read_csv(file, '\t', header=None, names=colnames)
    IR_spectra.set_index(colnames[0], inplace=True)
    ax.plot(IR_spectra)
    filelist.append(file.rsplit('/')[-1].rstrip('.0.dpt'))
ax.legend(filelist)
plt.show()

# i use print('hi') as a quick debug line to test things out
print('hi')