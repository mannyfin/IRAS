import pandas as pd
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import seaborn
"""
1. change dir
2. read in file with pd.read_csv( , sep = '\t', header=None)
3. rename columns with  df.columns = ['freq', 'amp']
4. df.reset_index('freq')
5. df =  df.loc[:800] to choose only data above 800 cm^-1
6. find min of the df using df.min() and also check the index with df.idxmin()
7. Repeat 2-5 with another file
8. Take ratio of the min of the most recent read file to reference (initial one) min
9. water_subtracted_df = new_df - ratio*ref_df
10. water_subtracted_df.plot() 

"""
# TODO add input validation and stack plots
# step 1
root = tk.Tk()
root.withdraw()
file_path1 = filedialog.askopenfilenames(filetypes=(('DPT files', '*.dpt'), ('All files', '*.*'), ('Text files', '*.txt')),
                                         title='Select REFERENCE Input File(s)')
# step 2 & 3
colnames=['freq', 'amp']
ref_df = pd.read_csv(file_path1[0], sep='\t', header=None, names=colnames)
# step 4
ref_df.set_index('freq', inplace=True)
# step 5
ref_df = ref_df.loc[:700]
# step 6
refmin = ref_df.idxmin()

# select second file(s)
root = tk.Tk()
root.withdraw()
file_path2 = filedialog.askopenfilenames(filetypes=(('DPT files', '*.dpt'), ('All files', '*.*'), ('Text files', '*.txt')),
                                         title='Select EXPERIMENT Input File(s)')
# step 7
for files in file_path2:
    # step 2, 3+
    exp_df = pd.read_csv(files, sep='\t', header=None, names=colnames)
    filename = '.'.join(files.split('/')[-1].split('.')[0:2])
    # step 4+
    exp_df.set_index('freq', inplace=True)
    # step 5+
    exp_df = exp_df.loc[:700]
    # step 6+
    expmin = exp_df.idxmin()

    # now compare if the indices match before taking the ratio. Otherwise dont take the ratio

    if expmin.values != refmin.values:
        print('\nmin indices dont match! for ' + files + '\n')
    else:
        # step 8
        ratio = exp_df.min()/ref_df.min()
        # step 9
        water_subtracted_df = exp_df - ratio*ref_df
        # water_subtracted_df.plot(title=filename)
        water_subtracted_df.plot(title=filename)
        # plt.hold()
        water_subtracted_df.to_csv(filename+'.dpt',sep='\t', header=None)
        print('\nCompleted ' + filename + '\n')

plt.show()