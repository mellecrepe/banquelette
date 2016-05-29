#-*- coding: utf-8 -*-
from account.forms import AccountForm
from account.models import Account
from account.data import auto_subcategory,auto_description
from account import settings
import datetime
import re
import StringIO

import categories
import categories.utils


# =============================================================================
def import_data(data, bank):
    if bank == u'Boursorama':
        import_boursorama(data)
    elif bank == u'Oney':
        import_oney(data)
    elif bank == u'ING Direct':
        import_ingdirect(data)
    elif bank == u'Banque Populaire':
        import_banquepopulaire(data)

# =============================================================================
def change_description(description):
    """ Renommage du champs description """
    for old_d, new_d in auto_description.items():
        if old_d in description:
            description = new_d 
    return description

# =============================================================================
def change_subcategory(subcategory, description):
    """ Automatisation du choix des sous categorie """
    for d, c in auto_subcategory.items():
        if d in description:
            subcategory = c 
    return subcategory

# =============================================================================
def halve_or_not(bank, description):
    if bank == u'Boursorama':
        settings_halve = settings.bs_halve
        settings_except = settings.bs_except

    elif bank == u'Oney':
        settings_halve = settings.oney_halve
        settings_except = settings.oney_except

    elif bank == u'ING Direct':
        try:
            settings_halve  = settings.ingdirect_halve
        except AttributeError:
            # Not defined? Use default value.
            settings_halve  = False

        try:
            settings_except = settings.ingdirect_except
        except AttributeError:
            # Not defined? Use default value.
            settings_except = []
            
    elif bank == u'Banque Populaire':
        try:
            settings_halve  = settings.banquepopulaire_halve
        except AttributeError:
            # Not defined? Use default value.
            settings_halve  = False

        try:
            settings_except = settings.banquepopulaire_except
        except AttributeError:
            # Not defined? Use default value.
            settings_except = []

    if settings_halve is True:
        halve = True
        for d in settings_except:
            if d in description:
                halve = False
    else:
        halve = False
    return halve


# =============================================================================
def import_boursorama(data):
    """ Parsing des données pour Boursorama """
    # mise en forme pour obtenir une liste sans tabulation, espace superflux, ...
    # et ou chaque element de la liste est une depense

    # Une entré boursorama :
    # 23/03/2015	PAIEMENT CARTE 190315 GB TOUCHNOTE LIMIT	
    #  Non catégorisé
    # 9,95 €	
    # ou
    # 01/09/2015	01/09/2015
    # VIR SEPA Safar agence	
    #  Virements emis
    # - 1 135,76 €
    # On obtient une liste avec chaque entree sur 3 ou 4 lignes
    data = data.split(u" \u20ac")
    data = [ re.sub(ur"^\t\r\n", u"", d) for d in data ]

    for entry in data:
        e = entry.split(u"\r\n")

        if len(e) != 3 and len(e) != 4 :
            continue

        s = e[0]
        # suppression des \t et des espaces en fin de lignes
        s = re.sub(ur"\t", u" ", s)
        s = re.sub(ur" $", u"", s)

        # element a ne pas prendre en compte
        re_detail = re.compile(ur"Dépenses carte .* de détails\)")
        re_releve = re.compile(ur"Relevé différé Carte")

        if re.search(re_detail, e[1]) or re.search(re_releve, e[1]):
            continue

        # analyse de la premiere ligne
        # 3 formats possibles :
        # format_retrait/virement :[u'01/09/2015\t01/09/2015', u'VIR SEPA Safar agence\t', u' Virements emis', u'- 1 135,76 \u20ac ']
        # format_CB : [u'26/08/2015\tPAIEMENT CARTE 250815 75 MONOPRIX\t', u' Alimentation', u'33,68']
        # format_avoir : [u'13/08/2015\tAVOIR 120815 75 MONOPRIX\t', u' Remboursements frais de v...', u'-3,09']

        # format_retrait/virement 
        re_vir = re.compile(ur"[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}/[0-9]{2}/[0-9]{4}")
        # format Paiement / Avoir
        re_cb = re.compile(ur"[0-9]{2}/[0-9]{2}/[0-9]{4} ")


        # format_retrait/virement 
        if re.match(re_vir, s) and (len(e) == 4) :

            # on recupere la 1e date
            date = datetime.datetime.strptime(s[:10], "%d/%m/%Y").date()
            description = e[1].replace(u'VIR SEPA ', u'Virement ')
            # on recupere la depense
            expense = float(e[3].replace(u' ',u'').replace(u',',u'.'))

        # format Paiement / Avoir
        elif re.match(re_cb, s) and len(e) == 3:
            # format paiement
            re_pai = re.compile(ur"[0-9]{2}/[0-9]{2}/[0-9]{4} PAIEMENT CARTE ")
            if re.match(re_pai, s):
                # on supprime le debut de ligne jusqu'a la vrai date DDMMYY
                s = re.sub(re_pai, u"", s)

            # format avoir
            re_av = re.compile(ur"[0-9]{2}/[0-9]{2}/[0-9]{4} AVOIR ")
            if re.match(re_av, s):
                # on supprime le debut de ligne jusqu'a la vrai date DDMMYY
                s = re.sub(re_av, u"", s)

            # on recupere la date et on la supprime de la string   
            date = datetime.datetime.strptime(s[:6], "%d%m%y").date()
            s = s.replace(s[:6] + u" ", u"")
            # on recupere la description
            description = s.replace(u'75 ', u'')
            # on recupere la depense
            expense = - float(e[2].replace(u' ',u'').replace(u',',u'.'))

        # format inconnu
        else:
            continue

        # element recupéré pour chacun des format
        # modification description
        description = change_description(description)

        # definition de subcategory
        subcategory = categories.utils.autoset_category(description)

        # halve or not
        halve = halve_or_not(u'Boursorama', description)
        if halve is True:
            expense = expense/2
                    
        account = Account(date = date, description = description, expense = expense, \
              category = subcategory, bank = u'Boursorama', check = False, halve = halve)  
        account.save()
        

# =============================================================================
def import_oney(data):
    """ Parsing des données pour Oney """
    form_list = []
    # creation liste avec une ligne une dépense
    list_data = data.split('\n')
    for e in list_data:
        # une liste de chacun ligne est faite
        e_list = e.split('\t')

        # format_ex :
        # [ u'26/02/2015',
        #   u'PAYPAL - 0800 942 890 - traite le 27/02',
        #   u' ',
        #   u'45,80',
        #   u' \r' ] 

        if len(e_list) < 4: # si e_list a moins de 4 éléments dernier élément
            continue
        description = e_list[1]
        if u"Solde initial" in description :
            continue
        if u"Prélèvement mensualité" in description :
            continue
        if u"Intérêts" in description :
            continue

        # on definit chaque valeur d'un objet Account
	# on définit la date comme un objet datetime
        date = datetime.datetime.strptime(e_list[0], "%d/%m/%Y").date()
	# l'id = la date + la depense ex: 201502264580

        # description
        description = re.sub(ur" - traité le .*$", "", description)
        description = re.sub(ur" - [0-9 ]*PARIS[0-9 ]*$", "", description)
        # modification description
        description = change_description(description)

        # definition de subcategory
        subcategory = categories.utils.autoset_category(description)

        # expense : on récupère la dépense positive ou négtive
        if e_list[2] == u' ':
            expense = float(u'-' + e_list[3].replace(u',',u'.'))
        elif e_list[3] == ' ':
            expense = float(e_list[2].replace(u',',u'.'))

        # halve or not
        halve = halve_or_not(u'Oney', description)
        if halve is True:
            expense = expense/2
                    
        account = Account(
                date        = date,
                description = description,
                expense     = expense,
                category    = subcategory,
                bank        = u'Oney',
                check       = False,
                halve       = halve
                )
        account.save()


# =============================================================================
def import_ingdirect(data):
    """ Parsing des données pour ING Direct.

        ING Direct propose de télécharger ses données bancaires dans plusieurs
        formats différents : xls, csv ou qif. Pour le parsing, on se base sur
        le format csv.

        Exemples d'entrées CSV d'un relevé ING Direct :

         09/12/2015;CARTE 05/12/2015 LE RUBAN BLEU;;-17,50;EUR;
         25/11/2015;VIREMENT SEPA RECU RPC ESPIONNAGE;;10000;EUR;

        soit, dans l'ordre, les champs suivants :

        * DATE DE PRISE EN COMPTE (au format JJ/MM/AAAA) ;
        * TYPE DE TRANSACTION (et date pour un paiement par carte) ET INFOS ;
        * ??? ;
        * MONTANT (positif ou négatif);
        * DEVISE ;
    """

    # data contient toutes les données collées depuis le CSV. On va donc les
    # traiter ligne par ligne. Pour cela on utilise StringIO.
    buf = StringIO.StringIO(data)

    # Start by reading the first line and loop
    line = buf.readline()
    while line != u"":

        # We parse the line here !
        csvline = line.split(';')

        raw_date        = csvline[0]
        raw_description = csvline[1]
        raw_expense     = csvline[3]
        raw_currency    = csvline[4]

        # 1 - the date
        # Nothing to do but assume DD/MM/YYYY conventions here.
        date = datetime.datetime.strptime(raw_date, "%d/%m/%Y").date()

        # 2 - the expense
        # First, try to convert directly. If that fails, that's probably
        # because of the coma used as decimal point. Vive la France \o/.
        try:
            expense = float(raw_expense)
        except ValueError:
            expense = float(raw_expense.replace(',', '.'))

        # 3 - the currency
        # For now we suppose it is always in €, and raise an exception
        # otherwise. TODO But maybe we could do better?
        if raw_currency != u"EUR":
            raise ValueError(u"Currency is not EUR in transaction: %s" % line)

        # 4 - the description
        # Last but not least.
        # Modifications automatiques de la description et de la subcategory
        description = change_description(raw_description)
        subcategory = categories.utils.autoset_category(description)

        # halve or not
        halve = halve_or_not(u'ING Direct', description)
        if halve is True:
            expense = expense/2

        # Save the transaction in database
        account = Account( date        = date,
                           description = description,
                           expense     = expense,
                           category    = subcategory,
                           bank        = u'ING Direct',
                           check       = False,
                           halve       = halve )
        account.save()


        # Read next line
        line = buf.readline()
        
def import_banquepopulaire(data):
    """ Parsing des données Banque Populaire au format CSV

        Le format du fichier CSV proposé par la Banque Populaire est le suivant:
        
        Le séparateur par défaut est ';' (point virgule)
        Les champs disponibles sont:
          - N° du compte
          - Date de comptabilisation (au format JJ/MM/AAAA)
          - Date de l'opération (au format JJ/MM/AAAA)
          - Libellé
          - Référence
          - Date valeur (au format JJ/MM/AAAA)
          - Montant
    """
    
    # Traitement par lignes des données
    for line in StringIO.StringIO(data):

	# Découpage des champs CSV
        csvdata = line.split(';')
        if len(csvdata) < 7:
            continue
            
        # On ignore la ligne d'en-tête du CSV (si il y en a une)
        if csvdata[0].isdigit() == False:
            continue
        
        # Date de l'opération
        date = datetime.datetime.strptime(csvdata[2], "%d/%m/%Y").date()
        
        # Montant de l'opération
        try:
            expense = float(csvdata[6])
        except ValueError:
            expense = float(csvdata[6].replace(u',', u'.'))
        
        # Description de l'opération et catégorisation
        description = csvdata[3]
        subcategory = settings.subcategory_default

        # Modifications automatiques de la description et de la subcategory
        description = change_description(description)
        subcategory = change_subcategory(subcategory, description)

        # halve or not
        halve = halve_or_not(u'Banque Populaire', description)
        if halve is True:
            expense = expense/2
            
        account = Account( date        = date,
                           description = description,
                           expense     = expense,
                           category    = subcategory,
                           bank        = u'Banque Populaire',
                           check       = False,
                           halve       = halve )
        account.save()
