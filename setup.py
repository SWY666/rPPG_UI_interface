from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy
# setup(ext_modules = cythonize(Extension(
#     'wave_process',
#     sources=['image_process.pyx'],
#     language='c',
#     include_dirs=[numpy.get_include()],
#     library_dirs=[],
#     libraries=[],
#     extra_compile_args=[],
#     extra_link_args=[]
# )))

setup(ext_modules = cythonize(Extension(
    'tttt',
    sources=['pydd.pyx'],
    language='c',
    include_dirs=[numpy.get_include()],
    library_dirs=[],
    libraries=[],
    extra_compile_args=[],
    extra_link_args=[]
)))