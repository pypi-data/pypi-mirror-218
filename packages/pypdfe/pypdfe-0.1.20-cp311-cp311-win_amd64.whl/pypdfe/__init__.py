"""
pyPDFe
======

A Python package for PDF estimation using Dr. Jennifer Farmer's PDFe and multivariate PDF libraries.

Usage:
    Import pypdfe and call the get_pdf() method on your data and add the optional "resolution" parameter.
    For example:

    '''\n
    import pypdfe\n
    PDF = pypdfe.get_pdf(data, resolution=10)\n
    '''

    The data is expected to be a numpy array of shape (n, d) where n is the number of samples and d is the number of
    dimensions.

    The resolution parameter is the number of bins to use in the PDF estimation. The default value is 10.
"""

from __future__ import annotations
from ._pypdfe import __version__, _getpdf
import numpy as np


def get_pdf(data, resolution=10, debug=0):
    data = data.astype(float)
    if len(data.shape) == 1:
        data = np.atleast_2d(data).T
    x = np.zeros((resolution, data.shape[1]), dtype=float, order='F')
    pdf = np.zeros([resolution for _ in range(data.shape[1])], dtype=float, order='F')
    _getpdf(data, resolution, debug, x, pdf)
    return x, pdf


__all__ = ['__doc__', '__version__', 'get_pdf']
