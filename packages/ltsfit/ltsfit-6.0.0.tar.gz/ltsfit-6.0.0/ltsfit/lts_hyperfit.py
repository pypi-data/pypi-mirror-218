# ###############################################################################
#
# Copyright (C) 2012-2023, Michele Cappellari
# E-mail: michele.cappellari_at_physics.ox.ac.uk
#
# Updated versions of the software are available from my web page
# http://purl.org/cappellari/software
#
# If you have found this software useful for your research, I would
# appreciate an acknowledgement to the use of the "LtsFit package
# described in Cappellari et al. (2013, MNRAS, 432, 1709), which
# combines the Least Trimmed Squares robust technique of Rousseeuw &
# van Driessen (2006) into a least-squares fitting algorithm which
# allows for errors in all variables and intrinsic scatter."
#
# This software is provided as is without any warranty whatsoever.
# Permission to use, for non-commercial purposes is granted.
# Permission to modify for personal or internal use is granted,
# provided this copyright and disclaimer are included unchanged
# at the beginning of the file. All other rights are reserved.
# In particular, redistribution of the code is not allowed.
#
###############################################################################
#
# MODIFICATION HISTORY:
#       V1.0.0: Michele Cappellari, Oxford, 21 March 2011
#       V2.0.0: Converted from lts_linefit. MC, Oxford, 06 April 2011
#       V2.0.1: Added PIVOT keyword, MC, Oxford, 1 August 2011
#       V2.0.2: Fixed program stop affecting earlier IDL versions.
#           Thanks to Xue-Guang Zhang for reporting the problem
#           and the solution. MC, Turku, 10 July 2013
#       V2.0.3: Scale line spacing with character size in text output.
#           MC, Oxford, 19 September 2013
#       V2.0.4: Check that all input vectors have the same size.
#           MC, Baltimore, 8 June 2014
#       V2.0.5: Text plotting changes. MC, Oxford, 26 June 2014
#       V3.0.0: Converted from IDL into Python. MC, Oxford, 5 November 2014
#       V3.0.1: Updated documentation. MC, Baltimore, 9 June 2015
#       V3.0.2: Fixed potential program stop without outliers.
#           Thanks to Masato Onodera for a clear report of the problem.
#         - Output boolean mask instead of good/bad indices.
#         - Removed lts_hyperfit_example from this file.
#           MC, Oxford, 6 July 2015
#       V3.0.3: Fixed potential program stop without outliers.
#           MC, Oxford, 1 October 2015
#       V3.0.4: Fixed potential program stop without outliers in Matplotlib 1.5.
#           MC, Oxford, 9 December 2015
#       V3.0.5: Use LimeGreen for outliers. MC, Oxford, 8 January 2016
#       V3.0.6: Check for non finite values in input.
#           MC, Oxford, 23 January 2016
#       V3.0.7: Added capsize=0 in plt.errorbar to prevent error bar caps
#           from showing up in PDF. MC, Oxford, 4 July 2016
#       V3.0.8: Fixed: store ab errors in p.ab_err as documented.
#           Thanks to Alison Crocker for the correction.
#           MC, Oxford, 5 September 2016
#       V3.0.9: Fixed typo causing full C-step to be skipped.
#           Thanks to Francesco D'Eugenio for reporting this problem.
#           Increased upper limit of intrinsic scatter accounting for
#           uncertainty of standard deviation with small samples.
#           Michele Cappellari, Oxford, 26 July 2017
#       V3.0.10: Fixed FutureWarning in Numpy 1.14. MC, Oxford, 13 April 2018
#       V3.0.11: Dropped Python 2.7 support. MC, Oxford, 12 May 2018
#       V3.0.12: Fixed clock DeprecationWarning in Python 3.7.
#           MC, Oxford, 27 September 2018
#       V3.0.13: Properly print significant trailing zeros in results.
#           Formatted documentation as dosctring. Included p.rms output.
#           MC, Oxford, 17 February 2020
#       V3.0.14: Fixed incorrect plot ranges due to a Matplotlib change.
#           Thanks to Davide Bevacqua (unibo.it) for the report.
#           MC, Oxford, 22 January 2021
#       Vx.x.x: Additional changes are documented in the CHANGELOG of the LtsFit package.
#
#------------------------------------------------------------------------------

from time import perf_counter as clock
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, stats

#----------------------------------------------------------------------------

def _hyperfit(x, z, sigz=None, weights=None):
    """
    Fit a hyperplane zfit = a + b1*x1 + b2*x2 + ...
    to a set of points (x1, x2,... , z)
    by minimizing chi2 = np.sum(((z - zfit)/sigz)**2)

    """
    v1 = np.ones_like(z)
    if weights is None:
        if sigz is None:
            sw = v1
        else:
            sw = v1/sigz
    else:
        sw = np.sqrt(weights)

    a = np.column_stack([v1, x])
    abc = np.linalg.lstsq(a*sw[:, None], z*sw, rcond=None)[0]

    return abc

#----------------------------------------------------------------------------

def _display_errors(par, sig_par, epsz):
    """ Print parameters rounded according to their uncertainties """

    prec = np.zeros_like(par)
    w = (sig_par != 0) & (par != 0)
    prec[w] = np.ceil(np.log10(np.abs(par[w]))) - np.floor(np.log10(sig_par[w])) + 1
    prec = prec.clip(0)  # negative precisions not allowed
    dg = list(map(str, prec.astype(int)))

    # print on the terminal and save as LaTeX string

    txt = ['a = '] + [f'b_{j} = ' for j in range(len(par) - 2)]
    txt1 = txt + ['scatter = ']
    for t, d, p, s in zip(txt1, dg, par, sig_par):
        print(f"{t:>12} {p:#.{d}g} +/- {s:#.2g}")

    if epsz:
        txt += ['\\varepsilon_z=']
    string = ''
    for t, d, p, s in zip(txt, dg, par, sig_par):
        string += f"${t} {p:#.{d}g} \\pm {s:#.2g}$\n"

    return string

#------------------------------------------------------------------------------

def _residuals(abc, x, z, sigx, sigz):
    """ See equation (7) of Cappellari et al. (2013, MNRAS, 432, 1709) """

    res = (abc[0] + x @ abc[1:] - z)/np.sqrt(sigx**2 @ abc[1:]**2 + sigz**2)

    return res

#----------------------------------------------------------------------------

def _fitting(x, z, sigx, sigz, abc):

    abc, pcov, infodict, errmsg, success = optimize.leastsq(
        _residuals, abc, args=(x, z, sigx, sigz), full_output=1)

    if pcov is None or np.any(np.diag(pcov) < 0):
        sig_abc = np.full(x.shape[1], np.inf)
        chi2 = np.inf
    else:
        chi2 = np.sum(infodict['fvec']**2)
        sig_abc = np.sqrt(np.diag(pcov))  # ignore covariance

    return abc, sig_abc, chi2

#----------------------------------------------------------------------------

def _fast_algorithm(x, z, sigx, sigz, h):

    # Robust least trimmed squares regression.
    # Pg. 38 of Rousseeuw & van Driessen (2006)
    # http://dx.doi.org/10.1007/s10618-005-0024-4
    #
    m = 500 # Number of random starting points
    ndim = x.shape[1] + 1
    abcv = np.empty((m, ndim))
    chi2v = np.empty(m)
    for j in range(m):  # Draw m random starting points
        w = np.random.choice(z.size, ndim, replace=False)
        abc = _hyperfit(x[w], z[w])  # Find a plane going trough three random points
        for k in range(3):  # Run C-steps up to H_3
            res = _residuals(abc, x, z, sigx, sigz)
            good = np.argsort(np.abs(res))[:h]  # Fit the h points with smallest errors
            abc, sig_abc, chi_sq = _fitting(x[good], z[good], sigx[good], sigz[good], abc)
        abcv[j, :] = abc
        chi2v[j] = chi_sq

    # Perform full C-steps only for the 10 best results
    #
    w = np.argsort(chi2v)
    nbest = 10
    chi_sq = np.inf
    for j in range(nbest):
        abc1 = abcv[w[j], :]
        while True:  # Run C-steps to convergence
            abcOld = abc1
            res = _residuals(abc1, x, z, sigx, sigz)
            good1 = np.argsort(np.abs(res))[:h]  # Fit the h points with smallest errors
            abc1, sig_ab1, chi1_sq = _fitting(x[good1], z[good1], sigx[good1], sigz[good1], abc1)
            if np.allclose(abcOld, abc1):
                break
        if chi_sq > chi1_sq:
            abc = abc1  # Save best solution
            good = good1
            chi_sq = chi1_sq

    mask = np.zeros_like(z, dtype=bool)
    mask[good] = True

    return abc, mask

#------------------------------------------------------------------------------

class lts_hyperfit:
    """
    lts_hyperfit
    ============ 

    Purpose
    -------

    Fit a linear function of the form::

        z = a + b1*x1 + b2*x2 +...+ bm*xm,

    to data with errors in all coordinates and intrinsic scatter, using a robust
    method that clips outliers. The function can handle lines in 2-dim, planes in
    3-dim, or hyperplanes in N-dim, where ``x1, x2,..., xm`` are the independent
    variables and ``z`` is the dependent variable. The method was introduced in
    Sec. 3.2 of `Cappellari et al. (2013a) <https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C>`_
    and the treatment of outliers is is based on the FAST-LTS technique by
    `Rousseeuw & van Driessen (2006) <http://doi.org/10.1007/s10618-005-0024-4>`_.
    See also `Rousseeuw (1987) <http://books.google.co.uk/books?id=woaH_73s-MwC&pg=PA15>`_.
    
    Calling Sequence
    ----------------

    .. code-block:: python

        from ltsfit.lts_hyperfit import lts_hyperfit

        p = lts_hyperfit(x, z, sigx, sigz, clip=2.6, corr=True, epsz=True,
                 frac=None, label='Fitted', label_clip='Clipped', pivot=0,
                 plot=True, text=True)

    The output values are stored as attributes of the ``p`` object.

    Input Parameters
    ----------------

    x: array_like with shape (n, m)
        Array of ``n`` independent variables for ``m`` dimensions.

        EXAMPLE: To fit a line in 2-dim, one has a single vector ``xx`` of
        length ``n`` with the independent variable and a corresponding vector of
        dependent variable ``yy``. In this case, ``x = xx`` and ``z = yy``.

        EXAMPLE: To fit a plane in 3-dim, one has two vectors of length ``n`` of
        independent variables ``(xx, yy)``. In this case, ``x = np.column_stack([xx, yy])``.

        EXAMPLE: To fit a hyperplane in 4-dim, one has three vectors of independent
        variables ``(x1, x2, x3)``. In this case, ``x = np.column_stack([x1, x2, x3])``.
    z: array_like with shape (n,)
        Vector of ``n`` measured values for each set of ``x`` variables.
    sigx: array_like with shape (n, m)
        Array of ``n`` values of ``1sigma`` uncertainties for each ``x`` 
        coordinate for ``m`` dimensions. This has the same shape as ``x``.
    sigz: array_like with shape (n,)
        Vector of ``n`` values of ``1sigma`` uncertainties for each ``z`` value.

    Optional Keywords
    -----------------

    clip: float
        Clipping threshold in ``sigma`` units. Values deviating more than
        ``clip*sigma`` from the best fit are considered outliers and are
        excluded from the fit. Default is ``2.6``, which would include 99% of
        the values for a Gaussian distribution.
    corr:
        if ``True``, the correlation coefficients are printed on the plot.
    epsz: bool
        If ``True``, the intrinsic scatter is printed on the output plot.
        Default is ``True``.
    frac: float
        Fraction of values to include in the LTS stage.
        Up to a fraction ``frac`` of the values can be outliers.
        One must have ``0.5 <= frac <= 1``. Default is ``0.5``.

        NOTE: Set ``frac=1`` to turn off outliers detection.
    pivot: array_like with shape (m,)
        If nonzero, then ``lts_hyperfit`` fits the hyperplane::

            z = a + b0*(x0 - pivot[0]) + b1*(x1 - pivot[1]) + ... + bm*(xm - pivot[m])

        ``pivot`` are called ``x_0``, ``y_0`` in eq.(7) of `Cappellari et al. (2013a)`_.
        Use of this parameter is strongly recommended, and suggested
        values are ``pivot = np.median(x, 0)``. The fitted parameters are not
        strongly dependent on the precise value of this parameter. For this
        reason it is generally better to round the pivot values to nice numbers.
        This parameter is important to reduce the covariance between the
        coefficients. Default is ``0``.
    plot: bool
        If ``True``, a plot of the fit is produced. Default is ``True``.
    text: bool
        If ``True``, the best fitting parameters are printed on the plot.
        Default is ``True``.

    Output Parameters
    -----------------

    The output values are stored as attributes of the ``lts_hyperfit`` class.

    p.abc: array_like with shape (m+1,)
        Best fitting parameters ``[a, b1, b2,..., bm]``.
    p.abc_err: array_like with shape (m+1,)
        ``1*sigma`` formal errors ``[a_err, b1_err, b2_err,..., bm_err]`` on
        ``[a, b1, b2,..., bm]``.
    p.mask: array_like with shape (n,) and dtype bool
        Boolean vector indicating which elements of ``z`` were included in
        the fit (``True``) and which were clipped as outliers (``False``).
    p.rms: float
        RMS deviation between the data and the fitted relation.
    p.sig_int: float
        Intrinsic scatter in the ``z`` direction around the hyperplane.
        ``sig_int`` is called ``epsilon_z`` in eq.(7) of `Cappellari et al. (2013a)`_.
    p.sig_int_err: float
        ``1*sigma`` formal error on ``sig_int``.

    ###########################################################################

    """

    def __init__(self, x0, z, sigx, sigz, clip=2.6, corr=True, epsz=True,
                 frac=None, label='Fitted', label_clip='Clipped', pivot=None,
                 plot=True, text=True):

        if x0.ndim == 1:
            x0, sigx = x0[:, None], sigx[:, None]

        n, ndim = x0.shape
        assert x0.shape == sigx.shape, 'x and sigx must have the same shape'
        assert n == z.size == sigz.size, 'z, sigz must have length x.shape[0]'

        if pivot is None:
            print(
                'WARNING: Using a nonzero `pivot` keyword is always reccomended')
            pivot = np.zeros(ndim)
        else:
            pivot = np.atleast_1d(pivot)

        if not np.all(np.isfinite(np.column_stack([x0, z, sigx, sigz]))):
            raise ValueError('Input contains non finite values')

        t = clock()

        p = ndim + 1  # space dimension
        n = z.size
        h = int((n + p + 1)/2) if frac is None else int(
            max(round(frac*n), (n + p + 1)/2))

        x = x0 - pivot
        self._single_fit(x, z, sigx, sigz, h, clip)
        self.rms = np.std(
            self.abc[0] + x[self.mask]@self.abc[1:] - z[self.mask], ddof=p)

        par = np.append(self.abc, self.sig_int)
        sig_par = np.append(self.abc_err, self.sig_int_err)
        print('################# Values and formal errors ################')
        string = _display_errors(par, sig_par, epsz)
        print(f'Observed rms scatter: {self.rms:#.2g}')

        ylabel = 'a + ' + ' + '.join(
            [f'(x_{j} - p_{j}) b_{j}' for j in range(ndim)])
        print('z = ' + ylabel)
        for j, piv in enumerate(pivot):
            print(f'   p_{j} = {pivot[j]:#.4g}')
        if p == 2:
            x, x0, sigx = map(np.ravel, [x, x0, sigx])
            print('Spearman r=%#.2g and p=%#.2g'%stats.spearmanr(x, z))
            print('Pearson r=%#.2g and p=%#.2g'%stats.pearsonr(x, z))

        print('##########################################################')

        print('seconds %.2f'%(clock() - t))

        if plot:

            if p == 2:
                xx = x0
                zz = z
                xerr = sigx
                yerr = sigz
                xlabel = '$x_0$'
                ylabel = '$y,\quad y_{\\rm fit} = a + (x_0 - p_{0}) b_0$'
            else:
                xx = z
                zz = par[0] + x@par[1:-1]
                xerr = sigz
                yerr = np.sqrt(sigx**2@par[1:-1]**2)
                xlabel = 'z'
                ylabel = '$' + ylabel + '$'

            plt.errorbar(xx[self.mask], zz[self.mask], xerr=xerr[self.mask],
                         yerr=yerr[self.mask], fmt='ob', capthick=0, capsize=0,
                         label=label)
            plt.errorbar(xx[~self.mask], zz[~self.mask], xerr=xerr[~self.mask],
                         yerr=yerr[~self.mask], fmt='d', color='LimeGreen',
                         capthick=0, capsize=0, label=label_clip)

            xlim = np.array(plt.gca().get_xlim())
            y1 = par[0] + par[1]*(xlim - pivot) if p == 2 else xlim

            plt.plot(xlim, y1, '-k', xlim, y1 + self.rms, '--r', xlim,
                     y1 - self.rms, '--r', xlim, y1 + 2.6*self.rms, ':r', xlim,
                     y1 - 2.6*self.rms, ':r', linewidth=2, zorder=1)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title('Best fit, 1$\sigma$ (68%) and 2.6$\sigma$ (99%)')

            ax = plt.gca()
            ax.minorticks_on()
            if text:
                string += f'$\Delta={self.rms:#.2g}$\n'
                if np.any(pivot):
                    for j, piv in enumerate(pivot):
                        string += f'$(p_{j}={piv:#.4g})$\n'
                ax.text(0.05, 0.95, string, horizontalalignment='left',
                        verticalalignment='top', transform=ax.transAxes)

            if (p == 2) and corr:
                txt = '${\\rm Spearman/Pearson}$\n'
                txt += '$r=%#.2g\, p=%#.2g$\n'%stats.spearmanr(x, z)
                txt += '$r=%#.2g\, p=%#.2g$\n'%stats.pearsonr(x, z)
                ax.text(0.95, 0.95, txt, horizontalalignment='right',
                        verticalalignment='top', transform=ax.transAxes)

    # ------------------------------------------------------------------------------
    def _find_outliers(self, sig_int, x, z, sigx, sigz1, h, offs, clip):

        sigz = np.sqrt(sigz1**2 + sig_int**2) # Gaussian intrinsic scatter

        if h == len(x): # No outliers detection

            abc = _hyperfit(x, z, sigz=sigz)  # quick initial guess
            abc, sig_abc, chi_sq = _fitting(x, z, sigx, sigz, abc)
            mask = np.ones_like(z, dtype=bool)  # No outliers

        else: # Robust fit and outliers detection

            # Initial estimate using the maximum breakdown of
            # the method of 50% but minimum efficiency
            #
            abc, mask = _fast_algorithm(x, z, sigx, sigz, h)

            # inside-out outliers removal
            #
            while True:
                res = _residuals(abc, x, z, sigx, sigz)
                sig = np.std(res[mask], ddof=abc.size)
                maskOld = mask
                mask = np.abs(res) < clip*sig
                abc, sig_abc, chi_sq = _fitting(x[mask], z[mask], sigx[mask], sigz[mask], abc)
                if np.array_equal(mask, maskOld):
                    break

        # To determine 1sigma error on the intrinsic scatter the chi2
        # is decreased by 1sigma=sqrt(2(h-3)) while optimizing (a,b,c)
        #
        h = mask.sum()
        dchi = np.sqrt(2*(h - abc.size)) if offs else 0.

        self.abc = abc
        self.abc_err = sig_abc
        self.mask = mask

        err = (chi_sq + dchi)/(h - abc.size) - 1
        print('sig_int: %10.4f  %10.4f' % (sig_int, err))

        return err

#------------------------------------------------------------------------------

    def _single_fit(self, x, z, sigx, sigz, h, clip):

        if self._find_outliers(0, x, z, sigx, sigz, h, 0, clip) < 0:
            print('No intrinsic scatter or errors overestimated')
            sig_int = 0.
            sig_int_err = 0.
        else:
            sig1 = 0.
            ndim = x.shape[1] + 1
            res = self.abc[0] + x @ self.abc[1:] - z  # Total residuals ignoring measurement errors
            std = np.std(res[self.mask], ddof=ndim)
            sig2 = std*(1 + 3/np.sqrt(2*self.mask.sum()))  # Observed scatter + 3sigma error
            print('Computing sig_int')
            sig_int = optimize.brentq(self._find_outliers, sig1, sig2,
                                      args=(x, z, sigx, sigz, h, 0, clip), rtol=1e-3)
            print('Computing sig_int error') # chi2 can always decrease
            sigMax_int = optimize.brentq(self._find_outliers, sig_int, sig2,
                                         args=(x, z, sigx, sigz, h, 1, clip), rtol=1e-3)
            sig_int_err = sigMax_int - sig_int

        self.sig_int = sig_int
        self.sig_int_err = sig_int_err

        print('Repeat at best fitting solution')
        self._find_outliers(sig_int, x, z, sigx, sigz, h, 0, clip)

#------------------------------------------------------------------------------

