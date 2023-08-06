# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from distutils import sysconfig
from setuptools import setup
from glob import glob
import shutil
# import sys
import os

import logging

# logging.basicConfig(level=logging.INFO)

__version__ = "0.1.8"

# This is not an endorsement of one of these compilers working. Most of these have not been tested.
possible_compilers = ['g++', 'clang++', 'cl', 'icc', 'bcc32', 'dmc', 'tcc', 'opencc', 'pathCC', 'pcc',
                      'CC', 'xlC', 'c++', 'armcc', 'iccarm', 'iccrenesas', 'sdcc', 'asc2.0', 'zapcc']

for possible_compiler in possible_compilers:
    path = shutil.which(possible_compiler)
    if possible_compiler:
        sysconfig.get_config_vars()['CXX'] = possible_compiler
        break

print("\n\n ==================================================================================================\n"
      f"                                        Chosen compiler: {sysconfig.get_config_vars()['CXX']}\n"
      " ==================================================================================================\n\n")

# print("Printing to console...", file=sys.stdout)

# raise Exception(f'Compiler found: {sysconfig.get_config_vars()["CXX"]}')

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
sources = sorted(
    glob(f'src{os.sep}**{os.sep}*.cpp', recursive=True))
depends = sorted(glob(f'src{os.sep}**{os.sep}*.h', recursive=True))
sources = [source for source in sources if 'mvPDFMain.cpp' not in source]

ext_modules = [
    Pybind11Extension("pypdfe._pypdfe",
                      sources=sources,
                      depends=depends,
                      )
    ]

setup(
    name="pypdfe",
    version=__version__,
    author="Nate Mauney",
    author_email="nmauney4@uncc.edu",
    url="https://github.com/CHANGE_ME",
    description="A Python package for PDF estimation using Dr. Jennifer Farmer's PDFe and multivariate PDF libraries.",
    long_description="",
    ext_modules=ext_modules,
    packages=['pypdfe'],
    package_data={'pypdfe': ['_pypdfe.*']},
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=['numpy'],
)
