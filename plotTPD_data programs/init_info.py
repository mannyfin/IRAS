

# Preliminary stuff
# Display of temp range on plots. These limits are null if there is more than one column unless otherwise specified
use_temp_limits = False
low_temp = 110
high_temp = 800
single_molecule_name = 'Furfural'
surface = 'Pt(100)'

# any vertical dotted lines go here
# dotted_lines = [204.7, 161, 395, 428]
# dotted_lines = [204.7, 161, 260, 395, 428]

# names of molecules and their mass from the QMS goes here.
# HREELS Chamber, PPPL

# dict_values = dict({'HOAC': 61.297,
#                     'CO': 28.2,
#                     'H2': 1.5,
#                     'H2O': 17.9,
#                     'CO2': 44.7})

# IR Chamber

#dict_values = dict({'HOAC': 60.08,
                    # 'CO': 27.7,
                    # 'H2':1.87,
                    # 'H2O':17.5,
                    # 'CO2': 43.,
                    # 'CH2': 14.6,
                    # 'ethane': 26.77,
                    # 'EtOH': 30.75,
                    # 'ketene': 13.,
                    # '43': 42.6})
#furfural
dict_values = dict({'H2': 1.994,
                    'H2O': 17.7,
                    'CO':27.9,
                    '39':39.,
                    'Propylene': 41.,
                    'Furan': 68.6,
                    'Mefuran': 82.8,
                    'Furfural': 97.08,
                    'GUA' : 125.5,
                    'anisole': 109.5,
                    'catechol' : 111.4,
                    'benzene': 78.8,
                    'phenol': 95.0,
                    'eth':26.9,
                    'formaldehyde':28.93,
                    'methanol/ethanol': 30.9})

# dict_values = dict(())
# integrating temp values. Put the temperature range in starting from low to high
# temp_values = dict({'HOAC': (140, 220),
#                     'CO': (320, 450),
#                     'H2': (200, 410),
#                     'H2O': (250, 450),
#                     'CO2': (250, 450),
#                     })

# to calculate areas under peaks put in the temp range value
temp_values = dict({'H2': (250,750),
                    'CO': (330,535),
                    'Furfural': (150,250)})