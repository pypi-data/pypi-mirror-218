"""
image
===============================================================================
"""

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseImage
from fontParts.base.deprecated import DeprecatedImage, RemovedImage

BaseImage.__bases__ = tuple(
    b for b in BaseImage.__bases__ if b not in (DeprecatedImage, RemovedImage)
)


class RImage(fontshell.RImage):
    wrapClass = wbDefcon.Image

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped: wbDefcon.Image = wrap

    def naked(self) -> wbDefcon.Image:
        return self._wrapped
