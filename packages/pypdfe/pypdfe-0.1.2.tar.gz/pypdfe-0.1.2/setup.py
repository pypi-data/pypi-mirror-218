# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
from glob import glob
import os

__version__ = "0.1.2"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)
sources = sorted(
    glob(f'{os.path.dirname(os.path.realpath(__file__))}{os.sep}src{os.sep}**{os.sep}*.cpp', recursive=True))
depends = sorted(glob(f'{os.path.dirname(os.path.realpath(__file__))}{os.sep}src{os.sep}**{os.sep}*.h', recursive=True))
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
    install_requires=[
        'setuptools',
        'pybind11',
        'numpy',
    ],
)
