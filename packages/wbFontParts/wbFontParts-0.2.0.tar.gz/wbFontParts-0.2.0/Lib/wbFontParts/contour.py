"""
contour
===============================================================================
"""
import wbDefcon
from fontParts import fontshell
from fontParts.base import BaseContour
from fontParts.base.compatibility import (
    ContourCompatibilityReporter as ContourCompatibilityReporterBase,
)
from fontParts.base.deprecated import DeprecatedContour, RemovedContour
from fontTools.pens.basePen import BasePen

from .bPoint import RBPoint
from .point import RPoint
from .segment import RSegment

BaseContour.__bases__ = tuple(
    b for b in BaseContour.__bases__ if b not in (DeprecatedContour, RemovedContour)
)


class ContourCompatibilityReporter(ContourCompatibilityReporterBase):
    def __init__(self, contour1, contour2):
        super().__init__(contour1, contour2)
        self.startPointDifference = False

    def report(self, showOK=True, showWarnings=True):
        report_text = super().report(showOK, showWarnings)
        if self.startPointDifference and showWarnings:
            report_text += "\n" + self.formatFatalString(
                "Start points may be different"
            )
        elif showOK:
            report_text += "\n" + self.formatOKString(
                "Start points seem to be consistent"
            )
        return report_text


class SegmentStructurePen(BasePen):
    """
    Calculate structure as sequece of relative segment position.
    Is used to detect inconsistent start points.
    """

    def __init__(self, glyphSet=None):
        super().__init__(glyphSet)
        self.structure = []

    @property
    def previousPoint(self):
        return self._getCurrentPoint()

    def _moveTo(self, pt):
        pass

    def _lineTo(self, pt):
        if not self.previousPoint:
            return
        self.structure.append(self.getDirection(pt))

    def _curveToOne(self, pt1, pt2, pt3):
        if not self.previousPoint:
            return
        self.structure.append(self.getDirection(pt3))

    def getDirection(self, pt):
        direction = set()
        previousPoint = self.previousPoint
        if pt[0] >= previousPoint[0]:
            direction.add("right")
        elif pt[0] <= previousPoint[0]:
            direction.add("left")
        if pt[1] >= previousPoint[1]:
            direction.add("up")
        elif pt[1] <= previousPoint[1]:
            direction.add("down")
        return direction


class RContour(fontshell.RContour):
    wrapClass = wbDefcon.Contour
    pointClass = RPoint
    segmentClass = RSegment
    bPointClass = RBPoint

    def _init(self, wrap=None):
        if wrap is None:
            wrap = self.wrapClass()
        self._wrapped: wbDefcon.Contour = wrap

    def naked(self) -> wbDefcon.Contour:
        return self._wrapped

    def _get_selected(self) -> bool:
        return self._wrapped.selected

    def _set_selected(self, value: bool):
        self._wrapped.selected = value

    def _transformBy(self, matrix, **kwargs):
        self._wrapped.holdNotifications()
        super()._transformBy(matrix, **kwargs)
        self._wrapped.releaseHeldNotifications()
        # self._wrapped.postNotification(notification="Glyph.ContoursChanged")

    # -------------
    # Interpolation
    # -------------

    compatibilityReporterClass = ContourCompatibilityReporter

    def _isCompatible(self, other, reporter):
        """
        Detect inconsistent start points in addition to
        super class implementation.
        """
        super()._isCompatible(other, reporter)
        if (
            not reporter.openDifference
            and not reporter.directionDifference
            and not reporter.segmentCountDifference
        ):
            contour1 = self
            contour2 = other
            structPen1 = SegmentStructurePen()
            contour1.draw(structPen1)
            structPen2 = SegmentStructurePen()
            contour2.draw(structPen2)
            structList = []
            for i, direction in enumerate(structPen1.structure):
                structList.append(bool(direction & structPen2.structure[i]))
            if not all(structList):
                reporter.startPointDifference = True
                reporter.fatal = True
