import numpy as np
"""

Assume a hexagonally closed packed layer of adsorbed molecules (doesn't matter the surface)

Then, the coverage is calculated as: coverage = (2/(np.sqrt(3)*(d**2)))*1e14/(sigma

Here is a list of some surface atom densities:

Pt(100): 1.302e15
Ni(110): 1.14e15

acetic acid vdW between two O's: .5272 nm --> cov = 0.3644
"""
d = .5272 # van der waals distance of adsorbed molecule, nm
sigma = 1.14e15 #surface atomic density [atoms/cm^2]

coverage = (2/(np.sqrt(3)*(d**2)))*1e14/(sigma)

print('coverage is: {0}'.format(np.round(coverage,4)))