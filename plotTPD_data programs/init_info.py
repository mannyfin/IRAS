"""
First off, change the stuff in the "Preliminary stuff" section
1. Make sure masses are added to the dictionary as needed from either the UTI or Hiden RGA
2. If a key is listed, no need to re-add the key. {key : value}
3. IMPORTANT, MAKE SURE YOU ADD ANY TEMPERATURE RANGES YOU WANT TO INTEGRATE FOR AN UPTAKE CURVE

"""

# Preliminary stuff
# Display of temp range on plots. These limits are null if there is more than one column unless otherwise specified
use_temp_limits = True
low_temp = 110
high_temp = 800
single_molecule_name = 'Guaiacol'
sat_CO_area = 2253432
surface = 'Pt(100)'
# add dict values here:
dict_values = dict({'1.879': 'H2',
                    '1.922': 'H2',
                    '1.994': 'H2',
                    '13.642': '14',
                    '14.639': '15',
                    '17.627': 'H2O',
                    '17.7': 'H2O',
                    '26.9': '27-eth',
                    '27.844': 'CO',
                    '39.000': '39',
                    '39.': '39',
                    '40.816': 'Propylene',
                    '43.905': 'CO2',
                    '68.654': 'Furan',
                    '78.423': 'Benzene',
                    '78.8': 'Benzene',
                    '82.865': 'Me-furan',
                    '95.0': 'Phenol',
                    '97.084': 'Furfural',
                    'Hydrogen': 'H2',
                    'Water': 'H2O',
                    'Carbon monoxide': 'CO',
                    'furan39': '39',
                    'Propene': 'Propylene',
                    'Carbon Dioxide': 'CO2',
                    'furan68': 'Furan',
                    'furf96': 'Furfural',
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

# to calculate areas under peaks put in the temp range value
temp_values = dict({'H2': (250,750),
                    'CO': (330,535),
                    'Furfural': (150,250)})