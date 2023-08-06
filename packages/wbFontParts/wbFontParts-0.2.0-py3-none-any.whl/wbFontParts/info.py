"""
info
===============================================================================
"""

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseInfo
from fontParts.base.deprecated import DeprecatedInfo, RemovedInfo

BaseInfo.__bases__ = tuple(
    b for b in BaseInfo.__bases__ if b not in (DeprecatedInfo, RemovedInfo)
)


class RInfo(fontshell.RInfo):
    wrapClass = wbDefcon.Info

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped: wbDefcon.Info = wrap

    def naked(self) -> wbDefcon.Info:
        return self._wrapped
