#!/usr/bin/env python
#-*- coding: utf-8 -*-

from . import CATEGORIES, DEFAULT_CATEGORY

# FUNCTIONS
# =============================================================================
def autoset_category(
        string,
        category_list=CATEGORIES,
        default_category=DEFAULT_CATEGORY
        ):
    """Determine automatically the category matching a given string."""

    for c in CATEGORIES:
        if CATEGORIES[c].matches_string(string):
            return c

    return default_category



