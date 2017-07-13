
langmuir = 1e-6 # torr

dose = float(input('what dose (L)? '))

base_pressure = float(input('what is BP (torr)? '))

time_dosed = 30 #seconds

DP = base_pressure + dose*langmuir/time_dosed

print('Your dosing pressure is: ' + str(DP))