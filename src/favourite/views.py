from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from basic.models import HistoryPart, FavouritePart


class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

def favourite(request):	
    favs_all = FavouritePart.objects.filter(user=request.user).order_by('-time')

    ## paginate
    page = request.GET.get('page')
    paginator = Paginator(favs_all, 10) ## settings.PRODUCTS_PER_PAGE
    try:
        favs = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        favs = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages ## ??
        favs = paginator.page(paginator.num_pages)

    return render(request, 'favourite/favourite.html', { 
        'favs' : favs, 
        'page' : page,
        'total' : len(favs_all),
        'now' : len(favs)+((int(page)-1)*10),
        'favs_empty_or_not_logged' : len(favs) == 0 or not request.user.is_authenticated
    })