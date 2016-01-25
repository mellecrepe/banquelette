#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect, render
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.db.models import Sum, Avg
from account.models import Account
from account.forms import AccountForm, UpdateDbForm, MonthChoiceForm
from account.utils import import_data 
from datetime import date, time, datetime
import calendar
import locale

import categories

locale.setlocale(locale.LC_TIME,'')

# =============================================================================
def home(request):
    """ Page d'accueil """

    current_year   = datetime.now().year
    current_month  = datetime.now().month
    months         = current_year * 12 + current_month - 1

    triples = [ { "year"  : ((months - i) // 12),
                  "month" : ((months - i) %  12) +1 }
                    for i in reversed(range(12))      ]

    for t in triples:
	t["month_word"] = date( t["year"],
                                t["month"],
                                1           ).strftime('%B').capitalize()

    # 1e partie : graph des dépenses de l'annee
    total_by_month = { "all"        : [],
                       "gain"       : [],
                       "necessaire" : [],
                       "achat"      : [],
                       "sortie"     : [],
                       "vacances"   : [],
                       "autre"      : [] } 

    # 2e partie : variable pour les camemberts
    average       = { "gain"       : 0,
                      "necessaire" : 0,
                      "achat"      : 0,
                      "sortie"     : 0,
                      "vacances"   : 0,
                      "autre"      : 0 } 
    average_month = { "gain"       : 0,
                      "necessaire" : 0,
                      "achat"      : 0,
                      "sortie"     : 0,
                      "vacances"   : 0,
                      "autre"      : 0 } 

    for t in triples :
        account_filter_year  = Account.objects  \
                .filter( date__year=t["year"] )
        account_filter_month = account_filter_year \
                .filter( date__month=t["month"] )

        for k in total_by_month:
            if k == "all":
                try: 
                    total_by_month["all"].append(
                            abs(int( account_filter_month.aggregate(Sum('expense'))['expense__sum'] ))
                            )
                except:
                    total_by_month["all"].append(0)

                continue

            try: 
                total_by_month[k].append(
                        abs(int( account_filter_month.filter(category__exact=k).aggregate(Sum('expense'))['expense__sum'] ))
                        )
            except:
                total_by_month[k].append(0)

            account_filter_category = account_filter_year.filter(category__exact=k)
            average_tmp = account_filter_category.aggregate(Avg('expense'))['expense__avg']

            if average_tmp is None:
                average[k] = 0
            else:
                average[k] = int(average_tmp)

            average_tmp = account_filter_category.filter( date__month=t["month"] ).aggregate(Avg('expense'))['expense__avg']

            if average_tmp is None:
                average_month[k] = 0
            else:
                average_month[k] = int(average_tmp)

    return render(request, 'account/accueil.html', locals())

# =============================================================================
def release(request):
    """ Release """
    return render(request, 'account/release.html')
    

# =============================================================================
def month_view(request, year, month):
    """ Résumé par mois """
    if not year or not month:
        raise Http404

    month_word = date(int(year), int(month), 1).strftime('%B').capitalize()

    # Get all objects (transactions) with the right date (year+month) and order
    # them by date.
    account_objects = Account.objects        \
            .order_by('date')                \
            .filter(date__year = int(year) ) \
            .filter(date__month= int(month))

    # Get the first-level categories (those without a parent category)
    categories = { c : 0 for c in categories.FIRST_LEVEL_CATEGORIES }

    # For each first-level category, we are going to find the relevant objects
    # (transactions) and sum them.
    for c in categories:

        # Sum the relevant account object 'expense' property
        category_sum = account_objects               \
                .filter(subcategory__startswith = c) \
                .aggregate(Sum('expense'))

        # Save the result
        if category_sum['expense__sum'] is not None:
            categories[c] = category_sum['expense__sum']

    # We got the sum of expenses for each category, now we can add a 'Total'
    # category:
    categories["Total"] = account_objects    \
            .aggregate(Sum('expense'))['expense__sum']

    # And done!
    return render(request, 'account/month.html', locals())

# =============================================================================
def month_choice(request):
    """ Choix du mois """
    title = "Choix du mois"
    if request.method == 'POST':
        form = MonthChoiceForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            return redirect(db_modify, year=year, month=month)
    else:
        form=MonthChoiceForm()

    return render(request, 'account/month_choice.html', locals())
    
    
def db_modify(request, year=None, month=None):
    """ Modification par mois ou les non check"""
    # definition des variables
    if year == None:
        title = "Dépenses non validées"
        account_all = Account.objects.filter(check__exact=False)
    else:
        month_word = date(int(year), int(month), 1).strftime('%B').capitalize().decode('utf-8')
        title = ''.join([month_word, " ", year])
        account_all = Account.objects.filter(date__year=int(year)).filter(date__month=int(month))

    AccountFormSet = modelformset_factory(Account, fields=('date', 'description', 'subcategory', 'expense', 'halve', 'bank', 'check', 'comment'), extra=0, can_delete=True)
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        formset = AccountFormSet(request.POST)
        if formset.is_valid(): # Nous vérifions que les données envoyées sont valides
           formset.save()
           if year == None:
               return redirect(home)
           return redirect(month_view, year=year, month=month)

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        formset = AccountFormSet(queryset=account_all)
    return render(request, 'account/db_modify.html', locals())

	
def db_add(request):
    """ Ajout d'entrées manuelles """
    title = "Ajout d'entrées manuelles"
    n = 5
    AccountFormSet = modelformset_factory(Account, fields=('date', 'description', 'subcategory', 'expense', 'halve', 'bank', 'check', 'comment'), extra=n, can_delete=True)
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        formset = AccountFormSet(request.POST)
        if formset.is_valid(): 
            formset.save()
            return redirect(home)

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        formset = AccountFormSet(queryset=Account.objects.none())

    return render(request, 'account/db_add.html', locals())
    

def db_update(request):
    """ Mise à jour de la base de donnée avec de nouvelles données """
    if request.method == 'POST':
        form = UpdateDbForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            bank = form.cleaned_data['bank']
            # Analyse des données stockées dans une liste
            import_data(data, bank)
            return redirect(db_modify)
    else:
        form=UpdateDbForm()

    return render(request, 'account/db_update.html', locals())
