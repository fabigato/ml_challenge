## [1.2.1] - 2018-11-21
- improved format of the meta file, added information and minor bug fixes

## [1.2.0] - 2018-11-19
- create a meta data file with all relevant aspects of data set generation
- added the biyective column swap. A seed saved in the meta data is all what's needed to reswap
- added a transformations.reconstruction function, that given a transformed image and the metadata of all the transformations it went through, gives the original image back

## [1.1.0] - 2018-11-15
- added consitent noise
- replaced bernoulli noise function. Now a single function handles that functionality and the consistent noise one
- fixed issue with dipoles where if one of the 2 ellipes is much smaller, it doesn't get as much ink. Now the color
of each pixel is normalized so that the rim is 1
- added background shade noise
- modified data set config file so that it allows filters
- added transformations (cut and vectorize)
- transformations can be specified in config file

## [1.0] - 2018-11-14
- finished basic pipeline: data set comprised of images from 3 classes can be generated given a yaml config file
- added gaussian filter noise
- added bernoulli pixel flip noise
- minor PEP8 corrections

## [0.0.2] - 2018-11-13
- corrected a bug in the random origin generation for ellipse, which made it never offset towards negative (left half of canvas)
- corrected the size of the ellipse as a function of canvas size, since the same random generation constants that workd for 100x100
canvas, didn't work for 32x32
- added the dipole class
- added the snow class

## [0.0.1] - 2018-11-12
- Added generation for ellipse class

