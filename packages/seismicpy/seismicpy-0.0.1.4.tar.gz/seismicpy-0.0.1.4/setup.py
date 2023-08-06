#!/usr/bin/env python
# -*- encoding: utf8 -*-
# import glob
# import inspect
# import io
# import os

from setuptools import setup
from distutils.core import Extension
import numpy


long_description = """
Source code: https://github.com/chenyk1990/pyseis""".strip() 


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")).read()

from distutils.core import Extension

npre3d_module = Extension('npre3dcfun', sources=['pyseis/src/npre3d.c',
												'pyseis/src/seis_fxynpre.c',
												'pyseis/src/seis_alloc.c',
												'pyseis/src/seis_kissfft.c',
												'pyseis/src/seis_komplex.c',
												'pyseis/src/seis_conjgrad.c',
												'pyseis/src/seis_cdivn.c',
												'pyseis/src/seis_triangle.c',
												'pyseis/src/seis_trianglen.c',
												'pyseis/src/seis_ntriangle.c',
												'pyseis/src/seis_ntrianglen.c',		
												'pyseis/src/seis_decart.c',	
												'pyseis/src/seis_win.c',	
												'pyseis/src/seis_memcpy.c',			
												'pyseis/src/seis_fft1.c'],
												include_dirs=[numpy.get_include()])

# eikonalvtic_module = Extension('eikonalvtic', sources=['pyekfmm/src/eikonalvti.c'], 
# 										include_dirs=[numpy.get_include()])
										
# from numpy.distutils.core import setup 
setup(
    name="seismicpy",
    version="0.0.1.4",
    license='GNU General Public License, Version 3 (GPLv3)',
    description="A python package for seismic data processing and inversion",
    long_description=long_description,
    author="pyseis developing team",
    author_email="chenyk2016@gmail.com",
    url="https://github.com/chenyk1990/pyseis",
    ext_modules=[npre3d_module],
    packages=['pyseis'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    keywords=[
        "seismology", "earthquake seismology", "exploration seismology", "array seismology", "denoising", "science", "engineering", "structure", "local slope", "filtering"
    ],
    install_requires=[
        "numpy", "scipy", "matplotlib"
    ],
    extras_require={
        "docs": ["sphinx", "ipython", "runipy"]
    }
)
