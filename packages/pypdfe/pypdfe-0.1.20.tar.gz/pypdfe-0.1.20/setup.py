# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
from glob import glob
import os


__version__ = "0.1.20"

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
    # url="https://github.com/CHANGE_ME",
    description="A Python package for PDF estimation using Dr. Jennifer Farmer's PDFe and multivariate PDFe libraries.",
    long_description="If you use this package, please cite the following paper:\n"
                     "https://doi.org/10.1371/journal.pone.0196937",
    ext_modules=ext_modules,
    packages=['pypdfe'],
    package_data={'pypdfe': ['_pypdfe.*']},
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=['numpy'],
)
