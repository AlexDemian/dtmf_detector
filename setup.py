
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
# cli command: python setup.py build_ext --inplace
ext_modules=[ Extension("goertzel",
              ["goertzel.pyx"],
              libraries=["m"],
              extra_compile_args = ["-O3","-funroll-loops","-ffast-math"])]

setup(
  name = "goertzel",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules)