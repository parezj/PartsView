from django.shortcuts import render
import json
import urllib
from urllib.parse import unquote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.conf import settings
from django.conf import settings
from basic.utils import extract_relevant_data

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
OFFLINE = settings.OFFLINE
    
def search(request, part):
        
    if OFFLINE == True:        
        part = "bq2"
        
    part2 = unquote(part)
            
    try:    
        try:   
            with open(settings.CACHE_QUERY_PATH + part + '.json', 'r') as f:
                search_response = json.load(f)
                res = search_response['results']
        except:
            return render(request, 'ajax/query.html', { 'part' : part, 'next' : 'search' })
        
        ## paginate
        page = request.GET.get('page')
        paginator = Paginator(res, 10) ## settings.PRODUCTS_PER_PAGE
        try:
            parts = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            parts = paginator.page(1)
        except EmptyPage:
            page = paginator.num_pages ## ??
            parts = paginator.page(paginator.num_pages)
        
        res = extract_relevant_data(res)
            
        return render(request, 'search/search.html', { 
            'parts' : parts, 
            'hits' : search_response['hits'], 
            'msec' : search_response['msec'], 
            'searched_enc' : part, 
            'searched' : part2, 
            'error' : '', 
            'err': False ,
            'total' : len(res),
            'now' : len(parts)+((int(page)-1)*10),
            'offline' : OFFLINE
        })
    except Exception as e:
        ## raise e
        return render(request, 'search/search.html', { 
            'parts' : [], 
            'hits' : 0, 
            'msec' : 0,
            'searched_enc' : part, 
            'searched' : part2, 
            'error' : e, 
            'err' : True,
            'total' : 0,
            'now' : 0,
            'offline' : OFFLINE
        })
