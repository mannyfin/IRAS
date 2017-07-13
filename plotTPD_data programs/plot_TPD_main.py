import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

#TODO zero out graphs better
#TODO plot 0.1 and 0.2L for big multilayer curve


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
    # caveat...only works with monitoring a single mass
    y_prime = pd.DataFrame(slope.values * file_read.index.values, columns=file_read.columns)
    y_prime.index = file_read.index
    difference = file_read - y_prime

    new_file_read = difference

    return new_file_read

# Main
root = tk.Tk()
root.withdraw()
file_path1 = filedialog.askopenfilenames(filetypes=(('Text files', '*.txt'),
                                   ('All files', '*.*')),
                                   title='Select Input File'
                                   )
for file in file_path1:
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

    # only do below if there is only one column
    if file_read.columns.nunique() is 1:
        new_file_read = single_slope_subtract(file_read)
    else:
        # this case is invoked if there are more than one column
        new_file_read = file_read

    # baseline subtraction
    new_file_read = new_file_read - new_file_read.min()
    if file_read.columns.nunique() is 1:
    # plot the data
    # file_read.plot(x=file_read.index, figsize=(15,7))  # ylabel='QMS signal (a.u.)'
        ax = plt.figure(123, figsize=(15,7))
        plt.plot(new_file_read, label=filename)
    else:
        # ax = plt.figure(123, figsize=(15, 7))
        new_file_read.plot(figsize=(15, 7))
        # plt.plot(new_file_read)
        # plt.legend()



    # file_read.plot()

    plt.ylabel('QMS signal (a.u.)')
    plt.xlabel('Temperature (K)')
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center', ncol=1)
    # plt.legend(bbox_to_anchor=(1, 0.5), loc='center', ncol=1)


    # labels = file_read.keys()
    # plt.get_legend_handles_labels()
    #
    # plt.legend()

    # plt.show()
    # ax.legend()
    #
    # ax.hold()

    # any vertical dotted line values go here
    dotted_lines = [204.7, 161, 260, 395, 428]
    for x_val in dotted_lines:
        plt.axvline(x=x_val, ymin=0, ymax=1, color='k',  linestyle='--')

plt.show()
print('hi')
print('hi')
