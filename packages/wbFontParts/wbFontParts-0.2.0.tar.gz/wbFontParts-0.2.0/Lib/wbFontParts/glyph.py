"""
glyph
===============================================================================
"""

from typing import Optional

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseGlyph
from fontParts.base.deprecated import DeprecatedGlyph, RemovedGlyph
from fontParts.base.normalizers import normalizeColor

from .anchor import RAnchor
from .color import Color
from .component import RComponent
from .contour import RContour
from .guideline import RGuideline
from .image import RImage
from .lib import RLib

BaseGlyph.__bases__ = tuple(
    b for b in BaseGlyph.__bases__ if b not in (RemovedGlyph, DeprecatedGlyph)
)


class RGlyph(fontshell.RGlyph):
    wrapClass = wbDefcon.Glyph
    contourClass = RContour
    componentClass = RComponent
    anchorClass = RAnchor
    guidelineClass = RGuideline
    imageClass = RImage
    libClass = RLib
    colorClass = Color

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped: wbDefcon.Glyph = wrap

    def _get_selected(self) -> bool:
        return self._wrapped.selected

    def _set_selected(self, value: bool):
        self._wrapped.selected = value

    def _transformBy(self, matrix, **kwargs) -> None:
        self._wrapped.holdNotifications()
        super()._transformBy(matrix, **kwargs)
        self._wrapped.releaseHeldNotifications()
        self._wrapped.postNotification(notification="Glyph.ContoursChanged")

    def _moveBy(self, value, **kwargs) -> None:
        self._wrapped.move(value)

    def show(self, newPage=False, view=None) -> None:
        self._wrapped.show(newPage, view)

    def naked(self) -> wbDefcon.Glyph:
        return self._wrapped

    # Mark
    def _get_base_markColor(self) -> Optional[Color]:
        value = self._get_markColor()
        if value is not None:
            value = self.colorClass(normalizeColor(value))
        return value

    def _set_base_markColor(self, value):
        if value is not None:
            value = normalizeColor(self.colorClass(value))
        self._set_markColor(value)
