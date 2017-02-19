#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import pprint

import account.yamlloader as yamlloader

from account.categories.category import Category, SeparatorUsedInCategoryNameError

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
        if Category.SEPARATOR in category:
            raise SeparatorUsedInCategoryNameError(category)

        # Create category !
        cat = Category(name=category, parent=parent)
        categories_dict[ str(cat) ] = cat

        # Decide what to do next depending on category type
        if   type(data[category]) is type(dict()):

            # Recursion !
            load_categories( data            = data[category],
                             categories_dict = categories_dict,
                             parent          = cat )

        elif type(data[category]) is type(list()):

            for subcategory in data[category]:
                subcat = Category(name=subcategory, parent=cat)
                categories_dict[ str(subcat) ] = subcat

        elif type(data[category]) is type(str()):

            subcat = Category( name=data[category], parent=cat )
            categories_dict[ str(subcat) ] = subcat

        elif type(data[category]) is type(None):
            pass

    # If there's nothing more to iterate on, we parsed the data !
    return categories_dict

if __name__ == '__main__':

    my_categories = load_categories( yamlloader.load_yaml( sys.argv[1] ) )
    pprint.pprint(my_categories)
