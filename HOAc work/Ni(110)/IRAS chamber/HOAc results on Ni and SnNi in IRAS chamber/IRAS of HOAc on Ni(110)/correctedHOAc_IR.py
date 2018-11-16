import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes as ax
# creates the data for the HOAc/Ni(110) IR
colnames = ['Wavenumber', 'Intensity']

# 15 s

f1 = pd.read_csv("Ni(110) 1e-9Torr15s 210K.0.dpt", '\t', header=None, names=colnames)
f1.set_index(colnames[0], inplace=True)

f2 = pd.read_csv("Ni(110) 1e-9Torr15s 352K.0.dpt", '\t', header=None, names=colnames)
f2.set_index(colnames[0], inplace=True)

f3 = pd.read_csv("Ni(110) 1e-9Torr15s 452K.0.dpt", '\t', header=None, names=colnames)
f3.set_index(colnames[0], inplace=True)

k90_15s = -1*f3 # background was taken at 90 K
k210_15s = -1*(f3-f1)
k352_15s = -1*(f3-f2)

cat_15s = pd.concat([k90_15s, k210_15s, k352_15s], axis=1, keys=['90K', '210K', '352K'])

# 60 s

f4 = pd.read_csv("Ni(110) 1e-9Torr60s -200K.0.dpt", '\t', header=None, names=colnames)
f4.set_index(colnames[0], inplace=True)

f5 = pd.read_csv("Ni(110) 1e-9Torr60s -350K.0.dpt", '\t', header=None, names=colnames)
f5.set_index(colnames[0], inplace=True)

f6 = pd.read_csv("Ni(110) 1e-9Torr60s -450K.1.dpt", '\t', header=None, names=colnames)
f6.set_index(colnames[0], inplace=True)

f7 = pd.read_csv("Ni(110) 1e-9Torr60s -550K.1.dpt", '\t', header=None, names=colnames)
f7.set_index(colnames[0], inplace=True)

k90_60s = -1*f7
k200_60s = -1*(f7-f4)
k350_60s = -1*(f7-f5)
k450_60s = -1*(f7-f6)

# colors added to more closely match excel
cat_60s = pd.concat([k90_60s, k200_60s, k350_60s, k450_60s], axis=1, keys=['90K', '200K', '350K', '450K'])
#
# fig1, ax1 = plt.subplots()
# ax1.plot(cat_15s)
cat_15s.plot(title='HOAc/Ni(110) IRAS, 15s', color=['mediumblue', 'firebrick', 'lime'], linewidth=2.5)
plt.minorticks_on()
# ax.Axes.invert_xaxis(plt.gca())
# fig2, ax2 = plt.subplots()
# ax2.plot(cat_60s)
cat_60s.plot(title='HOAc/Ni(110) IRAS, 60s', color=['rebeccapurple', 'steelblue', 'darkorange', 'navy'], linewidth=2.5)
plt.minorticks_on()

plt.show()

# uncomment if needed

writer = pd.ExcelWriter('HOAc_Ni(110) IR plot2.xlsx')
cat_15s.to_excel(writer, sheet_name='Sheet1')
cat_60s.to_excel(writer, sheet_name='Sheet1', startcol=5)
writer.save()
