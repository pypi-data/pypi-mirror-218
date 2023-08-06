from __future__ import annotations

import io
from typing import Sequence, Tuple

import fontTools.feaLib.ast as ast
from fontTools.feaLib.parser import Parser

__version__ = "0.2.2"


def getFeatureSyntaxTree(
    featureText: str, glyphNames: Sequence[str] = ()
) -> ast.FeatureFile:
    """
    Return features from featureText as Abstract Syntax Tree
    """
    featureFile = io.StringIO(featureText)
    parser = Parser(featureFile, glyphNames)
    syntaxTree = parser.parse()
    return syntaxTree
