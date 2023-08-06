"""
features
===============================================================================
"""

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseFeatures
from fontParts.base.deprecated import DeprecatedFeatures, RemovedFeatures

BaseFeatures.__bases__ = tuple(
    b for b in BaseFeatures.__bases__ if b not in (DeprecatedFeatures, RemovedFeatures)
)

class RFeatures(fontshell.RFeatures):
    wrapClass = wbDefcon.Features

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped:wbDefcon.Features = wrap

    def naked(self) -> wbDefcon.Features:
        return self._wrapped
