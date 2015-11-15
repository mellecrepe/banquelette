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

    # 1e partie : graph des dépenses de l'annee
    total_by_month = {"all": [], "gain": [], "necessaire": [], "achat": [], "sortie": [], "vacances": [], "autre": []} 

    # 2e partie : variable pour 1e camembert
    average = {"all": 0, "gain": 0, "necessaire": 0, "achat": 0, "sortie": 0, "vacances": 0, "autre": 0} 
    month_average = {"all": 0, "gain": 0, "necessaire": 0, "achat": 0, "sortie": 0, "vacances": 0, "autre": 0} 

    for i in range(0,12):
        str_i = str(i+1).rjust(2, '0')
        startkey = ''.join([year, "-", str_i, "-01"])
        endkey = ''.join([year, "-", str_i, "-", str(calendar.monthrange(int(2015), i+1)[1])])

        for k in total_by_month.keys():
            try: 
                tmp = int(Account.view(''.join(["sum/", k]), startkey=startkey, endkey=endkey).first()["value"])
                total_by_month[k].append(abs(tmp))
                average[k] = average[k] + tmp
                
            except:
                total_by_month[k].append(0)

    # 2e partie : camemberts
    for k in average.keys():
        average[k] = average[k]/12

    # 2e camembert : moyenne sur le mois
    startkey = ''.join([year, "-", month, "-01"])
    endkey = ''.join([year, "-", month, "-", str(calendar.monthrange(int(2015), i+1)[1])])

    for k in month_average.keys():
        try:
            tmp = Account.view(''.join(["sum/", k]), startkey=startkey, endkey=endkey).first()
            month_average[k] = int(tmp["value"])
        except:
            month_average[k] = 0

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
    for a in account_all:
        try:
            a.comment
        except AttributeError:
            comment = False
        else: 
            comment = True
            continue

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
