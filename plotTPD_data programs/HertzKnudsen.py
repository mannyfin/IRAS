from math import pi, sqrt


# flux in 1/(m^2*s)
# 1e15 is the surface atom density in atoms/cm^2. I convert to m^2 by a factor of 100^2
Na = 6.02214e23
Z = 1e15*(100**2)
# mass in kg
m = 28/(Na*1000)
#  boltzmann constant J/K, kb = R/Na
kb = 1.38066e-23
# Temperature, Kelvin
T = 300
# sticking coefficient
sticking = 1
#  Hertz knudsen equation. The pressure is in Pascal
P = Z*sqrt(2*pi*m*kb*T)/sticking

P_torr = P*760/101325
print(P_torr)


















# T = 707.1  # Assume desorption at 707.1 K
#
# dmm = 10  # 8 mm diameter of crystal
# d = dmm/1000  # convert mm to m
# # Area = pi*((d/10)**2)/4  # Area of crystal in m^2
# Area = pi*(d**2)/4  # Area of crystal in m^2
# # print(Area)
# # Area = d**2
# # print(Area)
# Na = 6.022*10**23  # molecules/mole
# M = 28/1000  # mass of Li in kg/mol
# R = 8.314  # gas const J/(mol*K)
# dNdtfigure4 = 1e15  # Li Desorption rate at Tp  (atoms/(cm^2*sec) from Figure 4 Top panel
# dNdt = dNdtfigure4/(100*100)  # convert Li desorption rate to (atoms/(m^2*sec)
# P = ((1/Area)*dNdt*(sqrt(2*pi*M*R*T)))/Na  # Pressure in Pa
# Pa_to_torr = 0.00750062  # 1 Pa = 0.00750062 torr
# Ptorr = P*Pa_to_torr
# print(Ptorr)