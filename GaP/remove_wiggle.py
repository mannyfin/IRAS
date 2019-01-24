"""
For figures 2 and 3, which look at first like delta functions, make sure you zoom into the origin...
All you need to do is adjust the bounds variable...
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


data = pd.read_excel('IR.xlsx',sheet_name='150 K')
selected = data.loc[ (data.Wavenumber>1500) & (data.Wavenumber <2000)]
# def model(x, A, omega, phi, c):
#     return A*np.sin(omega*x + phi) + c
#
#
# popt, pcov = curve_fit(model, selected.Wavenumber.values, selected.Intensity.values)
#
# print(popt)
#
# selected.plot(x='Wavenumber', y='Intensity')
# data.plot(x='Wavenumber', y='Intensity')
#
# fig, ax = plt.subplots()
# ax.plot(selected.Wavenumber, selected.Intensity,'b', selected.Wavenumber, model(selected.Wavenumber.values, *popt), 'r-')
#
# fig1,ax1 = plt.subplots()
# ax1.plot(selected.Wavenumber, selected.Intensity,'b', selected.Wavenumber, model(selected.Wavenumber.values, 0.00003, (2*np.pi)/50, 0.03, 2.23e-3), 'r-')
#
# plt.show()

fft = np.fft.fft(selected.Intensity.values)
freq = np.fft.fftfreq(selected.Wavenumber.values.shape[-1])
fig3,ax3 = plt.subplots()
ax3.plot(freq, 2.0/len(fft) * np.abs(fft))

# remove a freq by setting those values to zero

# asdf = np.fft.fft(selected.Intensity)
# asdfx = np.fft.fftfreq(selected.Wavenumber.shape[-1])
# fig99, ax99 = plt.subplots()
# ax99.plot(asdfx, np.abs(asdf))
# np.put(asdf,np.where((asdfx>0.01) & (asdfx<0.05)), v=0)
# np.put(asdf,np.where((asdfx<-0.01) & (asdfx>-0.05)), v=0)
# fig100, ax100 = plt.subplots()
# ax100.plot(asdfx, np.abs(asdf))
# goback = np.fft.ifft(asdf)
# fig101, ax101 = plt.subplots()
# ax101.plot(selected.Wavenumber, selected.Intensity,'b', selected.Wavenumber,goback.real, 'r', )
# plt.legend(['original', 'single frequency subtracted'])
# plt.show()

fftdata = np.fft.fft(data.Intensity)
freqdata = np.fft.fftfreq(data.Wavenumber.shape[-1])
# plot results
fig4, ax4 = plt.subplots()
ax4.plot(freqdata, fftdata)
bounds = [0.02, 0.035]
np.put(fftdata,np.where((freqdata>bounds[0]) & (freqdata<bounds[1])), v=0)
np.put(fftdata,np.where((freqdata<-bounds[0]) & (freqdata>-bounds[1])), v=0)
# plot removed freq
fig5, ax5 = plt.subplots()
ax5.plot(freqdata, np.abs(fftdata))
# inverse transform
goback = np.fft.ifft(fftdata)
# plot results
fig101, ax101 = plt.subplots()
ax101.plot(data.Wavenumber, data.Intensity,'b', data.Wavenumber,goback.real, 'r', )
plt.legend(['original', 'single frequency subtracted'])
plt.show()