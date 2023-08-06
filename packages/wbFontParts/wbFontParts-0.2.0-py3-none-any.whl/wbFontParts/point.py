"""
point
===============================================================================
"""

import wbDefcon
from fontParts import fontshell
from fontParts.base import BasePoint
from fontParts.base.deprecated import DeprecatedPoint, RemovedPoint

BasePoint.__bases__ = tuple(
    b for b in BasePoint.__bases__ if b not in (DeprecatedPoint, RemovedPoint)
)

class RPoint(fontshell.RPoint):
    wrapClass = wbDefcon.Point

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass((0, 0))
        self._wrapped:wbDefcon.Point = wrap

    def naked(self) -> wbDefcon.Point:
        return self._wrapped

    def _get_selected(self) -> bool:
        return self._wrapped.selected

    def _set_selected(self, value:bool):
        self._wrapped.selected = value
