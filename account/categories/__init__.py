#!/usr/bin/env python
#-*- coding: utf-8 -*-

import settings
import yamlloader

import loader

# VARIABLES
# =============================================================================
try:
    CATEGORIES = loader.load_categories(
            yamlloader.load_yaml(settings.YAMLFILE)
            )
except:
    CATEGORIES = loader.load_categories( yamlloader.load_yaml(sys.argv[1]) )

# =============================================================================
try:
    DEFAULT_CATEGORY = [ c for c in CATEGORIES
            if CATEGORIES[c].is_default()
            ][0]
except:
    DEFAULT_CATEGORY = None

# =============================================================================
FIRST_LEVEL_CATEGORIES = { c:v  for c,v in CATEGORIES.items()
                                if CATEGORIES[c].parent is None }


