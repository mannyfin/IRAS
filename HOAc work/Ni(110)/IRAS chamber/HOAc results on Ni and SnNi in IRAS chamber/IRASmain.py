import pandas as pd
import os
from os import walk
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import numpy as np
import re

"""
New code not implemented yet
"""
root = tk.Tk()
root.withdraw()
file_path1 = filedialog.askopenfilenames(filetypes=(('All files', '*.*'), ('Data Point Table files', '*.dpt'),
                                                    ('Text files', '*.txt')), title='Select Input File(s)')

"""
New code not implemented yet
"""

#OLD CODE
# print('test')
# mypath = os.chdir('acetic acid export/acetic acid export')
#
#
# blah = []
# for (dirpath, dirnames, filenames) in walk(mypath):
#     blah.extend(filenames)
#     break
#

# start = '150K dose acetic acid-4-8torr 1 min-'
# end = '.0.dpt'
# headers = [blah[file_counter][len(start):-len(end)] for file_counter in range(0, len(blah))]
#
# concat_init = [pd.read_csv(blah[0], sep='\t')]
# concats = [ pd.read_csv(blah[file_counter], sep='\t', usecols=[1]) for file_counter in range(1, len(blah))]
# OLD CODE
#

headers = [file_path1[i][-file_path1[i][::-1].index('/') : -file_path1[i][::-1].index('.')-3] for i in range(len(file_path1))]

concat_init = [pd.read_csv(file_path1[0], sep='\t')]
concats = [ pd.read_csv(file_path1[file_counter], sep='\t', usecols=[1]) for file_counter in range(1, len(file_path1))]
# ### pd.read_csv(blah[1], sep='\t'),
test = pd.concat(concat_init + concats, axis=1)
test.columns = ['wavenumber'] + headers
indexed_df = test.set_index(['wavenumber'])
#
# difference_spectra = indexed_df.sub(indexed_df['200K'], axis=0).astype('float64')
#
# difference_spectra = difference_spectra.drop(difference_spectra[difference_spectra.index<750].index, axis =0)
# # hsv = plt.get_cmap('hsv')
# # colors = hsv(np.linspace(0, 1.0, len(kinds)))
# difference_spectra[difference_spectra.columns[2:-3]].plot(figsize=(15,10), colormap='jet').legend(loc="center left", bbox_to_anchor=(1, 0.5))

indexed_df.plot()

xcoords= [2930, 2848, 2334, 2362, 2260 ,2062, 1876, 1446, 1425, 968 ]
for xcoord in xcoords:
    plt.axvline(x=xcoord, color='k', linestyle='--')
    plt.text(x=xcoord, y=plt.ylim()[1], s=str(xcoord), verticalalignment='top')


plt.show()
print('test')

