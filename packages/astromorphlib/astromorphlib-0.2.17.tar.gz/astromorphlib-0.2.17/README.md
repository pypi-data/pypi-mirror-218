# astromorphlib

Python scripts to analyze the morphology of isolated and interacting galaxies.
The package is designed to download S-PLUS (https://splus.cloud/) and
Legacy (https://www.legacysurvey.org) images automatically. There are functions
to calculate a 2D sky background of the images and deblended segmentation maps of
interacting systems with merger isophotes. The non-parametric analysis is
performed by using a decorator of the `statmorph` package (https://github.com/vrodgom/statmorph).  The user can study the environment of the object/system by downloading a list of the galaxies within Field-of-View of S-PLUS/Legacy images from SIMBAD server
(http://simbad.u-strasbg.fr/simbad/). In addition, there is a function to display DSS2 (http://alasky.u-strasbg.fr/hips-image-services/hips2fits) images of any size.

(c) 2021-2022 J. A. Hernandez-Jimenez

E-mail: joseaher@gmail.com

Website: https://gitlab.com/joseaher/astromorphlib

## Installation

astromorphlib requires:

    * statmorph
    * splusdata
    * astroplotlib
    * numpy
    * scipy
    * matplotlib
    * astropy
    * astroquery
    * wget


This version can be easily installed within Anaconda Enviroment via PyPI:

    % pip install astromorphlib

If you prefer to install astromorphlib manually, you can clone the developing
version at https://gitlab.com/joseaher/astromorphlib. In the directory this
README is in, simply:

    % pip install .

or,

    % python setup.py install

## Uninstallation

To uninstall astromorphlib, simply

    % pip uninstall astromorphlib


## Acknowledgements

This software was funded partially by Brazilian agency FAPESP,
process number 2021/08920-8.
