"""
This is a wrapper for old code that uses the lts_planeefit procedure.
For new code, it is better to call lts_hyperfit directly.
Michele Cappellari, 7 July 2023

"""
import numpy as np
from .lts_hyperfit import lts_hyperfit

class lts_planefit(lts_hyperfit):

    def __init__(self, x0, y0, z, sigx, sigy, sigz, clip=2.6, corr=False,
                 epsz=True, frac=None, label='Fitted', label_clip='Clipped',
                 pivotx=0, pivoty=0, plot=True, text=True):

        x0 = np.column_stack([x0, y0])
        sigx = np.column_stack([sigx, sigy])
        pivot = np.hstack([pivotx, pivoty])

        super().__init__(x0, z, sigx, sigz, clip=clip, corr=corr, epsz=epsz,
                         frac=frac, label=label, label_clip=label_clip,
                         pivot=pivot, plot=plot, text=text)
