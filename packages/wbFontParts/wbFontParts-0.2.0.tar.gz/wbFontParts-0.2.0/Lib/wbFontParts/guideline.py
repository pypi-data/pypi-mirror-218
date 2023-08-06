"""
guideline
===============================================================================
"""

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseGuideline
from fontParts.base.deprecated import DeprecatedGuideline, RemovedGuideline

BaseGuideline.__bases__ = tuple(
    b for b in BaseGuideline.__bases__ if b not in (DeprecatedGuideline, RemovedGuideline)
)

class RGuideline(fontshell.RGuideline):
    wrapClass = wbDefcon.Guideline

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped:wbDefcon.Guideline = wrap

    def naked(self) -> wbDefcon.Guideline:
        return self._wrapped

    def _get_selected(self) -> bool:
        return self._wrapped.selected

    def _set_selected(self, value:bool):
        self._wrapped.selected = value
