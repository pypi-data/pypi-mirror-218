from dataclasses import dataclass

import numpy as np
from scipy.stats.mstats import mquantiles

from ._base import BaseFeature


@dataclass()
class PercentDifferenceMagnitudePercentile(BaseFeature):
    p: float = 0.05

    def _eval(self, t, m, sigma=None):
        median = np.median(m)
        q1, q2 = mquantiles(m, [self.p, 1 - self.p], alphap=0.5, betap=0.5)
        return (q2 - q1) / median

    @property
    def size(self):
        return 1


__all__ = ("PercentDifferenceMagnitudePercentile",)
