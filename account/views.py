#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect, render
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from account.models import Account
from account.forms import AccountForm, UpdateDbForm, MonthChoiceForm
from account.utils import import_data 
from datetime import date, time, datetime
import calendar
import locale

locale.setlocale(locale.LC_TIME,'')

def home(request):
    """ Page d'accueil """

    now = datetime.now()
    year = str(now.year)
    month = str(now.month).rjust(2, '0')

    # 1e partie : graph des dépense de l'annee
    total = [ 0 for i in range(0,12) ]
    gain = [ 0 for i in range(0,12) ]
    necessaire = [ 0 for i in range(0,12) ]
    necessaire_achat =  [ 0 for i in range(0,12) ]
    necessaire_achat_sortie =  [ 0 for i in range(0,12) ]
    necessaire_achat_sortie_vacances =  [ 0 for i in range(0,12) ]

    # 2e partie : variable pour 1e camembert
    necessaire_average = 0
    achat_average = 0
    sortie_average = 0
    vacances_average = 0
    autre_average = 0


    for i in range(0,12):
        str_i = str(i+1).rjust(2, '0')
        startkey = ''.join([year, "-", str_i, "-01"])
        endkey = ''.join([year, "-", str_i, "-", str(calendar.monthrange(int(2015), i+1)[1])])

        tmp = Account.view("sum/all", startkey=startkey, endkey=endkey).first()
        if tmp is not None:
            total[i] = int(tmp["value"])
        tmp = Account.view("sum/gain", startkey=startkey, endkey=endkey).first()
        if tmp is not None:
            gain[i] = int(tmp["value"])
            necessaire[i] = int(tmp["value"])
            necessaire_achat[i] = int(tmp["value"])
            necessaire_achat_sortie[i] = int(tmp["value"])
            necessaire_achat_sortie_vacances[i] = int(tmp["value"])

        tmp_necessaire = Account.view("sum/necessaire", startkey=startkey, endkey=endkey).first()
        tmp_achat = Account.view("sum/achat", startkey=startkey, endkey=endkey).first()
        tmp_sortie = Account.view("sum/sortie", startkey=startkey, endkey=endkey).first()
        tmp_vacances = Account.view("sum/vacances", startkey=startkey, endkey=endkey).first()
        tmp_autre = Account.view("sum/autre", startkey=startkey, endkey=endkey).first()

        if tmp_necessaire is not None:
            necessaire[i] = necessaire[i] + (int(tmp_necessaire["value"]))
            necessaire_achat[i] = necessaire_achat[i] + (int(tmp_necessaire["value"]))
            necessaire_achat_sortie[i] = necessaire_achat_sortie[i] + (int(tmp_necessaire["value"]))
            necessaire_achat_sortie_vacances[i] = necessaire_achat_sortie_vacances[i] + (int(tmp_necessaire["value"]))
            necessaire_average = necessaire_average + (int(tmp_necessaire["value"]))
        if tmp_achat is not None:
            necessaire_achat[i] = necessaire_achat[i] + (int(tmp_achat["value"]))
            necessaire_achat_sortie[i] = necessaire_achat_sortie[i] + (int(tmp_achat["value"]))
            necessaire_achat_sortie_vacances[i] = necessaire_achat_sortie_vacances[i] + (int(tmp_achat["value"]))
            achat_average = achat_average + (int(tmp_achat["value"]))
        if tmp_sortie is not None:
            necessaire_achat_sortie[i] = necessaire_achat_sortie[i] + (int(tmp_sortie["value"]))
            necessaire_achat_sortie_vacances[i] = necessaire_achat_sortie_vacances[i] + (int(tmp_sortie["value"]))
            sortie_average = sortie_average + (int(tmp_sortie["value"]))
        if tmp_vacances is not None:
            necessaire_achat_sortie_vacances[i] = necessaire_achat_sortie_vacances[i] + (int(tmp_vacances["value"]))
            vacances_average = vacances_average + (int(tmp_vacances["value"]))
        if tmp_autre is not None:
            autre_average = autre_average + (int(tmp_autre["value"]))

    # 2e partie : camemberts
    necessaire_average = necessaire_average/12
    achat_average = achat_average/12
    sortie_average = sortie_average/12
    vacances_average = vacances_average/12
    autre_average = autre_average/12

    # 2e camembert : moyenne sur le mois
    startkey = ''.join([year, "-", month, "-01"])
    endkey = ''.join([year, "-", month, "-", str(calendar.monthrange(int(2015), i+1)[1])])
    tmp = Account.view("sum/necessaire", startkey=startkey, endkey=endkey).first()
    if tmp is None:
        necessaire_average_month = 0
    else:
        necessaire_average_month = int(tmp["value"])

    tmp = Account.view("sum/achat", startkey=startkey, endkey=endkey).first()
    if tmp is None:
        achat_average_month = 0
    else:
        achat_average_month = int(tmp["value"])
    
    tmp = Account.view("sum/sortie", startkey=startkey, endkey=endkey).first()
    if tmp is None:
        sortie_average_month = 0    
    else:
        sortie_average_month = int(tmp["value"])
    
    tmp = Account.view("sum/vacances", startkey=startkey, endkey=endkey).first()
    if tmp is None:
        vacances_average_month = 0    
    else:
        vacances_average_month = int(tmp["value"])

    tmp = Account.view("sum/autre", startkey=startkey, endkey=endkey).first()
    if tmp is None:
        autre_average_month = 0    
    else:
        autre_average_month = int(tmp["value"])

    return render(request, 'account/accueil.html', locals())

def release(request):
    """ Release """
    return render(request, 'account/release.html')
    

def month_view(request, year, month):
    """ Résumé par mois """
    if not year or not month:
        raise Http404

    month_word = date(int(year), int(month), 1).strftime('%B').capitalize()
    startkey = ''.join([year, "-", month, "-01"])
    endkey = ''.join([year, "-", month, "-", str(calendar.monthrange(int(year), int(month))[1])])
    account_all = Account.view("all/by_date", startkey=startkey, endkey=endkey)
    category={'necessaire': '0', 'achat' : '0', 'sortie': '0', 'vacances': '0', 'autre' : '0', 'gain': '0', 'all': '0'}
    for c in category:
        category_view = Account.view("sum/"+c, startkey=startkey, endkey=endkey).first()
        if category_view is None:
            continue
        category[c] = category_view["value"]
    return render(request, 'account/month.html', locals())

def month_choice(request):
    """ Choix du mois """
    title = "Choix du mois"
    if request.method == 'POST':
        form = MonthChoiceForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            return redirect(couchdb_modify, year=year, month=month)
    else:
        form=MonthChoiceForm()

    return render(request, 'account/month_choice.html', locals())
    
    
def couchdb_modify(request, year=None, month=None):
    """ Modification par mois ou les non check"""
    # definition des variables
    if year == None:
        title = "Dépenses non validées"
        account_all = Account.view("all/check_false")
    else:
        month_word = date(int(year), int(month), 1).strftime('%B').capitalize().decode('utf-8')
        startkey = ''.join([year, "-", month, "-", "01"])
        endkey = ''.join([year, "-", month, "-", str(calendar.monthrange(int(year), int(month))[1])])
        account_all = Account.view("all/by_date", startkey=startkey, endkey=endkey)
        title = ''.join([month_word, " ", year])

    if request.method == 'POST':  # S'il s'agit d'une requête POST
        for a in account_all:
            f = AccountForm(request.POST, instance = a, prefix = a.get_id)
            f.is_valid() # Nous vérifions que les données envoyées sont valides
            if f.cleaned_data['delete']:
                a.delete()    
            else:
                f.save()
        if year == None:
            return redirect(home)
        return redirect(month_view, year=year, month=month)

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form_list = []
        for a in account_all:
            form_list.append(AccountForm(instance = a, prefix = a.get_id))
    return render(request, 'account/couchdb_modify.html', locals())

	
def couchdb_add(request):
    """ Ajout d'entrées manuelles """
    title = "Ajout d'entrées manuelles"
    n = 5
    AccountFormSet = formset_factory(AccountForm, extra = n)
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        formset = AccountFormSet(request.POST)
        if formset.is_valid(): 
            for i in range(0, n):
                if not formset.cleaned_data[i]:
                    continue
                date = formset.cleaned_data[i]['date']
                description = formset.cleaned_data[i]['description']
                subcategory = formset.cleaned_data[i]['subcategory']
                expense = formset.cleaned_data[i]['expense']
                check = formset.cleaned_data[i]['check']
                halve = formset.cleaned_data[i]['halve']
                a = Account(date=date, description=description, subcategory=subcategory,
                    expense=expense, halve=halve, check=check)
                a.save()
            return redirect(home)

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        formset = AccountFormSet()

    return render(request, 'account/couchdb_add.html', locals())
    

def couchdb_update(request):
    """ Mise à jour de la base de donnée avec de nouvelles données """
    if request.method == 'POST':
        form = UpdateDbForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            bank = form.cleaned_data['bank']
            # Analyse des données stocké dans une liste
            import_data(data, bank)
            return redirect(couchdb_modify)
    else:
        form=UpdateDbForm()

    return render(request, 'account/couchdb_update.html', locals())
