"""
font
===============================================================================
"""
import logging
import os
from tempfile import TemporaryDirectory
from typing import Iterator, List, Tuple

import wx
from compreffor.cxxCompressor import compreff
from fontParts import fontshell
from fontParts.base import BaseFont, normalizers
from fontParts.base.deprecated import DeprecatedFont, RemovedFont
from fontTools.ttLib import TTFont
from fontTools.ufoLib import UFOFileStructure
from glyphsLib import to_glyphs
from psautohint.autohint import ACOptions, hintFiles
from ufo2ft import CFFOptimization, compileOTF
from wbDefcon import Font
from wbDefcon.tools.conversion import UFO3_guides_to_robofont, UFO3_mark_to_robofont

from .features import RFeatures
from .glyph import RGlyph
from .groups import RGroups
from .guideline import RGuideline
from .info import RInfo
from .kerning import RKerning
from .layer import RLayer
from .lib import RLib

BaseFont.__bases__ = tuple(
    b for b in BaseFont.__bases__ if b not in (DeprecatedFont, RemovedFont)
)

log = logging.getLogger(__name__)


class RFont(fontshell.RFont):
    wrapClass = Font
    infoClass = RInfo
    groupsClass = RGroups
    kerningClass = RKerning
    featuresClass = RFeatures
    libClass = RLib
    layerClass = RLayer
    guidelineClass = RGuideline

    # typing stuff
    _wrapped: Font
    path: str
    info: RInfo
    groups: RGroups
    kerning: RKerning
    features: RFeatures
    lib: RLib
    layers: Tuple[RLayer]
    layerOrder: List[str]
    defaultLayerName: str
    defaultLayer: RLayer
    glyphOrder: List[str]
    guidelines: Tuple[RGuideline]

    def _init(self, pathOrObject=None, showInterface=True, **kwargs):
        if pathOrObject is None:
            font = self.wrapClass()
        elif isinstance(pathOrObject, str):
            font = self.wrapClass(pathOrObject)
        elif hasattr(pathOrObject, "__fspath__"):
            font = self.wrapClass(os.fspath(pathOrObject))
        else:
            assert isinstance(pathOrObject, Font)
            font = pathOrObject
        self._wrapped: Font = font

    def naked(self) -> Font:
        return self._wrapped

    def __iter__(self) -> Iterator[RGlyph]:
        for name in self._wrapped.keys():
            yield self[name]

    def _reprContents(self):
        contents = ["'%s %s'" % (self.info.familyName, self.info.styleName)]
        if self.path is not None:
            if len(self.path) > 60:
                contents.append("path=%s ... %s" % (self.path[:29], self.path[-29:]))
            else:
                contents.append(f"path='{self.path}'")
        return contents

    # def _iter(self):
    #     glyphNames = self.keys()
    #     if (
    #         self._wrapped.document
    #         and self._wrapped.document.fontView
    #         and self._wrapped.document.fontView.frame.glyphGridPanel
    #     ):
    #         glyphNames = self._wrapped.document.fontView.frame.glyphGridPanel.glyphNames
    #     for name in glyphNames:
    #         yield self[name]

    @staticmethod
    def generateFormatToExtension(format, fallbackFormat):
        """
        +--------------+--------------------------------------------------------------------+
        | otfcff       | PS OpenType (CFF-based) font (OTF)                                 |
        +--------------+--------------------------------------------------------------------+
        | otfttf       | PC TrueType/TT OpenType font (TTF)                                 |
        +--------------+--------------------------------------------------------------------+
        | ufo1         | UFO format version 1                                               |
        +--------------+--------------------------------------------------------------------+
        | ufo2         | UFO format version 2                                               |
        +--------------+--------------------------------------------------------------------+
        | ufo3         | UFO format version 3                                               |
        +--------------+--------------------------------------------------------------------+
        | glyphs       | Glyphs App source file                                             |
        +--------------+--------------------------------------------------------------------+
        | vfb          | FontLab 5 source file                                              |
        +--------------+--------------------------------------------------------------------+
        """
        formatToExtension = dict(
            otfcff=".otf",
            otfttf=".ttf",
            ufo1=".ufo",
            ufo2=".ufo",
            ufo3=".ufo",
            glyphs=".glyphs",
            vfb=".vfb",
        )
        return formatToExtension.get(format, fallbackFormat)

    @staticmethod
    def _isValidGenerateEnvironmentOption(name):
        if name in (
            "autohint",
            "cffcompress",
            "removeOverlaps",
            "structure",
            "featureWriters",
            "minimize_ufo_diffs",
        ):
            return True
        return False

    def _generate(self, format, path, environmentOptions, **kwargs):
        if format == "ufo2":
            font = self.copy().naked()
            assert isinstance(font, Font)
            font.save(
                path=path,
                formatVersion=2,
                progressBar=None,
                structure=environmentOptions.get("structure", UFOFileStructure.PACKAGE),
            )
        elif format == "ufo3":
            font = self.copy().naked()
            assert isinstance(font, Font)
            font.save(
                path=path,
                formatVersion=3,
                progressBar=None,
                structure=environmentOptions.get("structure", UFOFileStructure.PACKAGE),
            )
        elif format == "otfcff":
            autohint = bool(environmentOptions.get("autohint", False))
            cffcompress = bool(environmentOptions.get("cffcompress", False))
            removeOverlaps = bool(environmentOptions.get("removeOverlaps", False))
            featureWriters = environmentOptions.get("featureWriters", [])
            otcff_Font: TTFont = compileOTF(
                self.naked(),
                featureWriters=featureWriters,
                useProductionNames=False,
                optimizeCFF=CFFOptimization.NONE,
                removeOverlaps=removeOverlaps,
                # layerName='com.adobe.type.processedglyphs',
            )
            if autohint:
                otcff_Font.save(path)
                otcff_Font.close()
                options = ACOptions()
                options.inputPaths = [path]
                options.outputPaths = [path]
                options.allowChanges = True
                options.hintAll = True
                hintFiles(options)
                otcff_Font = TTFont(path, lazy=False)
            if cffcompress:
                compreff(otcff_Font)
            otcff_Font.save(path)
            otcff_Font.close()
        elif format == "glyphs":
            font = self.naked()
            minimize_diffs = bool(environmentOptions.get("minimize_ufo_diffs", True))
            glyphsFont = to_glyphs([font], minimize_ufo_diffs=minimize_diffs)
            glyphsFont.save(path)
        elif format == "vfb":
            font = self.copy().naked()
            assert isinstance(font, Font)
            UFO3_guides_to_robofont(font)
            UFO3_mark_to_robofont(font)
            with TemporaryDirectory() as tempFolder:
                tempPath = os.path.join(tempFolder, "__temp_font__.ufo")
                font.save(
                    path=tempPath,
                    formatVersion=2,
                    progressBar=None,
                    structure=UFOFileStructure.PACKAGE,
                )
                if os.path.isdir(tempPath):
                    command = f'vfb2ufo -s -fo "{tempPath}" "{path}"'
                    process = wx.Process(wx.GetApp().TopWindow)
                    process.Redirect()
                    pid = wx.Execute(command, wx.EXEC_SYNC, process)
                    stream = process.GetInputStream()
                    if stream.CanRead():
                        data = stream.read()
                        text = "".join(chr(i) for i in data)
                        print(text)
                    process.Destroy()
                    process = None
                else:
                    log.error("Unable to write temp UFO as Format 2 PACKAGE")

        else:
            log.error("Unsupported format %s, can not generate xxx", format)

    def newGlyph(self, name, clear=True):
        """
        Make a new glyph with **name** in the default layer. ::

            >>> glyph = font.newGlyph("A")

        The newly created :class:`BaseGlyph` will be returned.

        If the glyph exists in the layer and clear is set to ``False``,
        the existing glyph will be returned, otherwise the default
        behavior is to clear the exisiting glyph.
        """
        name = normalizers.normalizeGlyphName(name)
        if name not in self or clear:
            glyph = self._newGlyph(name, clear=clear)
        else:
            glyph = self._getItem(name)
        self._setLayerInGlyph(glyph)
        return glyph

    def _newGlyph(self, name, **kwargs):
        layer = self.defaultLayer
        return layer.newGlyph(name, clear=kwargs.get("clear", False))

    # -----------
    # Workbench stuff
    # -----------

    @property
    def selection(self):
        """Selected glyphs in the font"""
        for glyph in self:
            if glyph.selected:
                yield glyph

    def _get_selectedGlyphs(self):
        return self.defaultLayer._get_selectedGlyphs()

    def _get_selectedGlyphNames(self):
        return self.defaultLayer.selectedGlyphNames
