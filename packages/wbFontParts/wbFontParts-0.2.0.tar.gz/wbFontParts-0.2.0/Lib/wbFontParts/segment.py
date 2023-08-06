"""
segment
===============================================================================
"""

from fontParts import fontshell
from fontParts.base import BaseSegment
from fontParts.base.deprecated import DeprecatedSegment, RemovedSegment

BaseSegment.__bases__ = tuple(
    b for b in BaseSegment.__bases__ if b not in (DeprecatedSegment, RemovedSegment)
)

class RSegment(fontshell.RSegment):
    # -------------
    # Selected Flag
    # -------------
    def _get_selected(self):
        return all(p.selected for p in self.points)
