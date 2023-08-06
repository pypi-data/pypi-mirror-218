"""
kerning
===============================================================================
"""

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseKerning
from fontParts.base.deprecated import DeprecatedKerning, RemovedKerning

BaseKerning.__bases__ = tuple(
    b for b in BaseKerning.__bases__ if b not in (DeprecatedKerning, RemovedKerning)
)

class RKerning(fontshell.RKerning):
    wrapClass = wbDefcon.Kerning

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped:wbDefcon.Kerning = wrap

    def naked(self) -> wbDefcon.Kerning:
        return self._wrapped
