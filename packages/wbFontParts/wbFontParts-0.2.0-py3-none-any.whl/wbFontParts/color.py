"""
color
===============================================================================
"""
from enum import Enum
from typing import Union

import wx
from defcon.objects.color import _stringToSequence
from wx.lib.colourdb import getColourInfoList, updateColourDB

updateColourDB()


class Color(tuple):
    """
    A color object.
    """
    def __new__(cls, *value):
        if isinstance(value[0], tuple):
            value = value[0]
        # convert from string
        elif isinstance(value[0], str):
            value = _stringToSequence(value[0])
        # convert from wx.Colour
        elif isinstance(value[0], wx.Colour):
            value = tuple(c / 255 for c in value[0])
        # validate the values
        r, g, b, a = value
        _color = (("r", r), ("g", g), ("b", b), ("a", a))
        for component, v in _color:
            if v < 0 or v > 1:
                raise ValueError(
                    "The color for %s (%s) is not between 0 and 1."
                    % (component, str(v))
                )
        # call the super
        value = tuple(round(c, 5) for c in value)
        return super().__new__(cls, value)

    def __eq__(self, other):
        try:
            return super().__eq__(self.__class__(other))
        except ValueError:
            return False
        except TypeError:
            return False

    @property
    def r(self) -> Union[int, float]:
        "The color's red component."
        return self[0]

    @property
    def g(self) -> Union[int, float]:
        "The color's green component."
        return self[1]

    @property
    def b(self) -> Union[int, float]:
        "The color's blue component."
        return self[2]

    @property
    def a(self) -> Union[int, float]:
        "The color's alpha component."
        return self[3]

mark = Enum(
    "mark",
    (
        (name, Color(tuple((r / 255, g / 255, b / 255, 1))))
        for name, r, g, b in getColourInfoList()
        if " " not in name and name[-1] not in "01234567899"
    ),
    module=__name__,
    type=Color,
)
