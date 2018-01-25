import pandas as pd
import numpy as np
import holoviews as hv
# hv.extension('bokeh')


def read_files(file):
    # TODO Fix search into the dictionary for increased speed
    """
    1. Reads in the files and does quick cleaning
    2. sets the temperature as the index
    :param file: .txt file of the data
    :return:
    """

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

    return file_read


file_path = 'C:\\Users\\manolis\\Desktop\\PycharmProjects\\IRAS\\IRAS\\HOAc work\\Ni(110)\\all\\HOAc_3.5E-09_15 s_724.txt'

file = read_files(file_path)
# file = pd.read_csv(file_path, sep='\t', header=3)
file.head(n=3)

curve = hv.Curve(file, ' temp (K)', ' MS5=61.297', group='title')

hv.extension('bokeh', 'matplotlib')