import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.axes as axes
import numpy as np
# import scipy.integrate
from scipy import integrate
import re
from init_info import *
from collections import defaultdict
# import seaborn as sns

# TODO see below
"""
1. Handle hiden TPD files by using corresponding mass instead of name in finding in the dict
"""



# sns.set_style("dark")
# sns.set_style("ticks", {"xtick.minor.size": 8, "ytick.minor.size": 8})
mpl.rcParams.update({'font.size': 20})
# current_palette = sns.color_palette("hls", 10)
# sns.set_palette(current_palette, n_colors=10)
# sns.palplot(sns.color_palette("hls", 8))

# TODO will append the langmuirs to this list
langmuir = []
# keep area dict empty
area_dict = defaultdict(list)
filename_list = []

def rename_to_text(file_path):
    """
    Appends a .txt to all files run since some output files do not have an extension

    :param file_path: input file path
    :return: .txt appended to end of file name
    """
    import os
    file = file_path.split('/')[-1]
    if file.endswith('.txt') is False:
        new_file_name = file_path+'.txt'
        os.rename(file_path, new_file_name)
        file_path = new_file_name
    filename = file
    return file_path, filename


def single_slope_subtract(file__read, num_points_to_average_beg=50, num_points_to_average_end=50):
    """
    Averages points at the beginning and end of a file and subtracts the line between the two points from the data to
    subtract a background.
    :param file__read: df of file
    :param num_points_to_average_beg: number of points to average from the beginning of the dataset
    :param num_points_to_average_end: number of points to average from the end of the dataset
    :return: new_file_read, which is the background subtracted data
    """

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
    # ynew = y - m_hat*x
    difference = file__read - y_prime
    difference = difference - difference.iloc[:(num_points_to_average_beg)].mean()

    new_file_read = difference

    return new_file_read

def plot_same_masses(dict__values, file_name, new__file__read, area_dict):
    """
    Plots the same masses together in a matploblib figure. It also feeds into uptake area to calculate the area
    under the curve for a particular mass
    :param dict__values: dictionary of masses
    :param file_name: name of the file
    :param new__file__read: dataframe of the data in the file
    :return: outputs a plot
    """
    i = 0
    # for key, value in dict__values.items():
    for colname in new__file__read.columns:
        try:
            i += 1
            # mass_data = new__file__read.filter(regex=str(value))


            # key = dict__values[new__file__read.columns[0].split('=')[1]]
            try:
                key = dict__values[new__file__read[colname].name.split('=')[1]]
            except IndexError:
                # if the file is a hiden file do the following below...
                key = dict__values[new__file__read[colname].name]
            mass_data = new__file__read[colname]
            # mass_data = new__file__read.columns[colname].split('=')[1]
            fig = plt.figure(figsize=(15, 7), num=key)
            ax = fig.add_subplot(111)
            ax.tick_params(direction='out', length=6, width=2, colors='k')

            if monochrome:
                ax.plot(mass_data, label=file_name, linewidth=2, color='k')
                if file_name == monolayer:
                    ax.plot(mass_data, label=file_name, linewidth=2, color='r')
            else:
                ax.plot(mass_data, label=file_name, linewidth=2)
            plt.ylabel('QMS signal (a.u.)')
            plt.xlabel('Temperature (K)')
            plt.title(key + '/' + surface + ' TPD')

            plt.minorticks_on()
            plt.tick_params(which='minor', length=4, width=1.5)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            # iterate i to change the figure number for the different mass
            # ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
            # ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
            # ax.grid(b=True, which='major', color='w', linewidth=1.0)
            # ax.grid(b=True, which='minor', color='w', linewidth=0.5)

            # new__file__read.rename(columns={new__file__read.filter(regex=str(value)).columns[0]: key}, inplace=True)
            new__file__read.rename(columns={new__file__read[colname].name: key}, inplace=True)
            mass_data.columns = [key]
            if legend_disp =='on':
                plt.legend()
            if use_temp_limits is True:
                axes.Axes.set_xlim(plt.gca(), left=low_temp, right=high_temp)
            integrate_area = uptake_area(mass_data, key, temp_ranges=temp_values, slope_subtract=slope_subtract)
            # print(str(int(integrate_area))+' area for ' + key)
            print(str((integrate_area))+' area for ' + key)

            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        # TODO add these areas to a list or ordered dictionary
        #     add these areas to a list or ordered dictionary

        except ZeroDivisionError or KeyError:
            if ax.has_data() is False:
                plt.close(fig)
            # print('ZeroDivisionError: integer division or modulo by zero')
            print('Mass: ' + key + ' not found in ' + file_name)
            integrate_area = -1
    #         TODO
    #         if the mass is not in the file, we still need to add an empty element to the area for that particular mass
    #         this way when another file is read that contains the mass, the order is not lost
    #         add these areas to a list or ordered dictionary

    #     now add this area to the dictionary
        area_dict[key].append(integrate_area)
        # area_dict[key].append(int(integrate_area))


    # return new__file__read, area_dict
    return area_dict


def uptake_area(mass_data, key, temp_ranges, slope_subtract = True):
    """

    :param mass_data: Data from the particular mass
    :param key: The name of the mass, ex. HOAc
    :param temp_ranges: The temperature range you want to take the area under the curve. This area is slope subtracted.
    :return: Area under the curve
    """
    # slope_subtract = True

    try:
        lower_index1 = str(temp_ranges[key][0])
        upper_index1 = str(temp_ranges[key][1])
        if type(mass_data) == pd.core.frame.DataFrame:
            mass_data = mass_data.query('index >' + lower_index1 + ' & index < ' + upper_index1)
            if slope_subtract is True:
                # slope subtraction?
                mass_data = single_slope_subtract(mass_data, num_points_to_average_beg=2,num_points_to_average_end=2 )

            area_under_curve = integrate.trapz(mass_data, x=mass_data.index, axis=0)[0]
        elif type(mass_data) == pd.core.series.Series:
            # mass_data = mass_data[float(lower_index1): float(upper_index1)]

            mass_data = mass_data.to_frame().query('index >' + lower_index1 + ' & index < ' + upper_index1)[
                mass_data.name]
            if slope_subtract is True:
            # slope subtraction?
                mass_data = single_slope_subtract(mass_data.to_frame(), num_points_to_average_beg=2, num_points_to_average_end=2)
                mass_data = mass_data - mass_data.min()
                area_under_curve = integrate.trapz(mass_data, x=mass_data.index, axis=0)[0]
            else:
                area_under_curve = integrate.trapz(mass_data)

        # The area below was calculated from a saturation dose of CO adsorbed on Pt(100)-hex
        # area_under_curve/=sat_CO_area_Pt
        # area_under_curve/=2253432

        # mass_data.plot()
    except KeyError:
        area_under_curve = -1

    return area_under_curve


def langmuir_determination(filename):
    """
    lets look at the naming conventions for the files
    example: '6_6_2017_AA_0.015 L.txt'
    or 'HOAc_6E-09_150 s _718_high_point_density.txt'
    In the first case, the dose is in the name, in the second case, we have to calculate the dose
    assuming background is zero torr...so this is the dosing pressure...

    For reference: 1 Langmuir(L) = 1e-6 torr * seconds and is a unit of exposure
    :param filename: Name of the experiment file. We assume the name of the file has the info to calculate the exposure
    :return: langmuir: the exposure for the experiment
    """
    try:
        if 'L' in filename:
            idx1 = filename[::-1].find('_')
            idx2 = filename[::-1].find('L')

            # files =filename[-idx1:-idx2]
            langmuir = float(''.join(i for i in filename[-idx1:-idx2] if i.isdigit() or i == '.'))
            print(str(langmuir))

        else:
            # please make sure your file has the name written right...
            underscore = [m.start() for m in re.finditer('_', filename)]
            dose = float(filename[underscore[0] + 1: underscore[1]])
            time_s = float(re.sub('\D', '', filename[underscore[1] + 1: underscore[2]]))
            langmuir = dose*time_s/(1e-6)
            print(str(langmuir))
    except ValueError:
        langmuir = 0
        print("uh oh, I can't figure out how many langmuir this file is.")
        print("Setting langmuir to zero")

    return langmuir


def area_table_fig(area_dictionary=area_dict):
    """
    Makes a nice looking figure of the areas
    :param area_dictionary: area dictionary calculated by integrating the areas under the curve
    :return:
    """
    # fig, ax = plt.subplots(num='Area Table', figsize=(20, 7))
    fig, ax = plt.subplots(num='Area Table')

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    # df_areadata = pd.DataFrame.from_dict(area_dictionary)
    df = pd.DataFrame.from_dict(area_dictionary)

    # df_filelist = pd.DataFrame(file_list, columns=['File'])

    # df = df_filelist.join(df_areadata)

    ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # tabla = plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', bbox=[0, 0, 1,1])
    # tabla.auto_set_font_size(False)
    # tabla.set_fontsize(14)

    # fig.tight_layout()
    # we dont want to show the plots till the end
    # plt.show()


def read_files(file):
    # TODO Fix search into the dictionary for increased speed
    """
    1. Reads in the files and does quick cleaning
    2. sets the temperature as the index
    :param file: .txt file of the data
    :return:
    """
    file_path, filename = rename_to_text(file)
    print('\n\n')
    print(file_path)
    print('\n\n')
    # find the exposure (L)
    # langmuir.append(langmuir_determination(filename=filename))
    try:
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
    except IndexError:
        "except it is a hiden mass spec file!"
        file_read = pd.read_csv(file_path, header=29)
        file_read = file_read.dropna(axis=1)
        file_read.drop(['Time', 'ms'],axis=1, inplace=True)
        file_read.set_index('Temperature', inplace=True)
    # pseudo code...
    # pd.DataFrame(molecule_area[i], index=langmuir) and append all of them

    return file_read, filename

def export_data(corrected_data_file, filename):
    writer = pd.ExcelWriter(filename + ' TPD_output ' + single_molecule_name+'.xlsx')
    corrected_data_file.to_excel(writer, 'Sheet1')
    writer.save()

# Main begins
root = tk.Tk()
root.withdraw()
file_path1 = filedialog.askopenfilenames(filetypes=(('All files', '*.*'), ('Text files', '*.txt')),
                                         title='Select Input File(s)')
# fignum = 1+len(dict_values.keys())
# attempt to order the files
file_path1 = sorted(file_path1, reverse=True)
# set color palette to be len(num_files). 8 refers to the typical number of masses represented on a TPD plot
try:
    sns.set()
    sns.set_context("poster")
    current_palette = sns.color_palette("Paired", max(len(file_path1), 8))
    sns.set_palette(current_palette, n_colors= max(len(file_path1), 8))
except NameError:
    "seaborn not imported and is likely commented out"
# sns.palplot(sns.color_palette())
temp_df = []
fname_lst = []
for file in file_path1:

    file_read, filename = read_files(file=file)

    if use_temp_limits is True:
        # selects only appropriate temperature range
        file_read = file_read.loc[(file_read.index <= high_temp) & (file_read.index >= low_temp)]
    # the line below is for the case where the temp falls before you stop the program, and so you only go from low to
    # high temp and not low-high-low on your temperature index
    file_read = file_read.iloc[0:file_read.index.argmax()+1]

    # first slope subtraction
    new_file_read = single_slope_subtract(file_read)
    # baseline subtraction
    new_file_read = new_file_read - new_file_read.min()
    # # a second slope subtraction -- TODO fix algo here because it can lead to curves < 0
    new_file_read = single_slope_subtract(new_file_read,num_points_to_average_beg=3,num_points_to_average_end=3)
    new_file_read = new_file_read - new_file_read.min()

    # PLOTTING
    # remove .txt from filename
    filename = re.sub('.txt', '', filename)
    # For Hiden data
    filename = re.sub('.csv', '', filename)
    filename_list.append(filename)
    areas = plot_same_masses(dict__values=dict_values, file_name=filename, new__file__read=new_file_read, area_dict=area_dict)
    temp_df.append(new_file_read)
    fname_lst.append(filename)
    """
    **************************************************************************************************
    Try to get the Langmuir from the filename and append to area dictionary for making the uptake plot
    **************************************************************************************************
    """
    try:
        file_added = re.search('.*([0-9]\.[0-9]+)', filename).group(1)
        try:
            file_added = float(file_added)
        except AttributeError:
            file_added = 0

    except AttributeError:
        file_added = float(0)
        # file_added = filename

    areas['L'].append(file_added)

    if use_temp_limits is True:
        axes.Axes.set_xlim(plt.gca(), left=low_temp, right=high_temp)

    fig = plt.figure(filename, figsize=(15, 7))
    all_axes = fig.add_subplot(111)
    new_file_read.plot(ax=all_axes, figsize=(15, 7), title=filename, linewidth=2.5)
    plt.ylabel('QMS signal (a.u.)')
    plt.xlabel('Temperature (K)')
    plt.title(filename)
    all_axes.tick_params(direction='out', length=6, width=2, colors='k')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    all_axes.spines['top'].set_visible(False)
    all_axes.spines['right'].set_visible(False)
    plt.minorticks_on()
    plt.tick_params(which='minor', length=4, width=1)

    # export the subtracted data?
    if export is True:
        export_data(new_file_read, filename)


    # plt.savefig(filename+'.png')
    # plt.close(fig)

    # any vertical dotted line values go here
    # for x_val in dotted_lines:
    #     plt.axvline(x=x_val, ymin=0, ymax=1, color='k',  linestyle='--')

# area_table_fig(areas, filename_list)
try:
    # areas = pd.DataFrame(areas)
    areas = pd.DataFrame.from_dict(areas, orient='index').T
    areas = areas.fillna(method='ffill')
    areas.sort_values(by='L',inplace=True)
    areas.reset_index(inplace=True, drop=True)

    area_table_fig(areas)

    if len(areas.index) > 1:
        areas.set_index('L', inplace=True)
        area_axes = areas.plot( title='Uptake')
        area_axes.set_ylabel('Area')
        fig = plt.gcf()
        fig.canvas.set_window_title('Uptake')

    writer = pd.ExcelWriter(single_molecule_name + ' Area_output.xlsx')
    areas.to_excel(writer, 'Sheet1')
    writer.save()

    # save plots
    if suppress_plots is False:
        plt.show()
    print('hi')

    """
    Use the following commented lines out below if you want to save the slope subtracted data
    """
    # tpd_writer = pd.ExcelWriter(single_molecule_name + fname_lst[0] +'TPD.xlsx')
    # for idx, val in enumerate(fname_lst):
    #     you need the line below because each sheet name has to have <= 31 chars
    #     if len(val) >= 31:
    #         val = val[:30]
    #     temp_df[idx].to_excel(tpd_writer, val)
    # tpd_writer.save()
except:
    print('')
    if suppress_plots is False:
        plt.show()