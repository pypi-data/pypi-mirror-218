"""
pPoint
===============================================================================
"""

from fontParts import fontshell
from fontParts.base import BaseBPoint
from fontParts.base.deprecated import DeprecatedBPoint, RemovedBPoint

BaseBPoint.__bases__ = tuple(
    b for b in BaseBPoint.__bases__ if b not in (DeprecatedBPoint, RemovedBPoint)
)


class RBPoint(fontshell.RBPoint):
    def _get_selected(self):
        return self.naked().selected

    def _set_selected(self, value):
        self.naked().selected = value
