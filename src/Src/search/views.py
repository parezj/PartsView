from django.shortcuts import render
import json
import urllib
from urllib.parse import unquote
import pickle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
OFFLINE = False
    
def search(request, part):
        
    if OFFLINE == True:        
        part = "bq2"
        
    part2 = unquote(part)
            
    try:    
        try:   
            with open('ajax/query/' + part + '.json', 'r') as f:
                search_response = json.load(f)
                res = search_response['results']
        except:
            return render(request, 'ajax/query.html', { 'part' : part })
        
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
        
        digikey_mnu = []
        digikey_usd = []
        mouser_mnu = []
        mouser_eur = []
        farnell_mnu = []
        farnell_eur = []
        
        prices2 = []
        datasheets2 = []
        imgs2 = []
            
        for r in res:
            for dat in r["item"]["imagesets"]:
                if "small_image" in dat:
                    imgs2.append(dat["small_image"]["url"])
                    break
                    
            for dat in r["item"]["datasheets"]:
                if dat["mimetype"] == "application/pdf":
                    datasheets2.append(dat["url"])
                    break
            
            digikey_mnu = 0
            digikey_usd = 0
            mouser_mnu = 0
            mouser_eur = 0
            farnell_mnu = 0
            farnell_eur = 0
                
            for off in r["item"]["offers"]:
                try:  
                    if off["seller"]["name"] == "Digi-Key" and "USD" in off["prices"]:
                        digikey_mnu = off["prices"]["USD"][0][0]
                        digikey_usd = round(float(off["prices"]["USD"][0][1]), 2)
                except Exception as e:
                    raise e
                try:  
                    if off["seller"]["name"] == "Mouser" and "USD" in off["prices"]:
                        mouser_mnu = off["prices"]["USD"][0][0]
                        mouser_eur = round(float(off["prices"]["USD"][0][1]), 2)
                except Exception as e:
                    raise e
                try:  
                    if off["seller"]["name"] == "Farnell" and "EUR" in off["prices"]:
                        farnell_mnu = off["prices"]["EUR"][0][0]
                        farnell_eur = round(float(off["prices"]["EUR"][0][1]), 2)
                except Exception as e:
                    raise e
                    
            prices2.append({ 
                "digikey_mnu" : digikey_mnu, 
                "digikey_usd" : digikey_usd, 
                "mouser_mnu" : mouser_mnu, 
                "mouser_eur" : mouser_eur, 
                "farnell_mnu" : farnell_mnu, 
                "farnell_eur" : farnell_eur, 
            })
                
        
        for i, n in enumerate(prices2):
            res[i]["prices2"] = n
            
        for i, n in enumerate(datasheets2):
            res[i]["datasheet2"] = n
            
        for i, n in enumerate(imgs2):
            res[i]["img2"] = n
        
            
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
            'farnell_mnu' : farnell_mnu,
            'farnell_eur' : farnell_eur
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
            'farnell_mnu' : farnell_mnu,
            'farnell_eur' : farnell_eur
        })
