#!/usr/bin/env python
import os
import platform
from setuptools import setup, find_packages
from setuptools.extension import Extension
from distutils.command.build_ext import build_ext
import numpy as np


USE_CYTHON = 'CYTHONIZE' in os.environ
IS_PYPY = platform.python_implementation() == 'PyPy'
ext = '.pyx' if USE_CYTHON else '.c'
extensions = [
    Extension("scrapely._htmlpage",
              ["scrapely/_htmlpage%s" % ext],
              include_dirs=[np.get_include()]),
    Extension("scrapely.extraction._similarity",
              ["scrapely/extraction/_similarity%s" % ext],
              include_dirs=[np.get_include()]),
]
if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)
if IS_PYPY:
    extensions = []


class BuildExt(build_ext):
    def build_extension(self, ext):
        if USE_CYTHON:
            ext.sources = [cythonize(src) for src in ext.sources]
        try:
            return build_ext.build_extension(self, ext)
        except Exception as e:
            print(e)
        print("WARNING: Failed to compile extension modules.")
        print("fallback pure python implementation.")


setup(
    name='scrapely',
    version='0.13.0b1',
    cmdclass={'build_ext': BuildExt},
    license='BSD',
    description='A pure-python HTML screen-scraping library',
    author='Scrapy project',
    author_email='info@scrapy.org',
    url='https://github.com/scrapy/scrapely',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    install_requires=['numpy', 'w3lib', 'six'],
    extras_require={
        'speedup': ['cython']
    },
    ext_modules=extensions,
)
