#!/usr/bin/env python
# V1.0.0: Michele Cappellari, Oxford, 5 November 2014
# V1.0.1: Fixed deprecation warning. MC, Oxford, 1 October 2015
# V1.0.2: Changed imports for ltsfit as package. MC, Oxford, 17 April 2018
# V2.0.0: Adapted to use lts_hyperfit. MC, Oxford, 7 July 2023

import numpy as np
import matplotlib.pyplot as plt

from ltsfit.lts_hyperfit import lts_hyperfit

#------------------------------------------------------------------------------

def lts_linefit_example():
    """
    Usage example for lts_linefit()
    In this extreme example I assume that
    40% of the values are strong outliers

    """
    print('-'*70 + "\nRunning lts_linefit_example\n")

    ntot = 300 # Number of values

    # Coefficients of the test line
    #
    a = 10.
    b = 0.5

    n = int(ntot*0.6)  # 60% good values
    np.random.seed(913)
    x = np.random.uniform(18.5, 21.5, n)
    y = a + b*x

    sig_int = 0.3 # Intrinsic scatter in y
    y += np.random.normal(0, sig_int, n)

    sigx = 0.1 # Observational error in x
    sigy = 0.2 # Observational error in y
    x += np.random.normal(0, sigx, n)
    y += np.random.normal(0, sigy, n)

    # Outliers produce a background of spurious values
    # intersecting with the true distribution
    #
    nout = int(ntot*0.4)   # 40% outliers
    x1 = np.random.uniform((max(x) + min(x))/2, max(x), nout)
    y1 = np.random.uniform(20, 26, nout)

    # Combines the good values and the outliers in one vector
    #
    x = np.append(x, x1)
    y = np.append(y, y1)

    sigx = np.full_like(x, sigx)  # Adopted error in x
    sigy = np.full_like(x, sigy)  # Adopted error in y

    # Important: use the kwyword `pivot` as done below
    plt.clf()
    p = lts_hyperfit(x, y, sigx, sigy, pivot=np.median(x))
    plt.pause(1)

    # Illustrates how to obtain the best-fitting values from the class
    print(f"The best fitting parameters are: {p.abc}\n")

#------------------------------------------------------------------------------

def lts_planefit_example():
    """
    Usage example for lts_planefit()

    """
    print('-'*70 + "\nRunning lts_planefit_example\n")

    ntot = 300  # Number of values

    # Coefficients of the test line
    #
    a = 10.
    b = 2.
    c = 1.

    n = int(ntot*0.6)
    np.random.seed(915)
    x = np.random.uniform(17.5, 22.5, n)
    y = np.random.uniform(7.5, 12.5, n)
    z = a + b*x + c*y

    sig_int = 1  # Intrinsic scatter in z
    z = np.random.normal(z, sig_int, n)

    sigx = 0.2  # Observational error in x
    sigy = 0.4  # Observational error in y
    sigz = 0.4  # Observational error in z
    x = np.random.normal(x, sigx, n)
    y = np.random.normal(y, sigy, n)
    z = np.random.normal(z, sigz, n)

    # Outliers produce a background of spurious values
    # intersecting with the true distribution
    #
    nout = int(ntot*0.4)  # 40% outliers
    x1 = np.random.uniform(10, 30, nout)
    y1 = np.random.uniform(20, 40, nout)
    z1 = np.random.uniform((max(z) + min(z))/2, max(z), nout)

    # Combines the good values and the outliers in one vector
    #
    x = np.append(x, x1)
    y = np.append(y, y1)
    z = np.append(z, z1)

    sigx = np.full_like(x, sigx)  # Adopted error in x
    sigy = np.full_like(x, sigy)  # Adopted error in y
    sigz = np.full_like(x, sigz)  # Adopted error in z

    plt.clf()
    data = np.column_stack([x, y])
    sigdata = np.column_stack([sigx, sigy])
    p = lts_hyperfit(data, z, sigdata, sigz, pivot=np.median(data, 0))
    plt.pause(1)

    # Illustrates how to obtain the best-fitting values from the class
    print(f"The best fitting parameters are: {p.abc}\n")

#------------------------------------------------------------------------------

def lts_hyperfit_example():
    """
    Usage example for lts_hyperfit()
    In this extreme example I assume that
    40% of the values are strong outliers

    """
    print('-'*70 + "\nRunning lts_hyperfit_example\n")

    ntot = 300  # Number of values

    # Coefficients of the test line
    #
    a = 10.
    b = 2.
    c = 1.
    d = 3.

    n = int(ntot*0.6)
    np.random.seed(915)
    x1 = np.random.uniform(17.5, 22.5, n)
    x2 = np.random.uniform(7.5, 12.5, n)
    x3 = np.random.uniform(5, 9, n)
    z = a + b*x1 + c*x2 + d*x3

    sig_int = 1  # Intrinsic scatter in z
    z = np.random.normal(z, sig_int, n)

    sigx1 = 0.2     # Observational error in x1
    sigx2 = 0.4     # Observational error in x2
    sigx3 = 0.4     # Observational error in x3
    sigz = 0.25     # Observational error in z
    x1 = np.random.normal(x1, sigx1, n)
    x2 = np.random.normal(x2, sigx2, n)
    x3 = np.random.normal(x3, sigx3, n)
    z = np.random.normal(z, sigz, n)

    # Outliers produce a background of spurious values
    # intersecting with the true distribution
    #
    nout = int(ntot*0.4)  # 40% outliers
    x1bad = np.random.uniform(10, 30, nout)
    x2bad = np.random.uniform(20, 40, nout)
    x3bad = np.random.uniform(4, 20, nout)
    zbad = np.random.uniform((max(z) + min(z))/2, max(z), nout)

    # Combines the good values and the outliers in one vector
    #
    x1 = np.append(x1, x1bad)
    x2 = np.append(x2, x2bad)
    x3 = np.append(x3, x3bad)
    z = np.append(z, zbad)

    sigx1 = np.full_like(z, sigx1)  # Adopted error in x1
    sigx2 = np.full_like(z, sigx2)  # Adopted error in x2
    sigx3 = np.full_like(z, sigx3)  # Adopted error in x3
    sigz = np.full_like(z, sigz)    # Adopted error in z

    plt.clf()
    data = np.column_stack([x1, x2, x3])
    sigdata = np.column_stack([sigx1, sigx2, sigx3])
    p = lts_hyperfit(data, z, sigdata, sigz, pivot=np.median(data, 0))
    plt.pause(1)

    # Illustrates how to obtain the best-fitting values from the class
    print(f"The best fitting parameters are: {p.abc}\n")

#------------------------------------------------------------------------------


if __name__ == '__main__':

    lts_linefit_example()
    lts_planefit_example()
    lts_hyperfit_example()
