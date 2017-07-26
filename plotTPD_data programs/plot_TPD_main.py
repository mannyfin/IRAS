import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import numpy as np

# TODO see below
"""
1. areas don't get bigger than monolayer for the cracks
2. plot uptake of HOAC 
3. plot uptake of H2 and CO vs uptake of HOAC (combine 1 and 2)

label each curve
Integrate each curve with separate
scipy.integrate.trapz(new_file_read,x=new_file_read.index, axis=0)

"""


# Preliminary stuff
# Display of temp range on plots. These limits are null if there is more than one column unless otherwise specified
use_temp_limits = True
low_temp = 100
high_temp = 600
single_molecule_name = 'HOAC'
# any vertical dotted lines go here
# dotted_lines = [204.7, 161, 395, 428]
dotted_lines = [204.7, 161, 260, 395, 428]


dict_values = dict({'HOAC': 61.297,
                    'CO': 28.1,
                    'H2':1.5,
                    'H2O':17.9,
                    'CO2': 44.7})
# dict_values = dict({'HOAC': 60.,
#                     'CO': 27.7,
#                     'H2':1.942,
#                     'H2O':17.57,
#                     'CO2': 43.7,
#                     'CH2': 13.6,
#                     '29': 28.8,
#                     'EtOH': 30.7,
#                     'CH4': 14.6})


def rename_to_text(file_path):
    import os
    file = file_path.split('/')[-1]
    if file.endswith('.txt') is False:
        new_file_name = file_path+'.txt'
        os.rename(file_path, new_file_name)
        file_path = new_file_name
    filename = file
    return file_path, filename


def single_slope_subtract(file__read, num_points_to_average_beg=50,num_points_to_average_end=50 ):
    """
    
    :param file__read: df of file
    :param num_points_to_average_beg: 
    :param num_points_to_average_end: 
    :return: 
    """
    # single slope subtraction
    # num_points_to_average_beg = 50
    # num_points_to_average_end = 50

    # mean of first N points
    avg_y_beg = file__read.iloc[:num_points_to_average_beg].mean()

    # mean of last N points
    avg_y_end = file__read.iloc[-num_points_to_average_end:].mean()

    # x value for beginning (assume first xval)
    first_xval = file__read.first_valid_index()

    # x value for ending (assume last xval)
    last_xval = file__read.last_valid_index()

    slope = (avg_y_end - avg_y_beg) / (last_xval - first_xval)
    # y' = mx
    # caveat...only works with monitoring a single mass-- update 7/13/17 appears to have fixed this...
    # y_prime = pd.DataFrame(slope.values * file_read.index.values, columns=file_read.columns)

    y_prime = pd.DataFrame(np.matmul(file__read.index.values[:, np.newaxis], np.transpose(slope.values[:, np.newaxis])),
                           columns=file__read.columns)

    y_prime.index = file__read.index

    # first attempt at fix
    # y_prime = slope.values[0]*file_read.index+avg_y_beg

    difference = file__read - y_prime
    difference = difference - difference.iloc[:(num_points_to_average_beg)].mean()

    new_file_read = difference

    return new_file_read


def plot_same_masses(dict__values, file_name, new__file__read):
    """
    Plots the same masses together
    :param dict__values: dictionary of masses
    :param file_name: name of the file
    :param new__file__read: dataframe of the data in the file
    :return: outputs a plot
    """
    i = 0
    for key, value in dict__values.items():

        try:
            i += 1
            mass_data = new__file__read.filter(regex=str(value))
            fig = plt.figure(i, figsize=(15, 7))
            ax = fig.add_subplot(111)
            ax.plot(mass_data, label=file_name)
            plt.ylabel('QMS signal (a.u.)')
            plt.xlabel('Temperature (K)')
            plt.title(key + '/Ni(110) TPD')
            # iterate i to change the figure number for the different mass


        except ZeroDivisionError:
            if ax.has_data() is False:
                plt.close(fig)
            # print('ZeroDivisionError: integer division or modulo by zero')
            print('Mass: ' + key + ' not found in ' + file_name)

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
    # file_read = file_read.drop([column_names[0], column_names[-1]], axis=1)
    file_read = file_read.drop([column_names[0]], axis=1)
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
fignum = 1+len(dict_values.keys())
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
    # # a second slope subtraction -- TODO fix algo here because it can lead to curves < 0
    # new_file_read = single_slope_subtract(new_file_read,num_points_to_average_beg=20,num_points_to_average_end=20)

    # PLOTTING

    plot_same_masses(dict__values=dict_values, file_name=filename, new__file__read=new_file_read)

    # # plot whole file
    # new_file_read.plot(figsize=(15, 7))
    # plt.plot(new_file_read)
    # plt.legend()
    # # set y lower limit = 0
    # axes.Axes.set_ylim(plt.gca(), bottom=0, auto=True)

    if use_temp_limits is True:
        axes.Axes.set_xlim(plt.gca(), left=low_temp, right=high_temp)

    # file_read.plot()
    # all_axes = plt.figure(fignum)
    fig = plt.figure(fignum, figsize=(15, 7))
    all_axes = fig.add_subplot(111)
    new_file_read.plot(ax=all_axes,figsize=(15, 7), title=filename)
    plt.ylabel('QMS signal (a.u.)')
    plt.xlabel('Temperature (K)')
    plt.title(filename)
    # if file_read.columns.__len__() is not 1:
    #     plt.title(filename)
    #     plt.legend(bbox_to_anchor=(1, 0.5), loc='center', ncol=1)
    # else:
    #     plt.title(single_molecule_name + '/Ni(110) TPD')
    # plt.legend(bbox_to_anchor=(1, 0.5), loc='center', ncol=1)

    # any vertical dotted line values go here
    for x_val in dotted_lines:
        plt.axvline(x=x_val, ymin=0, ymax=1, color='k',  linestyle='--')

    fignum += 1
plt.show()
print('hi')
print('hi')
