import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import numpy as np

#TODO zero out graphs better
#TODO plot 0.1 and 0.2L for big multilayer curve

# Preliminary stuff
# Display of temp range on plots. These limits are null if there is more than one column unless otherwise specified
use_temp_limits = True
low_temp = 100
high_temp = 375
single_molecule_name = 'HOAC'
# any vertical dotted lines go here
dotted_lines = [204.7, 161, 395, 428]
# dotted_lines = [204.7, 161, 260, 395, 428]

# dict_values = dict({'HOAC':'61.297', 'CO':})


def rename_to_text(file_path):
    import os
    file = file_path.split('/')[-1]
    if file.endswith('.txt') is False:
        new_file_name = file_path+'.txt'
        os.rename(file_path, new_file_name)
        file_path = new_file_name
    filename = file
    return file_path, filename


def single_slope_subtract(file_read, num_points_to_average_beg=50,num_points_to_average_end=50 ):
    """
    
    :param file_read: df of file
    :param num_points_to_average_beg: 
    :param num_points_to_average_end: 
    :return: 
    """
    # single slope subtraction
    # num_points_to_average_beg = 50
    # num_points_to_average_end = 50

    # mean of first N points
    avg_y_beg = file_read.iloc[:num_points_to_average_beg].mean()

    # mean of last N points
    avg_y_end = file_read.iloc[-num_points_to_average_end:].mean()

    # x value for beginning (assume first xval)
    first_xval = file_read.first_valid_index()

    # x value for ending (assume last xval)
    last_xval = file_read.last_valid_index()

    slope = (avg_y_end - avg_y_beg) / (last_xval - first_xval)
    # y' = mx
    # caveat...only works with monitoring a single mass-- update 7/13/17 appears to have fixed this...
    # y_prime = pd.DataFrame(slope.values * file_read.index.values, columns=file_read.columns)

    y_prime = pd.DataFrame(np.matmul(file_read.index.values[:, np.newaxis],np.transpose(slope.values[:, np.newaxis])),
                           columns=file_read.columns)

    y_prime.index = file_read.index

    # first attempt at fix
    # y_prime = slope.values[0]*file_read.index+avg_y_beg

    difference = file_read - y_prime
    difference = difference - difference.iloc[:(num_points_to_average_beg)].mean()

    new_file_read = difference

    return new_file_read


def read_files(file):
    file_path, filename = rename_to_text(file)
    print(file_path)

    # read file
    file_read = pd.read_csv(file_path, sep='\t', header=3)

    # remove whitespace
    column_names = [file_read.keys()[i].lstrip() for i in range(0, len(file_read.keys()))]
    # rename columns
    file_read.columns = column_names
    # drop the time column and mse=8
    file_read = file_read.drop([column_names[0], column_names[-1]], axis=1)
    temp = file_read[file_read != 0]
    temp = temp.dropna(axis=0)


    file_read = file_read.dropna(axis=1)

    # for the bug in the labview that the temperature cuts out
    temp = file_read[file_read != 0]
    file_read = temp.dropna(axis=0)

    # set the index to be temperature
    file_read = file_read.set_index(file_read.keys()[0])

    return file_read, filename

# Main begins
root = tk.Tk()
root.withdraw()
file_path1 = filedialog.askopenfilenames(filetypes=(('All files', '*.*'), ('Text files', '*.txt')),
                                         title='Select Input File(s)')

for file in file_path1:

    file_read, filename = read_files(file=file)

    if use_temp_limits is True:
        # selects only appropriate temperature range
        file_read = file_read.loc[(file_read.index <= high_temp) & (file_read.index >= low_temp)]

    # only do below if there is only one column
    # if file_read.columns.__len__() is 1:
    #     new_file_read = single_slope_subtract(file_read)
    #
    # else:
    #     # this case is invoked if there are more than one column
    #
    #     new_file_read = single_slope_subtract(file_read)
    #
    #     # new_file_read = file_read

    # first slope subtraction
    new_file_read = single_slope_subtract(file_read)
    # baseline subtraction
    new_file_read = new_file_read - new_file_read.min()
    # a second slope subtraction
    new_file_read = single_slope_subtract(new_file_read,num_points_to_average_beg=20,num_points_to_average_end=20)

    # only for 1 column
    if file_read.columns.__len__() is 1:
    # plot the data
    # file_read.plot(x=file_read.index, figsize=(15,7))  # ylabel='QMS signal (a.u.)'
        ax = plt.figure(123, figsize=(15, 7))
        plt.plot(new_file_read, label=filename)

    # for multiple columns
    else:
        # ax = plt.figure(123, figsize=(15, 7))
        new_file_read.plot(figsize=(15, 7))
        # plt.plot(new_file_read)
        # plt.legend()
    # set y lower limit = 0
    axes.Axes.set_ylim(plt.gca(), bottom=0, auto=True)

    if use_temp_limits is True:
        axes.Axes.set_xlim(plt.gca(), left=low_temp, right=high_temp)

    # file_read.plot()

    plt.ylabel('QMS signal (a.u.)')
    plt.xlabel('Temperature (K)')
    if file_read.columns.__len__() is not 1:
        plt.legend(bbox_to_anchor=(1, 0.5), loc='center', ncol=1)
    else:
        plt.title(single_molecule_name + '/Ni(110) TPD')
    # plt.legend(bbox_to_anchor=(1, 0.5), loc='center', ncol=1)

    # labels = file_read.keys()
    # plt.get_legend_handles_labels()

    # any vertical dotted line values go here
    for x_val in dotted_lines:
        plt.axvline(x=x_val, ymin=0, ymax=1, color='k',  linestyle='--')

plt.show()
print('hi')
print('hi')
