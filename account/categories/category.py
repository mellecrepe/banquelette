#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# =============================================================================
class Category():
    """Une étiquette permettant de classer une dépense"""

    SEPARATOR = '/'

    MDKW_STARTCHAR = '_'
    MDKW_PATTERN   = 'pattern'
    MDKW_DEFAULT   = 'default'
    MDKW_COLORS    = 'colors'

    # -------------------------------------------------------------------------
    def __init__(self, name, parent=None, metadata=None):
        """Définir une catégorie parente permet de définir une
        sous-catégorie."""

        self.parent = parent

        self.name = name

        if metadata is None:
            self.metadata = {}
        else:
            self.metadata = metadata



    # -------------------------------------------------------------------------
    def matches_string(self, string):

        try:
            lowstring = string.lower()

            for p in self.metadata[Category.MDKW_PATTERN]:

                if p.lower() in lowstring:
                    return True

        except KeyError:
            pass

        return False


    # -------------------------------------------------------------------------
    def is_default(self):

        try:
            return self.metadata[Category.MDKW_DEFAULT]
        except KeyError:
            return False


    # -------------------------------------------------------------------------
    def __str__(self):
        rv = '' 

        if self.parent is not None:
            rv = str(self.parent)
            rv += Category.SEPARATOR

        rv += str(self.name)

        return rv

# =============================================================================
class SeparatorUsedInCategoryNameError(Exception):
    """A custom exception to alert that the Category.SEPARATOR was used in a
    Category name."""

    # -------------------------------------------------------------------------
    def __init__(self, category_name):
        Exception.__init__( self,
                            "The Category name %s contains the Category " \
                            "separator character '%s'"                    \
                            % ( category_name, Category.SEPARATOR ) )
