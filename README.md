# Description:
Simple tool for searching DTMF-sequences in .wav audiofile based on cython Goertzel algorithm implementation.
Many thanks to Valentine Zaretsky for help in creation cython extension.

Succesfully tested on mono .wav 8kHz recording 

# Requirements:

Numpy

Wave

Cython(for recompilition)

# Recompilition: 

python setup.py build_ext --inplace

# Usage:

python dtfm_detector.py sample.wav

# Configuration:

Modify config.txt so set up your searchrules

# Recommended:
Use audio with duration 2-3+ minutes for correct average audio power countation.

DTMF-sequences must be at least a bit louder then main audio. 

