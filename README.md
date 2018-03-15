Simple tool for searching DTMF-keys in .wav audiofile based on cython Goertzel algorithm implementation.
Many thanks to Valentine Zaretsky for help in creation cython extension.

Succesfully tested on mono .wav 8kHz recording 

Requirements:
Numpy
Wave
Cython(for recompilition)


For recompilition: 

python setup.py build_ext --inplace

Usage:

python dtfm_detector.py sample.wav
Modify config.txt so set up your searchrules

Default config.txt:

# Use '#' to make a comment string
# Duration per one DTMF signal in seconds
SIGNAL_DURATION = 0.08
# Fixed pause between 2 DTMF signals in seconds
PAUSE = 0
# Times signal louder then AVG(power)
LOUDER_COEFF = 2.5
# Search for DTMF-sequences:
KEYS = ['A21D','D12A']