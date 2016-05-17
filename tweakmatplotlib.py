from matplotlib.colors import Colormap
import matplotlib.cbook as cbook
from numpy import ma
import numpy as np

def _newcall_(self, X, alpha=None, bytes=False):
    if not self._isinit:
        self._init()
    mask_bad = None
    if not cbook.iterable(X):
        vtype = 'scalar'
        xa = np.array([X])
    else:
        vtype = 'array'
        xma = ma.array(X, copy=True)  # Copy here to avoid side effects.
        mask_bad = xma.mask           # Mask will be used below.
        xa = xma.filled()             # Fill to avoid infs, etc.
        del xma

    # Calculations with native byteorder are faster, and avoid a
    # bug that otherwise can occur with putmask when the last
    # argument is a numpy scalar.
    if not xa.dtype.isnative:
        xa = xa.byteswap().newbyteorder()

    if xa.dtype.kind == "f":
        # Treat 1.0 as slightly less than 1.
        vals = np.array([1, 0], dtype=xa.dtype)
        almost_one = np.nextafter(*vals)
        cbook._putmask(xa, xa == 1.0, almost_one)
        # The following clip is fast, and prevents possible
        # conversion of large positive values to negative integers.

        xa *= self.N
        np.clip(xa, -1, self.N, out=xa)

        # ensure that all 'under' values will still have negative
        # value after casting to int
        cbook._putmask(xa, xa < 0.0, -1)
        xa = xa.astype(int)
    # Set the over-range indices before the under-range;
    # otherwise the under-range values get converted to over-range.
    cbook._putmask(xa, xa > self.N - 1, self._i_over)
    cbook._putmask(xa, xa < 0, self._i_under)
    if mask_bad is not None:
        if mask_bad.shape == xa.shape:
            cbook._putmask(xa, mask_bad, self._i_bad)
        elif mask_bad:
            xa.fill(self._i_bad)
    if bytes:
        lut = (self._lut * 255).astype(np.uint8)
    else:
        lut = self._lut.copy()  # Don't let alpha modify original _lut.

    if alpha is not None:
        alpha = min(alpha, 1.0)  # alpha must be between 0 and 1
        alpha = max(alpha, 0.0)
        if bytes:
            alpha = int(alpha * 255)
        if (lut[-1] == 0).all():
            lut[:-1, -1] = alpha
            # All zeros is taken as a flag for the default bad
            # color, which is no color--fully transparent.  We
            # don't want to override this.
        else:
            lut[:, -1] = alpha
            # If the bad value is set to have a color, then we
            # override its alpha just as for any other value.

    rgba = np.empty(shape=xa.shape + (4,), dtype=lut.dtype)
    lut.take(xa, axis=0, mode='clip', out=rgba)
    if vtype == 'scalar':
        rgba = tuple(rgba[0, :])
    if len(rgba.shape) == 3:
        for i in range(rgba.shape[0]):
            for j in range(rgba.shape[1]):
                if np.allclose(rgba[i,j], [0, 0, 0.5, 1]):
                    rgba[i,j] = [0, 0, 0, 1]
    return rgba
Colormap.__call__ = _newcall_
