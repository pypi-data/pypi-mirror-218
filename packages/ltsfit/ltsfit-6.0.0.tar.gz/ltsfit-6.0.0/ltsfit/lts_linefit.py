"""
This is a wrapper for old code that uses the lts_linefit procedure.
For new code, it is better to call lts_hyperfit directly.
Michele Cappellari, 7 July 2023

"""
from .lts_hyperfit import lts_hyperfit

class lts_linefit(lts_hyperfit):

    def __init__(self, x0, y, sigx, sigy, clip=2.6, epsy=True, label='Fitted',
                 label_clip='Clipped', frac=None, pivot=0, plot=True,
                 text=True, corr=True):

        super().__init__(x0, y, sigx, sigy, clip=clip, corr=corr, epsz=epsy,
                 frac=frac, label=label, label_clip=label_clip, pivot=pivot,
                 plot=plot, text=text)

        self.ab     = self.abc
        self.ab_err = self.abc_err

