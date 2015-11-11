from couchdbkit.ext.django.schema import *

class Account(Document):
    date = DateProperty(required=True)
    description = StringProperty(required=True)
    expense = FloatProperty(required=True)
    category = StringProperty()
    subcategory = StringProperty()
    bank = StringProperty()
    check = BooleanProperty()
    halve = BooleanProperty()
    
    def save(self, *args, **kwargs):
        necessaire = ['necessaire','courses', 'transport', 'electricite', 'loyer', 'repas-midi', 'sante', 'impot-taxe', 'assurance', 'telephone-box', 'necessaire-autre']
        achat = ['achat', 'vetement', 'cadeau', 'decoration', 'box', 'beaute', 'achat-divers']
        sortie = ['sortie', 'resto', 'bar', 'gourmandise', 'soiree', 'concert', 'cine', 'theatre', 'expo-musee', 'sport', 'sortie-autre']
        vacances = ['vacances', 'weekend']
        gain = ['gain', 'paye', 'remboursement', 'argent-cadeau', 'gain-autre']
        autre = ['autre', 'retrait', 'nicolas']
        
        for list in [ necessaire, achat, sortie, vacances, gain, autre ]:
            if self.subcategory in list:
                self.category = list[0]
        
        super(Account, self).save(*args, **kwargs)
