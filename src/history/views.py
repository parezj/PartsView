from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from basic.models import HistoryPart, FavouritePart


class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

def history(request): 
    hists_all = HistoryPart.objects.filter(user=request.user).order_by('-time')

    ## paginate
    page = request.GET.get('page')
    paginator = Paginator(hists_all, 10) ## settings.PRODUCTS_PER_PAGE
    try:
        hists = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        hists = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages ## ??
        hists = paginator.page(paginator.num_pages)

    return render(request, 'history/history.html', { 
        'hists' : hists, 
        'page' : page,
        'total' : len(hists_all),
        'now' : len(hists)+((int(page)-1)*10),
        'hists_empty_or_not_logged' : len(hists) == 0 or not request.user.is_authenticated
    })