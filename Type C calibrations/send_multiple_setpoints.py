import pandas as pd
import os
from scipy import interpolate
import numpy as np
import sys
from thermocouples_reference import thermocouples
import minimalmodbus as mm
import time
"""
1. Define input temperature and heating rate
2. Define how frequently to send new setpoint in seconds.

3a. Make array of setpoints (mV) based on frequency all the way to the highest T, say 2000 K
3b. Or make array of setpoints(mV) up to some pre-defined stop temperature
-Interpolate points in 3a/b as necessary.

4. Send these setpoints at the desired frequency

5. Read output
"""


class Eurotherm(mm.Instrument):
    def __init__(self, port, baudrate=9600, num_dec=3):
        self.num_dec = num_dec
        mm.Instrument.__init__(self, port=port, slaveaddress=1)
        self.serial.baudrate = baudrate
        self.serial.close()
        self.serial.open()
        print(str(port) + ' is open?' + str(self.serial.isOpen()))

    def close_me(self):
        # close serial port
        self.serial.close()
        return print(self.serial.isOpen())

    def open_me(self):
        # open serial port
        self.serial.open()
        return print(self.serial.isOpen())

    def read_val(self, num_dec=3):
        # read current value
        return self.read_register(1, num_dec, signed=True)

    def read_sp(self, num_dec=3):
        # read setpoint val
        return self.read_register(2, num_dec, signed=True)

    def write_sp(self,sp, num_dec=3):
        # write setpoint val
        return self.write_register(2, sp, num_dec, signed=True)

    def read_rt(self,num_dec=2):
        # read CJC temp in C to two decimals
        # if Eurotherm is not in a thermocouple mode it may read 0.0
        return self.read_register(215, 2)


def interp_setpoints(low_T, high_T,df, heatingRate=7., sendFreq=0.5,log_style=False,scalar=1 ):
    """
    Make sure the column names are 'Temp' and 'mV'
    :param low_T: input low T, should be within range on the df Table
    :param high_T: input high T, should be within range on the df Table
    :param df: Table of values for the Type C thermocouple, but could be any table in principle
    :param scalar: scalar to multiply by the number of calculated setpoints, will raise an error if num_setpoints >
    number of datapoints.
    :return: interpolated mV values for the LabView program
    """

    assert low_T < high_T, 'low T is not lower than high T!'
    assert low_T >= df['Temp'].min(), 'low T is lower than on the calibration table'
    assert high_T <= df['Temp'].max(), 'high T is higher than on the calibration table'

    # calculate the length of the data between lowT and highT
    num_data = len(df[df['Temp'].between(low_T, high_T)])

    if log_style is False:

        """
        this is the "new" way based on the heating rate
        """
        # x_new is a linspace from low_T to high_T and the number of setpoints
        interp_T = np.arange(low_T, high_T, heatingRate*sendFreq)

        print('From {0} data points, you selected {1} setpoints!'.format(num_data, len(interp_T)))

    elif log_style is True:
        # num_setpoints = scalar *(highT-lowT)/ log10(number of datapoints between highT and lowT)
        num_setpoints = scalar*int(np.round((high_T-low_T)/np.log10(num_data),))
        """
        this is the "old" way based on the number of setpoints
        """
        # x_new is a linspace from low_T to high_T and the number of setpoints
        interp_T = np.linspace(low_T, high_T, num=num_setpoints)

        print('From {0} data points, you selected {1} setpoints!'.format(num_data, num_setpoints))

        # just in case the scalar is set too high
        if num_setpoints > len(df[df['Temp'].between(low_T, high_T)]):
            raise ValueError('Too many setpoints expected. Adjust scalar or increase temperature range')

    # I create a function f, that I will interpolate values from
    interp_fcn = interpolate.interp1d(x=df['Temp'].values, y=df['mV'].values)



    # y_new contains the mV of the interpolated T's
    interp_mV = interp_fcn(interp_T)

    # all you need to do is return y_new back into LabView
    return interp_mV


def read_table(pathname, name):
    os.chdir(pathname)
    # df_ = pd.read_excel(name, names=['Temp','mV'])
    df_ = pd.read_csv(name, names=['Temp','mV'])
    return df_

"Read in calibration Table"
file_path = 'C:\\Users\\Administrator\\Desktop\\PythonProjects\\LabViewtest\\'
# fname = 'Type C calibration_corrected.xlsx'
fname = 'Type C calibration_corrected.csv'
# df = pd.read_csv('Type C calibration_corrected.csv', names=['Temp', 'mV'])
df = read_table(file_path, fname)

"Create obj for reading and writing temperature to Eurotherm"
port1 = 'COM4'
controlObj = Eurotherm(port1)
"Create obj for reading Room temperature from Eurotherm"
port2 = 'COM5'
# controlObj2 = Eurotherm(port2)


"For reading in Room Temp to correct Temp reading"
typeC = thermocouples['C']
# TODO add room temp compensation



"1."
start_T = 100 # will vary based on input temperature from eurotherm
end_T = 150
heatingRate = 5 # heating rate in Kelvin per second
"2."
# tested down to 0.01 seconds, but it increases the amount of errors. Also total time increases as sendFreq decreases
sendFreq = 0.5
"3b."
mVsetpoints = interp_setpoints(start_T, end_T, df, heatingRate=heatingRate, sendFreq=sendFreq)

"4. Send setpoints"
j=0


alpha=.95
while j <4:
    print('iteration ' + str(j))
    start = time.time()
    for i in mVsetpoints:
        # We might briefly lose contact with the instrument, so we try sending the setpoint. if it fails, try it again

        try:
            controlObj.write_sp(i)
            # this alpha will try to snap the total time down to the proper rate
            time.sleep(alpha*sendFreq)
            # print(controlObj.read_sp())
            # print(controlObj.read_val())
        except (ValueError, OSError) as e:
            print(e)
            # still try to send it again
            try:
                time.sleep(0.02)
                controlObj.close_me()
                controlObj.open_me()
                controlObj.write_sp(i)
            except (ValueError, OSError) as e:
                print(e)
                time.sleep(0.1)
                controlObj.close_me()
                controlObj.open_me()
                # still try to send it again for another time
                controlObj.write_sp(i)
      # TODO: Handle ValueError from sending setpoints too rapidly or OSError
    end_time = (time.time()-start)
    print(end_time)
    alpha = alpha*(end_T - start_T)/(end_time*heatingRate)
    # TODO adjust alpha inside the loop instead of after every iteration
    print(alpha)
    j+=1

# for safety, set final setpoint back to beginning
controlObj.write_sp(mVsetpoints[0])

print('hi')


