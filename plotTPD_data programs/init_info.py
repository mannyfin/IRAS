"""
First off, change the stuff in the "Preliminary stuff" section
1. Make sure masses are added to the dictionary as needed from either the UTI or Hiden RGA
2. If a key is listed, no need to re-add the key. {key : value}
3. IMPORTANT, MAKE SURE YOU ADD ANY TEMPERATURE RANGES YOU WANT TO INTEGRATE FOR AN UPTAKE CURVE

"""

#################################### Preliminary stuff ####################################

"Export the data"
export = False
"suppress plots"
suppress_plots = False
"Perform a background slope subtraction of the data"
# if slope subtract is true, then it also performs subtraction between the temp_values variable for integration below
slope_subtract = True

"legend, on or off"
legend_disp = 'off'

"Plot the experiment TPD file"
plot_whole_file = True

"Where is the monolayer? This will search the filenames for the exposure and plot those particular plots in red"
monolayer = '0.04 L'
# monochrome in curves other than monolayer
monochrome = False

"Axes limits on plots, and whether to use them"
# Display of temp range on plots. These limits are null if there is more than one column unless otherwise specified

use_temp_limits = True
low_temp = 100
high_temp = 800

"Molecule name"
# single_molecule_name = 'Acetic acid'
# single_molecule_name = 'Guaiacol'
single_molecule_name = 'Furfural'

"Saturation areas of a reference molecule"
"These aren't used in calculations for this program at the moment, but are definitely used in additional processing."
# On IR Chamber with UTI 100C
# sat_CO_area_Pt = 2253432
# sat_H2_area_Pt = 274878 #average of 400 L and 2400 L H2 exposures using 220 and 450 as limits of integration

# on MB Chamber with Hiden RGA:
# H2 coverage on Pt(100) is 1.1E15 molecules/cm^2 @200K ads
sat_H2_area_Pt = 6.09407E-06  # See file "Combined H2 TPD with areas calculated.xlsx" The integrands were 215-450 K
sat_CO_area_Pt = 2.09037E-05  # See file "Combined CO TPD with areas calculated.xlsx" The integrands were 215-550 K

# surface = 'Ni(110)'
surface = 'Pt(100)'

###########################################################################################

"to calculate areas under peaks put in the temp range values"
if single_molecule_name == 'Acetic acid':
    "HOAc"
    temp_values = dict({'H2': (190, 570),
                        'Water': (280, 335),
                        'CO': (360, 500),
                        'CO2': (320, 570),
                        'HOAc': (130, 300),
                        })
# using UTI 100C
# sat_CO_area = 2253432 # Pt(100)
# sat_CO_area = 75759996 # Ni(110)

# to calculate areas under peaks put in the temp range value
# temp_values = dict({'H2': (250,750),
#                     'CO': (236, 570),
#                     'CO2': (320,570),
#                     'Benzene': (310,460),
#                     'Furfural': (130,250),
#                     'GUA': (290, 360)
#                     })
elif single_molecule_name == 'Guaiacol' or 'Furfural':
    "GUA and Furfural"
    temp_values = dict({'H2': (250,750),
                        'CO': (330,550),
                        'Benzene': (310,460),
                        'Furfural': (130,250),
                        'GUA': (290, 360)
                        })


"Some notes on the molecules is listed below"

# 'GUA': (170,375) -> total
# 'GUA': (290,360) -> recombinative peak
# 'GUA': (208,250) -> 2nd physisorbed layer
# 'Furfural': (188,250), --> mono
# 'Furfural': (130,250), --> mono + multi
# 'Furfural': (150,250), --> old


# UPDATED 4252018
# 'GUA': (150,375) -> total
# 'GUA' : (150,208)-> multilayer
# 'GUA': (260,3375) -> recombinative peak
# 'GUA': (208,260) -> 2nd physisorbed layer




# add dict values here:
dict_values = dict({'1.538': 'H2',
                    '1.839': 'H2',
                    '1.879': 'H2',
                    '1.922': 'H2',
                    '1.933': 'H2',
                    '1.942': 'H2',
                    '1.962': 'H2',
                    '1.9708': 'H2',
                    '1.971': 'H2',
                    '1.994': 'H2',
                    '2.051': 'H2',
                    '2.071': 'H2',
                    '2.085': 'H2',
                    '11.679': 'C',
                    '13.642': '14',
                    '13.681': '14',
                    '13.596': '14',
                    '14.639': '15',
                    '14.600': 'CH4',
                    '14.613': 'CH4',
                    '14.708': 'CH4',
                    '14.745': 'CH4',
                    '15.166': 'CH4',
                    '15.880': '16',
                    '17.074': 'Water',
                    '17.526': 'Water',
                    '17.577': 'Water',
                    '17.627': 'Water',
                    '17.664': 'Water',
                    '17.798': 'Water',
                    '17.701': 'Water',
                    '17.737': 'Water',
                    '17.847': 'Water',
                    '17.884': 'Water',
                    '17.895': 'Water',
                    '17.903': 'Water',
                    '24.835': 'Ethylene',
                    '25.803': 'Ethylene',
                    '26.000': '26',
                    '26.712': '27-eth',
                    '26.774': '27-eth',
                    '26.890': '27-eth',
                    '26.9': '27-eth',
                    '27.000': '27-eth',
                    '27.708': 'CO',
                    '27.740': 'CO',
                    '27.745': 'CO',
                    '27.796': 'CO',
                    '27.844': 'CO',
                    '27.883': 'CO',
                    '27.907': 'CO',
                    '27.993': 'CO',
                    '28.038': 'CO',
                    '28.178': 'CO',
                    '28.219': 'CO',
                    '28.250': 'CO',
                    '28.270': 'CO',
                    '28.818': 'Formaldehyde',
                    '28.920': 'Formaldehyde',
                    '28.936': 'Formaldehyde',
                    '28.920': 'Formaldehyde',
                    '29.015': 'Formaldehyde',
                    '29.393': 'Formaldehyde',
                    '30.937': '31-ol',
                    '30.949': '31-ol',
                    '30.708': '31-ol',
                    '30.759': '31-ol',
                    '31.296': '31-ol',
                    '32.000':'32',
                    '39.000': '39',
                    '39.': '39',
                    '40.816': 'Propylene',
                    '41.000': 'Propylene',
                    '41.148': '41.148',
                    '42.035': 'Ketene',
                    '42.078': 'Ketene',
                    '42.664': 'Ketene43?',
                    '42.992': 'Acetic acid43',
                    '43.088': 'Acetic acid43',
                    '43.686': 'CO2',
                    '43.737': 'CO2',
                    '43.765': 'CO2',
                    '43.788': 'CO2',
                    '43.905': 'CO2',
                    '44.109': 'CO2',
                    '44.029': 'CO2',
                    '44.784': 'CO2',
                    '44.818': 'CO2_2',
                    '45.058': 'Acetic acid45',
                    '56.522': '56.522',
                    '57.407': 'Acetone',
                    '60.047': 'HOAc',
                    '60.080': 'HOAc',
                    '60.088': 'HOAc',
                    '60.996': 'HOAc',
                    '61.297': 'HOAc',
                    '68.654': 'Furan',
                    '78.423': 'Benzene',
                    '78.871': 'Benzene',
                    '78.8': 'Benzene',
                    '82.865': 'Me-furan',
                    '84.866': '84.866',
                    '95.0': 'Phenol',
                    '95.042': 'Phenol',
                    '97.084': 'Furfural',
                    '111.496': 'Catechol',
                    '111.548': 'Catechol',
                    'Hydrogen': 'H2',
                    'Ketene': 'Ketene',
                    'Water': 'Water',
                    'Carbon monoxide': 'CO',
                    'furan39': '39',
                    'Acetaldehyde': 'Acetaldehyde',
                    'Propene': 'Propylene',
                    'Carbon Dioxide': 'CO2',
                    'Carbon dioxide': 'CO2',
                    'Acetic acid': 'Acetic acid43',
                    'Acetic acid.1': 'HOAc',
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
                    'methanol/ethanol': 30.9
                    })


# # any vertical dotted lines go here
# # dotted_lines = [204.7, 161, 395, 428]
# # dotted_lines = [204.7, 161, 260, 395, 428]



