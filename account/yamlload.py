#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import yaml
import pprint

from category import Category

def load_yaml(filename):
    """Parse et charge Un fichier de config YAML."""

    with open(filename, 'r') as f:
        data = yaml.load( f.read() )

    return data
 

def load_categories(data, categories_dict={}, parent=None):
    """Recursive function
    Charge les catgégories depuis un dictionnaire (comme celui parsé depuis le
    fichier YAML).
    Retourne un dictionnaire des catégories que l'on peut utiliser."""

    # À ce stade, les données yaml sont généralement un dict de la forme :
    # { "catégorie" : [ "sous-catégorie", "souscatégories", ... ] ... }

    for category in data:

        if Category.SEPARATOR in unicode(category):
            raise SeparatorUsedInCategoryNameError(category)

        cat = Category(name=category, parent=parent)
        categories_dict[ unicode(cat) ] = cat

        if   type(data[category]) is type(dict()):

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

    return categories_dict

if __name__ == '__main__':
    pprint.pprint( load_categories( load_yaml( sys.argv[1] ) ) )
