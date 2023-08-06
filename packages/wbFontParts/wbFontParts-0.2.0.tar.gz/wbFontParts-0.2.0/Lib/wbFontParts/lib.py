"""
lib
===============================================================================
"""

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseLib
from fontParts.base.deprecated import DeprecatedLib, RemovedLib

BaseLib.__bases__ = tuple(
    b for b in BaseLib.__bases__ if b not in (DeprecatedLib, RemovedLib)
)

class RLib(fontshell.RLib):
    wrapClass = wbDefcon.Lib

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped:wbDefcon.Lib = wrap

    def naked(self) -> wbDefcon.Lib:
        return self._wrapped
