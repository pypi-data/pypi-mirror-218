"""
groups
===============================================================================
"""

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseGroups
from fontParts.base.deprecated import DeprecatedGroups, RemovedGroups

BaseGroups.__bases__ = tuple(
    b for b in BaseGroups.__bases__ if b not in (DeprecatedGroups, RemovedGroups)
)


class RGroups(fontshell.RGroups):
    wrapClass = wbDefcon.Groups

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped: wbDefcon.Groups = wrap

    def naked(self) -> wbDefcon.Groups:
        return self._wrapped
