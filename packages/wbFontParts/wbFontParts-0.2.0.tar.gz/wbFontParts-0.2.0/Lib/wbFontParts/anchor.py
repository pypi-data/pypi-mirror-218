"""
anchor
===============================================================================
"""

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseAnchor
from fontParts.base.deprecated import DeprecatedAnchor, RemovedAnchor

BaseAnchor.__bases__ = tuple(
    b for b in BaseAnchor.__bases__ if b not in (DeprecatedAnchor, RemovedAnchor)
)


class RAnchor(fontshell.RAnchor):
    wrapClass = wbDefcon.Anchor

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
            wrap.x = 0
            wrap.y = 0
        self._wrapped:wbDefcon.Anchor = wrap

    def naked(self) -> wbDefcon.Anchor:
        return self._wrapped

    def _get_selected(self) -> bool:
        return self._wrapped.selected

    def _set_selected(self, value:bool):
        self._wrapped.selected = value
