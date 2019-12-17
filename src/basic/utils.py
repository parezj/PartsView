import urllib
from urllib.parse import quote
    
def extract_relevant_data(res):

    digikey_mnu = []
    digikey_usd = []
    mouser_mnu = []
    mouser_eur = []
    farnell_mnu = []
    farnell_eur = []

    prices2 = []
    datasheets2 = []

    imgs_big = []
    imgs_big2 = []
    imgs_big3 = []
    imgs_big4 = []
    imgs_small = []

    specs = []
    names_enc = []
        
    for r in res:
        names_enc.append(quote(r["item"]["mpn"]))

        imgs_big_cnt = 1
        imgs_big2_cnt = 0
        imgs_big3_cnt = 0
        imgs_big4_cnt = 0
        imgs_small_cnt = 1
        for dat in r["item"]["imagesets"]:
            if imgs_small_cnt == 1 and "small_image" in dat and dat["small_image"] is not None:
                imgs_small.append(dat["small_image"]["url"])
                imgs_small_cnt = 0
            if imgs_big_cnt == 1 and "medium_image" in dat and dat["medium_image"] is not None:
                imgs_big.append(dat["medium_image"]["url"])
                imgs_big_cnt = 0
                imgs_big2_cnt = 1
                continue
            if imgs_big2_cnt == 1 and "medium_image" in dat and dat["medium_image"] is not None:
                imgs_big2.append(dat["medium_image"]["url"])
                imgs_big2_cnt = 0
                imgs_big3_cnt = 1
                continue
            if imgs_big3_cnt == 1 and "medium_image" in dat and dat["medium_image"] is not None:
                imgs_big3.append(dat["medium_image"]["url"])
                imgs_big3_cnt = 0
                imgs_big4_cnt = 1
                continue
            if imgs_big4_cnt == 1 and "medium_image" in dat and dat["medium_image"] is not None:
                imgs_big4.append(dat["medium_image"]["url"])
                imgs_big4_cnt = 0
            if imgs_small_cnt == 0 and imgs_big_cnt == 0 and imgs_big2_cnt == 0 and imgs_big3_cnt == 0 and imgs_big4_cnt == 0:
                break
        if imgs_small == []:
            imgs_small.append("/static/img/blank_part_small.png")
        if imgs_big == []:
            imgs_big.append("/static/img/blank_part_big.png")
        if imgs_big2 == []:
            imgs_big2.append("")
        if imgs_big3 == []:
            imgs_big3.append("")
        if imgs_big4 == []:
            imgs_big4.append("")
                
        for dat in r["item"]["datasheets"]:
            if dat["mimetype"] == "application/pdf":
                datasheets2.append(dat["url"])
                break
        if datasheets2 == []:
            datasheets2.append("")

        s = []
        for key, value in r["item"]["specs"].items():
            try:
                s.append({"name" : value["metadata"]["name"], "val" : value["display_value"]})
            except Exception as e:
                pass
                ## raise e
        if s == []:
            specs.append([{" " : " "}])
        else:
            specs.append(s)
        
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
                pass
                ##raise e
            try:  
                if off["seller"]["name"] == "Mouser" and "USD" in off["prices"]:
                    mouser_mnu = off["prices"]["USD"][0][0]
                    mouser_eur = round(float(off["prices"]["USD"][0][1]), 2)
            except Exception as e:
                pass
                ##raise e
            try:  
                if off["seller"]["name"] == "Farnell" and "EUR" in off["prices"]:
                    farnell_mnu = off["prices"]["EUR"][0][0]
                    farnell_eur = round(float(off["prices"]["EUR"][0][1]), 2)
            except Exception as e:
                pass
                ##raise e
                
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
        
    for i, n in enumerate(imgs_small):
        res[i]["img_small"] = n

    for i, n in enumerate(imgs_big):
        res[i]["img_big"] = n

    for i, n in enumerate(imgs_big2):
        res[i]["img_big2"] = n

    for i, n in enumerate(imgs_big3):
        res[i]["img_big3"] = n

    for i, n in enumerate(imgs_big4):
        res[i]["img_big4"] = n

    for i, n in enumerate(specs):
        res[i]["specs"] = n

    for i, n in enumerate(names_enc):
        res[i]["name_enc"] = n

    return res
    