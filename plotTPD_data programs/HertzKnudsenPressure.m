clear;clc
%Feel free to change T
T = 707.1;%Assume desorption at 707.1 K

dmm = 8;% 8 mm diameter of crystal
d = dmm/1000; %convert mm to m
Area = pi*((d/10)^2)./4; % Area of crystal in m^2
Na = 6.022*10^23; %molecules/mole
M = 7/1000; %mass of Li in kg/mol 
R = 8.314; %gas const J/(mol*K)
dNdtfigure4 = 8e12; %Li Desorption rate at Tp  (atoms/(cm^2*sec) from Figure 4 Top panel
dNdt = (dNdtfigure4)./(100*100); %convert Li desorption rate to (atoms/(m^2*sec)
P = ((1/Area).*(dNdt).*(sqrt(2*pi*M*R*T)))./(Na);% Pressure in Pa
Pa_to_torr = 0.00750062; % 1 Pa = 0.00750062 torr
Ptorr = P*Pa_to_torr
