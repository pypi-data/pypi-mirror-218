"""
inspect
===============================================================================

Inspect feature files.

"""
from __future__ import annotations

import logging

import fontTools.feaLib.ast as ast

log = logging.getLogger(__name__)


def hasFeature(featureSyntaxTree: ast.FeatureFile, featureTag: str) -> bool:
    for statement in featureSyntaxTree.statements:
        if isinstance(statement, ast.FeatureBlock) and statement.name == featureTag:
            return True
    return False
