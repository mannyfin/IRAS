import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import os
"quick plot of IR spectra from the Bruker IR"

colnames = ['Wavenumber', 'Intensity']

# Select the rest
root = tk.Tk()
root.withdraw()
file_path1 = filedialog.askopenfilenames(filetypes=(('All files', '*.*'), ('Data files', '*.dpt')),
                                         title='Select Input File(s)')
# path to files
pathlocation = file_path1[0].rstrip(os.path.basename(file_path1[0]))
os.chdir(pathlocation)

fig, ax = plt.subplots()
filelist = []
ir_writer = pd.ExcelWriter('IR.xlsx')
temp_df = []
cols = []
for file in file_path1:
    IR_spectra = pd.read_csv(file, '\t', header=None, names=colnames, dtype=float)
    IR_spectra.set_index(colnames[0], inplace=True)
    ax.plot(IR_spectra)

    file = file.rsplit('/')[-1].rstrip('.0.dpt.txt')
    filelist.append(file)
    # puts all the IR files together in an excel file
    cols.append(file[-5:])
    IR_spectra.to_excel(ir_writer,sheet_name=cols[-1])
    temp_df.append(IR_spectra)

try:
# saves combined df
    combined = pd.concat(temp_df, axis=1, keys=cols)
    combined.to_excel(ir_writer, sheet_name='Combined')
    ir_writer.save()
except:
    combined = pd.concat(temp_df, axis=1, keys=cols, ignore_index=True)
    combined.columns = cols
    combined.to_excel(ir_writer, sheet_name='Combined')
    ir_writer.save()
ax.legend(filelist)
plt.show()

# i use print('hi') as a quick debug line to test things out
print('hi')
