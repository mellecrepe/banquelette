#!/usr/bin/env python
#-*- coding: utf-8 -*-

from category import Category, SeparatorUsedInCategoryNameError

import yamlload

import sys
import pprint

# CONSTANTS
# =============================================================================

# The name of the TAML file containing all informations about the user-defined
# categories.
YAMLFILE = u"account/categories.yaml"

# FUNCTIONS
# =============================================================================
def load_categories(
        data,
        categories_dict=None,
        parent=None ):
    """Recursive function
    Charge les catégories depuis un dictionnaire (comme celui parsé depuis le
    fichier YAML).
    Retourne un dictionnaire des catégories que l'on peut utiliser."""


    if categories_dict is None:
        categories_dict = {}

    # À ce stade, les données yaml sont généralement un dict de la forme :
    # { "catégorie" : [ "sous-catégorie", "souscatégories", ... ] ... }

    for category in data:

        # Treat metadata entries
        if category.startswith(Category.MDKW_STARTCHAR):
            if parent is not None:
                # TODO add checks for data[category] type ?
                # Add to the metadata (without the first char)
                parent.metadata[category[1:]] = data[category]

            continue

        # Check for a malformed category name
        if Category.SEPARATOR in unicode(category):
            raise SeparatorUsedInCategoryNameError(category)

        # Create category !
        cat = Category(name=category, parent=parent)
        categories_dict[ unicode(cat) ] = cat

        # Decide what to do next depending on category type
        if   type(data[category]) is type(dict()):

            # Recursion !
            load_categories( data            = data[category],
                             categories_dict = categories_dict,
                             parent          = cat )

        elif type(data[category]) is type(list()):

            for subcategory in data[category]:
                subcat = Category(name=subcategory, parent=cat)
                categories_dict[ unicode(subcat) ] = subcat

        elif type(data[category]) is type(str()):

            subcat = Category( name=data[category], parent=cat )
            categories_dict[ unicode(subcat) ] = subcat

        elif type(data[category]) is type(None):
            pass

    # If there's nothing more to iterate on, we parsed the data !
    return categories_dict


# VARIABLES
# =============================================================================

try:
    CATEGORIES = load_categories( yamlload.load_yaml(YAMLFILE) )
except:
    CATEGORIES = load_categories( yamlload.load_yaml(sys.argv[1]) )

try:
    DEFAULT_CATEGORY = [ c for c in CATEGORIES
            if CATEGORIES[c].is_default()
            ][0]
except:
    DEFAULT_CATEGORY = None

FIRST_LEVEL_CATEGORIES = { c:v  for c,v in CATEGORIES.items()
                                if CATEGORIES[c].parent is None }


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



if __name__ == '__main__':
    pprint.pprint(CATEGORIES)
    pprint.pprint("default: %s" % DEFAULT_CATEGORY)

    for c in FIRST_LEVEL_CATEGORIES:
        print(c)
        pprint.pprint(FIRST_LEVEL_CATEGORIES[c].metadata)
