# IRAS

This repository is used to facilitate quick data analysis and plots (effectively in _real time_) of our temperature
programmed desorption (TPD) data and Infrared Reflection Absorption Spectroscopy (IRAS) data. As a result, I have been
able to conduct 2-3x more experiments than before.

It is a code that I use for my research and that I update whenever necessary.

The programs can be found in the 'plotTPD_data programs' folder and the necessary files can be found under 'molecule
name' + work (ex. GUA work). I also have some other small utilities for some on the fly calculations.

TPD (`plot_TPD_main.py`)::
To begin, open init_info.py and fill in the fields
. plot TPD file (using seaborn if desired)
. Perform slope subtraction and/or background subtraction
. Integrate area for uptake curve by either using an additional slope subtraction (for peaks w/in another peak) or
plain area between two temperatures (points)
. Produce plots of:
    a) all  the masses for a particular file
    b) all the files for a particular mass (i.e. all the H2O curves from all the files together)
    c) uptake plot (area vs L)
    d) a table of the areas
. It will also output the areas to an excel file named 'MoleculeName Area_output.xlsx'
. Ordering of the files when you pick them is not necessary as long as the files fit a consistent naming convention in
my files

IRAS (any program with `IR` in the filename) ::

. Quick plotter for producing plots of IR data
. Also plots reference spectra from NIST
. Can do scaling of plots to compare relative peak heights of one spectra to another in the same plot