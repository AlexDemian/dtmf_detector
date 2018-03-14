Simple tool for searching DTMF-keys in .wav audiofile based on cython Goertzel algorithm implementation.
Many thanks to Valentine Zaretsky for help in creation cython extension.

Succesfully tested on mono .wav 8kHz recording 

For recompilition: 
python setup.py build_ext --inplace

For test:
python dtfm_detector.py
