#-*- coding: utf-8 -*-
from account.forms import AccountForm
from account.models import Account
from account.data import auto_subcategory,auto_description
from account import settings
import datetime
import re
from io import StringIO

import account.categories
import account.categories.utils


# =============================================================================
def import_data(data, bank):
    if bank == 'Boursorama':
        import_boursorama(data)
    elif bank == 'Oney':
        import_oney(data)
    elif bank == 'ING Direct':
        import_ingdirect(data)
    elif bank == 'Banque Populaire':
        import_banquepopulaire(data)
    elif bank == 'Boobank/Boursorama':
        import_boobank(data,"Boursorama")
    elif bank == 'Boobank/Societe Generale':
        import_boobank(data,"Societe Generale")

# =============================================================================
def change_description(description):
    """ Renommage du champs description """
    for old_d, new_d in auto_description.items():
        if old_d in description:
            description = new_d
    return description


# =============================================================================
def halve_or_not(bank, description):
    if bank == 'Boursorama':
        settings_halve = settings.bs_halve
        settings_except = settings.bs_except

    elif bank == 'Oney':
        settings_halve = settings.oney_halve
        settings_except = settings.oney_except

    elif bank == 'ING Direct':
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

    elif bank == 'Banque Populaire':
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

    month_boursorama = {
        'JANV.' : '01',
        'FÉVR.' : '02',
        'MARS' : '03',
        'AVR.' : '04',
        'MAI' : '05',
        'JUIN' : '06',
        'JUIL.' : '07',
        'AOÛT' : '08',
        'SEPT.' : '09',
        'OCT.' : '10',
        'NOV.' : '11',
        'DÉC.' : '12'
    }

    # mise en forme pour obtenir une liste sans tabulation, espace superflux, ...
    # et ou chaque element de la liste est une depense

    # Une entrée boursorama :
    # 19
    # JUIL.
    # -26,95 € PAIEMENT CARTE 170716 75 A2PAS Alimentation
    # ou
    # 28
    # JUIL.
    # 100 € VIR SEPA xxx Virements recus
    # On obtient une liste avec chaque entree sur 3
    data = data.split("\n")
    entries = []
    j = 0
    for i in range(len(data)):
        if i % 3 == 0:
            entries.append([data[i]])
        elif i % 3 == 1:
            entries[j].append(data[i])
        else:
            entries[j].append(data[i])
            j = j + 1

    for entry in entries:
        for i in range(3):
            entry[i] = re.sub(r" $", "", entry[i])
            entry[i] = re.sub(r"\r$", "", entry[i])

        # analyse de la premiere ligne
        # 3 formats possibles :
        # format_retrait/virement :['28', 'JUIL.', 'VIR SEPA xxx Virements recus']
        # format_CB : ['18', 'JUIL.', '-26,95 PAIEMENT CARTE 170716 75 A2PAS Alimentation']
        # format_avoir : ['10', '']
        # element a ne pas prendre en compte
        re_detail = re.compile(r"Dépenses carte .* de détails\)")
        re_releve = re.compile(r"Relevé différé Carte")

        if re.search(re_detail, entry[2]) or re.search(re_releve, entry[2]):
            continue


        # format Paiement / Avoir
        re_cb = re.compile(r"[0-9]{6} ")


        # format_retrait/virement
        if not re.search(re_cb, entry[2]) :
            # on recupere la date
            year = datetime.datetime.now().year
            month_num = month_boursorama[entry[1].encode('utf-8')]
            month = datetime.datetime.strptime(month_num , 
                                               '%m').month
            day = int(entry[0])
            date = datetime.datetime(year, month, day)

        # recherche € _ e[0] depense e[1] description
        e = entry[2].split(" \u20ac ")
        s = e[1]

        # format paiement
        re_pai = re.compile(r"PAIEMENT CARTE ")
        if re.match(re_pai, s):
            # on supprime le debut de ligne jusqu'a la date DDMMYY
            s = re.sub(re_pai, "", s)

        # format avoir
        re_av = re.compile(r"AVOIR ")
        if re.match(re_av, s):
            # on supprime le debut de ligne jusqu'a la date DDMMYY
            s = re.sub(re_av, "", s)

        # format retrait
        re_av = re.compile(r"RETRAIT DAB ")
        if re.match(re_av, s):
            # on supprime le debut de ligne jusqu'a la date DDMMYY
            s = re.sub(re_av, "", s)

        # format frais
        re_av = re.compile(r"CION OP.ETR ")
        if re.match(re_av, s):
            # on supprime le debut de ligne jusqu'a la date DDMMYY
            s = re.sub(re_av, "", s)

        # on recupere la date et on la supprime de la string
        # format Paiement / Avoir
        if re.search(re_cb, s):
            date = datetime.datetime.strptime(s[:6], "%d%m%y").date()
            s = s.replace(s[:6] + " ", "")

        # on recupere la description
        s = s.replace('75 ', '')
        s = s.replace('Alimentation', '')
        s = s.replace('Non catégorisé', '')
        s = s.replace('Electronique et informatique', '')
        s = s.replace('Transports quotidiens (métro, bus,...)', '')
        s = s.replace('Transports longue distance (avions, trains,...)', '')
        s = s.replace('Loisirs', '')
        s = s.replace('Mobilier, électroménager, décoration', '')
        s = s.replace('Restaurants, bars, discothèques...', '')
        s = s.replace('Frais bancaires et de gestion (dont agios)', \
                          'Frais bancaires')
        s = s.replace('Bricolage et jardinage', '')
        s = s.replace('Equipements sportifs et artistiques', '')
        s = s.replace('Vêtements et accessoires', '')
        s = s.replace('Virements recus', '')
        s = s.replace('VIR SEPA ', 'Virement ')
        description = s

        # on recupere la depense
        expense = float(e[0].replace(' ','').replace(',','.'))

        # element recupéré pour chacun des format
        # modification description
        description = change_description(description)

        # definition de subcategory
        subcategory = categories.utils.autoset_category(description)

        # halve or not
        halve = halve_or_not('Boursorama', description)
        if halve is True:
            expense = expense/2

        account = Account(date = date, description = description, expense = expense, \
              category = subcategory, bank = 'Boursorama', check = False, halve = halve)
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
        # [ '26/02/2015',
        #   'PAYPAL - 0800 942 890 - traite le 27/02',
        #   ' ',
        #   '45,80',
        #   ' \r' ]

        if len(e_list) < 4: # si e_list a moins de 4 éléments dernier élément
            continue
        description = e_list[1]
        if "Solde initial" in description :
            continue
        if "Prélèvement mensualité" in description :
            continue
        if "Intérêts" in description :
            continue

        # on definit chaque valeur d'un objet Account
	# on définit la date comme un objet datetime
        date = datetime.datetime.strptime(e_list[0], "%d/%m/%Y").date()
	# l'id = la date + la depense ex: 201502264580

        # description
        description = re.sub(r" - traité le .*$", "", description)
        description = re.sub(r" - [0-9 ]*PARIS[0-9 ]*$", "", description)
        # modification description
        description = change_description(description)

        # definition de subcategory
        subcategory = categories.utils.autoset_category(description)

        # expense : on récupère la dépense positive ou négtive
        if e_list[2] == ' ':
            expense = float('-' + e_list[3].replace(',','.'))
        elif e_list[3] == ' ':
            expense = float(e_list[2].replace(',','.'))

        # halve or not
        halve = halve_or_not('Oney', description)
        if halve is True:
            expense = expense/2

        account = Account(
                date        = date,
                description = description,
                expense     = expense,
                category    = subcategory,
                bank        = 'Oney',
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
    while line != "":

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
        if raw_currency != "EUR":
            raise ValueError("Currency is not EUR in transaction: %s" % line)

        # 4 - the description
        # Last but not least.
        # Modifications automatiques de la description et de la subcategory
        description = change_description(raw_description)
        subcategory = categories.utils.autoset_category(description)

        # halve or not
        halve = halve_or_not('ING Direct', description)
        if halve is True:
            expense = expense/2

        # Save the transaction in database
        account = Account( date        = date,
                           description = description,
                           expense     = expense,
                           category    = subcategory,
                           bank        = 'ING Direct',
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
            expense = float(csvdata[6].replace(',', '.'))

        # Description de l'opération et catégorisation
        description = csvdata[3]

        # Modifications automatiques de la description et de la subcategory
        description = change_description(description)
        subcategory = categories.utils.autoset_category(description)

        # halve or not
        halve = halve_or_not('Banque Populaire', description)
        if halve is True:
            expense = expense/2

        account = Account( date        = date,
                           description = description,
                           expense     = expense,
                           category    = subcategory,
                           bank        = 'Banque Populaire',
                           check       = False,
                           halve       = halve )
        account.save()


def import_boobank(data, bank):
    """ Parsing des données Boobank

        Le format die boobank est le suivant:

        Le séparateur par défaut est ' ' (point virgule)
        Les champs disponibles sont:
          - Date de l'opération (au format AAAA-MM-JJ) : 1-10 champs
          - Category : 14-25
          - Label    : 27-78
          - Montant  : 80-89
    """

    # Traitement par lignes des données
    for line in StringIO.StringIO(data):
        # Date de l'opération
        try:
            date = datetime.datetime.strptime(line[1:11], "%Y-%m-%d").date()
        except:
            continue

        # Montant de l'opération
        expense = float(line[80:90])

        # Description de l'opération et catégorisation
        description = line[27:79]

        # Modifications automatiques de la description et de la subcategory
        description = change_description(description)
        subcategory = categories.utils.autoset_category(description)

        # halve or not
        halve = halve_or_not(bank, description)
        if halve is True:
            expense = expense/2

        account = Account( date        = date,
                           description = description,
                           expense     = expense,
                           category    = subcategory,
                           bank        = bank,
                           check       = False,
                           halve       = halve )
        account.save()
