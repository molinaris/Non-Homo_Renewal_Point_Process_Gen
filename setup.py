from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
fn = 'spkCounting.pyx'

import subprocess
subprocess.call(["cython","-a",fn])

setup(name='teste',
	ext_modules=cythonize([Extension("spkCounting", [fn])]))

#compile as
# python setup.py build_ext --inplace