#!/usr/bin/env python
#-*- coding:utf-8 -*-

# =============================================================================
class Category():
    """Une étiquette permettant de classer une dépense"""

    SEPARATOR = u'/'

    MDKW_STARTCHAR = u'_'
    MDKW_PATTERN   = MDKW_STARTCHAR + u'pattern'
    MDKW_DEFAULT   = MDKW_STARTCHAR + u'default'
    MDKW_COLORS    = MDKW_STARTCHAR + u'colors'

    # -------------------------------------------------------------------------
    def __init__(self, name, parent=None):
        """Définir nune catégorie parente permet de définir une
        sous-catégorie."""

        self.parent = parent
        
        self.name = name

        self.metadata = {}


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
        return unicode(self).encode('utf8')


    # -------------------------------------------------------------------------
    def __unicode__(self):

        rv = u'' 

        if self.parent is not None:
            rv = unicode(self.parent)
            rv += Category.SEPARATOR

        rv += unicode(self.name)

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
