Simple tool for searching DTMF-keys in .wav audiofile based on cython Goertzel algorithm implementation.
Many thanks to Valentine Zaretsky for help in creation cython extension.

Succesfully tested on mono .wav 8kHz recording 

# Requirements:

Numpy

Wave

Cython(for recompilition)


# For recompilition: 

python setup.py build_ext --inplace

# Usage:

python dtfm_detector.py sample.wav

# Configuration

Modify config.txt so set up your searchrules

