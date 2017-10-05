import numpy as np
import matplotlib.pyplot as plt
A = 5.5607
B = 2484.596
C = -31.035
# T = 300  # K
T = np.arange(290, 478, 0.1)
P = 10**( A - (B/(T+C)))  # bar
bar_to_torr = 1/750.062  # bar/torr
P = P/bar_to_torr
print(P)

plt.plot(T,P)
plt.xlabel('T (K)')
plt.ylabel('P (torr)')
plt.title('Vapor Pressure of Guaiacol')
plt.show()