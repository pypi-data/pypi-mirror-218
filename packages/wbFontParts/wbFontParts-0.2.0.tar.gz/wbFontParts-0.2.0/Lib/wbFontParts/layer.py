"""
layer
===============================================================================
"""
import logging

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseLayer, normalizers
from fontParts.base.deprecated import DeprecatedLayer, RemovedLayer

from .glyph import RGlyph
from .lib import RLib

BaseLayer.__bases__ = tuple(
    b for b in BaseLayer.__bases__ if b not in (DeprecatedLayer, RemovedLayer)
)

log = logging.getLogger(__name__)


class RLayer(fontshell.RLayer):
    wrapClass = wbDefcon.Layer
    libClass = RLib
    glyphClass = RGlyph

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped: wbDefcon.Layer = wrap

    def naked(self) -> wbDefcon.Layer:
        return self._wrapped

    def newGlyph(self, name, clear=True):
        """
        Make a new glyph with **name** in the layer. ::

            >>> glyph = layer.newGlyph("A")

        The newly created :class:`BaseGlyph` will be returned.

        If the glyph exists in the layer and clear is set to ``False``,
        the existing glyph will be returned, otherwise the default
        behavior is to clear the exisiting glyph.
        """
        name = normalizers.normalizeGlyphName(name)
        if name not in self or clear:
            glyph = self._newGlyph(name)
        else:
            glyph = self._getItem(name)
        self._setLayerInGlyph(glyph)
        return glyph

    def _get_selectedGlyphs(self):
        return tuple(self[g] for g in self._wrapped.selectedGlyphNames)

    def _get_selectedGlyphNames(self):
        return self._wrapped.selectedGlyphNames
