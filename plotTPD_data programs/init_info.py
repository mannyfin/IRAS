"""
First off, change the stuff in the "Preliminary stuff" section
1. Make sure masses are added to the dictionary as needed from either the UTI or Hiden RGA
2. If a key is listed, no need to re-add the key. {key : value}
3. IMPORTANT, MAKE SURE YOU ADD ANY TEMPERATURE RANGES YOU WANT TO INTEGRATE FOR AN UPTAKE CURVE

"""

# Preliminary stuff
# Display of temp range on plots. These limits are null if there is more than one column unless otherwise specified
use_temp_limits = True
slope_subtract = True
legend = 'on'
monolayer = '0.015 L'
low_temp = 100
high_temp = 800
single_molecule_name = 'Guaiacol'
# single_molecule_name = 'Furfural'
sat_CO_area = 2253432
surface = 'Pt(100)'
# to calculate areas under peaks put in the temp range value
temp_values = dict({'H2': (250,750),
                    'CO': (330,550),
                    'Benzene': (310,460),
                    'Furfural': (130,250),
                    'GUA': (290, 360)
                    })

# 'GUA': (170,375) -> total
# 'GUA': (290,360) -> recombinative peak
# 'GUA': (208,250) -> 2nd physisorbed layer
# 'Furfural': (188,250), --> mono
# 'Furfural': (130,250), --> mono + multi
# 'Furfural': (150,250), --> old

# add dict values here:
dict_values = dict({'1.879': 'H2',
                    '1.922': 'H2',
                    '1.933': 'H2',
                    '1.9708': 'H2',
                    '1.971': 'H2',
                    '1.994': 'H2',
                    '2.071': 'H2',
                    '11.679': 'C',
                    '13.642': '14',
                    '14.639': '15',
                    '14.708': 'CH4',
                    '17.627': 'H2O',
                    '17.798': 'H2O',
                    '17.701': 'H2O',
                    '17.737': 'H2O',
                    '17.847': 'H2O',
                    '26.9': '27-eth',
                    '27.708': 'CO',
                    '27.844': 'CO',
                    '27.883': 'CO',
                    '27.907': 'CO',
                    '27.993': 'CO',
                    '28.936': 'Formaldehyde',
                    '30.937': '31-ol',
                    '39.000': '39',
                    '39.': '39',
                    '40.816': 'Propylene',
                    '42.078': 'Ketene',
                    '43.905': 'CO2',
                    '68.654': 'Furan',
                    '78.423': 'Benzene',
                    '78.871': 'Benzene',
                    '78.8': 'Benzene',
                    '82.865': 'Me-furan',
                    '95.0': 'Phenol',
                    '95.042': 'Phenol',
                    '97.084': 'Furfural',
                    'Hydrogen': 'H2',
                    'Water': 'H2O',
                    'Carbon monoxide': 'CO',
                    'furan39': '39',
                    'Propene': 'Propylene',
                    'Carbon Dioxide': 'CO2',
                    'Carbon dioxide': 'CO2',
                    'furan68': 'Furan',
                    'furf96': 'Furfural',
                    '109.505': 'Anisole',
                    '125.586': 'GUA',
                    'H2': 1.922,
                    'H2O': 17.627,
                    'CO': 27.844,
                    '39': 39.,
                    'Propylene': 41.,
                    'Furan': 68.6,
                    'Me-furan': 82.8,
                    'Furfural': 97.08,
                    'GUA': 125.5,
                    'anisole': 109.5,
                    'catechol': 111.4,
                    'benzene': 78.8,
                    'phenol': 95.0,
                    'eth': 26.9,
                    'formaldehyde': 28.93,
                    'methanol/ethanol': 30.9})
# # any vertical dotted lines go here
# # dotted_lines = [204.7, 161, 395, 428]
# # dotted_lines = [204.7, 161, 260, 395, 428]
#
# # names of molecules and their mass from the QMS goes here.
# # HREELS Chamber, PPPL
#
# # dict_values = dict({'HOAC': 61.297,
# #                     'CO': 28.2,
# #                     'H2': 1.5,
# #                     'H2O': 17.9,
# #                     'CO2': 44.7})
#
# # IR Chamber
#
# #dict_values = dict({'HOAC': 60.08,
#                     # 'CO': 27.7,
#                     # 'H2':1.87,
#                     # 'H2O':17.5,
#                     # 'CO2': 43.,
#                     # 'CH2': 14.6,
#                     # 'ethane': 26.77,
#                     # 'EtOH': 30.75,
#                     # 'ketene': 13.,
#                     # '43': 42.6})
# if single_molecule_name == 'Furfural':
#     # #furfural 'H2': 1.879
#     # dict_values = dict({'H2': 1.922,
#     #                     'H2O': 17.627,
#     #                     'CO':27.844,
#     #                     '39':39.,
#     #                     'Propylene': 41.,
#     #                     'Furan': 68.6,
#     #                     'Me-furan': 82.8,
#     #                     'Furfural': 97.08,
#     #                     'GUA' : 125.5,
#     #                     'anisole': 109.5,
#     #                     'catechol' : 111.4,
#     #                     'benzene': 78.8,
#     #                     'phenol': 95.0,
#     #                     'eth':26.9,
#     #                     'formaldehyde':28.93,
#     #                     'methanol/ethanol': 30.9})
#     #furfural 'H2': 1.879
#     dict_values = dict({'1.879': 'H2',
#                         '1.922': 'H2',
#                         '1.994': 'H2',
#                         '13.642': '14',
#                         '14.639': '15',
#                         '17.627': 'H2O',
#                         '17.7': 'H2O',
#                         '26.9': '27-eth',
#                         '27.844': 'CO',
#                         '39.000': '39',
#                         '39.': '39',
#                         '40.816': 'Propylene',
#                         '43.905': 'CO2',
#                         '68.654': 'Furan',
#                         '78.423': 'Benzene',
#                         '78.8': 'Benzene',
#                         '82.865': 'Me-furan',
#                         '95.0': 'Phenol',
#                         '97.084': 'Furfural',
#                         'Hydrogen': 'H2',
#                         'Water': 'H2O',
#                         'Carbon monoxide': 'CO',
#                         'furan39': '39',
#                         'Propene': 'Propylene',
#                         'Carbon Dioxide': 'CO2',
#                         'furan68': 'Furan',
#                         'furf96': 'Furfural',
#                         'H2': 1.922,
#                         'H2O': 17.627,
#                         'CO':27.844,
#                         '39':39.,
#                         'Propylene': 41.,
#                         'Furan': 68.6,
#                         'Me-furan': 82.8,
#                         'Furfural': 97.08,
#                         'GUA' : 125.5,
#                         'anisole': 109.5,
#                         'catechol' : 111.4,
#                         'benzene': 78.8,
#                         'phenol': 95.0,
#                         'eth':26.9,
#                         'formaldehyde':28.93,
#                         'methanol/ethanol': 30.9})
#
# elif single_molecule_name == 'Guaiacol':
#     #Guaiacol
#     dict_values = dict({'H2': 1.994,
#                         'H2O': 17.7,
#                         'CO':27.9,
#                         '39':39.,
#                         'Propylene': 41.,
#                         'Furan': 68.6,
#                         'Mefuran': 82.8,
#                         'Furfural': 97.08,
#                         'GUA' : 125.5,
#                         'anisole': 109.5,
#                         'catechol' : 111.4,
#                         'benzene': 78.8,
#                         'phenol': 95.0,
#                         'eth':26.9,
#                         'formaldehyde':28.93,
#                         'methanol/ethanol': 30.9})

# dict_values = dict(())
# integrating temp values. Put the temperature range in starting from low to high
# temp_values = dict({'HOAC': (140, 220),
#                     'CO': (320, 450),
#                     'H2': (200, 410),
#                     'H2O': (250, 450),
#                     'CO2': (250, 450),
#                     })

