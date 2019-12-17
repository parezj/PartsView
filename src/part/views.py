from django.shortcuts import render
from django.conf import settings
from basic.utils import extract_relevant_data
from urllib.parse import unquote, quote
from django.conf import settings
import json


from basic.models import HistoryPart, FavouritePart

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

OFFLINE = settings.OFFLINE

def part(request, part, searched):	
        
    if OFFLINE == True:        
        part = "BQ24610RGET"
        searched = "bq2"
        
    part2 = unquote(part)
    searched2 = unquote(searched)

    backlink = "/search/" + searched
    if "refn" in request.GET:
        backlink = "/" + request.GET["refn"]
    if "refp" in request.GET:
        backlink += "?page=" + request.GET["refp"]
            
    try:   
        with open(settings.CACHE_QUERY_PATH + searched + '.json', 'r') as f:
            search_response = json.load(f)

            res = [x for x in search_response['results'] if "mpn" in x['item'] and x['item']['mpn'] == part2]
            if len(res) < 1:
            	raise Exception('seach json found but item inside is missing')
    except Exception as e:
        #raise e
        return render(request, 'ajax/query.html', { 'next' : 'part', 'part' : part2, 'searched' : searched2 })
    
    res = (extract_relevant_data(res))[0]

    HistoryPart.objects.filter(name=res["item"]["mpn"]).delete()
    fav = len(FavouritePart.objects.filter(name=res["item"]["mpn"])) > 0

    res2 = { 'name' : res["item"]["mpn"],
        'name_enc' : quote(res["item"]["mpn"]),
        'user' : str(request.user),
        'manuf' : res["item"]["manufacturer"]["name"],
        'desc' : res["snippet"],
        'pdf' : res["datasheet2"],
        'octo' : res["item"]["octopart_url"],
        'search' : searched,
        'search_enc' : quote(searched),
        'img_big' : res["img_big"],
        'img_big2' : res["img_big2"],
        'img_big3' : res["img_big3"],
        'img_big4' : res["img_big4"],
        'img_small' : res["img_small"],
        'img_footprint' : "",
        'img_symbol' : "",
        'farnell_mnu' : res["prices2"]["farnell_mnu"],
        'farnell_czk' : res["prices2"]["farnell_eur"],
        'mouser_mnu' : res["prices2"]["mouser_mnu"],
        'mouser_eur' : res["prices2"]["mouser_eur"],
        'digikey_mnu' : res["prices2"]["digikey_mnu"],
        'digikey_usd' : res["prices2"]["digikey_usd"],
        'specs' : res["specs"],
        'fav' : fav
    }

    if (request.user.is_authenticated):
        p = HistoryPart(user = request.user,
                        name = res["item"]["mpn"],
                        name_enc = quote(res["item"]["mpn"]),
                        manuf = res["item"]["manufacturer"]["name"],
                        desc = res["snippet"],
                        pdf = res["datasheet2"],
                        octo = res["item"]["octopart_url"],
                        search = searched,
                        search_enc = quote(searched),
                        img_big = res["img_big"],
                        img_big2 = res["img_big2"],
                        img_big3 = res["img_big3"],
                        img_big4 = res["img_big4"],
                        img_small = res["img_small"],
                        img_footprint = "",
                        img_symbol = "",
                        farnell_mnu = res["prices2"]["farnell_mnu"],
                        farnell_czk = res["prices2"]["farnell_eur"],
                        mouser_mnu = res["prices2"]["mouser_mnu"],
                        mouser_eur = res["prices2"]["mouser_eur"],
                        digikey_mnu = res["prices2"]["digikey_mnu"],
                        digikey_usd = res["prices2"]["digikey_usd"],
                        specs = res["specs"])
        p.save()
        
    return render(request, 'part/part.html', { 
        'node' : res, 
        'searched' : searched,
        'nodeJson' : json.dumps(res2), 
        'fav' : fav,
        'backlink' : backlink,
        'logged' : request.user.is_authenticated
    })