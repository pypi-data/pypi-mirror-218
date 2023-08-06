"""
component
===============================================================================
"""

import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseComponent
from fontParts.base.deprecated import DeprecatedComponent, RemovedComponent

BaseComponent.__bases__ = tuple(
    b for b in BaseComponent.__bases__ if b not in (DeprecatedComponent, RemovedComponent)
)

class RComponent(fontshell.RComponent):
    wrapClass = wbDefcon.Component

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped:wbDefcon.Component = wrap

    def naked(self) -> wbDefcon.Component:
        return self._wrapped

    def _get_selected(self) -> bool:
        return self._wrapped.selected

    def _set_selected(self, value:bool):
        self._wrapped.selected = value
