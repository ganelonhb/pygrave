from setuptools import setup, Extension
from Cython.Build import cythonize


extensions = [
    Extension("grave.cimplement", ["grave/cimplement.pyx"]),
    ]

setup(
    name = "PyGrave",
    version="0.0.1",
    packages=["grave"],
    ext_modules=cythonize(extensions),
    )
