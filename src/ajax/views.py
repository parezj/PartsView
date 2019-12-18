from django.shortcuts import render
from django.http import JsonResponse
import json
import urllib
from urllib.parse import unquote, quote
import time
import requests
import argparse
from django.conf import settings
import os
import logging
import wave

from basic.models import HistoryPart, FavouritePart


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.AJAX_PATH + "google.json"
ocr_api_key = "f15f1595ea88957"
octopart_api_key = "548dbd02df0dfc20df42"

OFFLINE = settings.OFFLINE

logger = logging.getLogger(__name__)

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

def upload(request):	      
    timestr = time.strftime("%Y%m%d_%H%M%S")
    try:
        if 'rec' in request.FILES:
            f = request.FILES['rec']
            foo = settings.CACHE_UPLOAD_PATH + "rec_" + timestr + ".wav"
            with open(foo, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            with wave.open(foo, "rb") as wave_file:
                frame_rate = wave_file.getframerate()
            text = transcribe_file(foo, frame_rate)         
            response = JsonResponse({"speech": text})
            response.status_code = 200
            return response
            
        elif 'capture' in request.FILES and 'ext' in request.POST:
            f = request.FILES['capture']
            ext = request.POST['ext']
            foo = settings.CACHE_UPLOAD_PATH + "capture_" + timestr + ext
            with open(foo, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            text = ocr_space_file(foo, False, ocr_api_key)
            response = JsonResponse({"ocr": text})
            response.status_code = 200
            return response
        
        else:
            response = JsonResponse({"error": "no input file"})
            response.status_code = 404
            return response
    except Exception as e:
        response = JsonResponse({"error": str(e)})
        response.status_code = 500
        return response
        
def query(request):	
    
    if OFFLINE == True:
        response = JsonResponse({"error": "offline mode"})
        response.status_code = 501
        return response
        
    if type(request) is str:
        part = request
    elif request.POST and'part' in request.POST:
        part = request.POST['part']
    else:
        response = JsonResponse({"error": "search query missing (AJAX GET or string via API)"})
        response.status_code = 404
        return response
        
    partf = settings.CACHE_QUERY_PATH + part + '.json'

    try:   
        with open(partf, 'r') as f:
            json.load(f)
            response = JsonResponse({"success": partf})
            response.status_code = 201
            return response
    except Exception as e: 
        url = "http://octopart.com/api/v3/parts/search"
        url += "?apikey=" + octopart_api_key
        url += "&include[]=imagesets"
        url += "&include[]=specs"
        url += "&include[]=datasheets"
        url += "&include[]=cad_models"
        
        part2 = unquote(part)
        
        args = [
           ('q', part2),
           ('start', 0),
           ('limit', 50)]
        
        try:       
            
            url += '&' + urllib.parse.urlencode(args)     
            data = urllib.request.urlopen(url).read()
            search_response = json.loads(data)
            res = search_response['results']     
        
            with open(partf, 'w') as f:
                json.dump(search_response, f, indent=4, sort_keys=True)
                    
            response = JsonResponse({"success": partf})
            response.status_code = 200
            return response
            
        except Exception as e:
            response = JsonResponse({"error": str(e)})
            response.status_code = 500
            return response

def fav_add(request):          
    try:
        if request.method == 'POST':
            data = json.loads(str(request.body.decode("utf-8")).replace('&quot;', '"').strip('b').strip("'"))
        else:
            response = JsonResponse({"error": "POST data missing"})
            response.status_code = 404
            return response

        f = FavouritePart(user = request.user,
            name = data["name"],
            name_enc = quote(data["name"]),
            manuf = data["manuf"],
            desc = data["desc"],
            pdf = data["pdf"],
            octo = data["octo"],
            search = data["search"],
            search_enc = quote(data["search"]),
            img_big = data["img_big"],
            img_big2 = data["img_big2"],
            img_big3 = data["img_big3"],
            img_big4 = data["img_big4"],
            img_small = data["img_small"],
            img_footprint = "",
            img_symbol = "",
            farnell_mnu = data["farnell_mnu"],
            farnell_czk = data["farnell_czk"],
            mouser_mnu = data["mouser_mnu"],
            mouser_eur = data["mouser_eur"],
            digikey_mnu = data["digikey_mnu"],
            digikey_usd = data["digikey_usd"],
            specs = data["specs"])
        f.save()

        response = JsonResponse({"success": "added to fav list"})
        response.status_code = 200
        return response

    except Exception as e:
        response = JsonResponse({"error": str(e)})
        response.status_code = 500
        return response

def fav_del(request):          
    try:
        if request.method == 'POST':
            logger.error("START" + str(request.body.decode("utf-8")).strip('b').strip("'"))
            data = json.loads(str(request.body.decode("utf-8")).replace('&quot;', '"').strip('b').strip("'"))
        else:
            response = JsonResponse({"error": "POST data missing"})
            response.status_code = 404
            return response

        FavouritePart.objects.filter(user=request.user, name=data["name"]).delete()
        response = JsonResponse({"success": "removed from fav list"})
        response.status_code = 200
        return response

    except Exception as e:
        response = JsonResponse({"error": str(e)})
        response.status_code = 500
        return response

def fav_flush(request):
    try:
        FavouritePart.objects.filter(user=request.user).delete()
        response = JsonResponse({"success": "fav list flushed"})
        response.status_code = 200
        return response

    except Exception as e:
        raise e
        response = JsonResponse({"error": str(e)})
        response.status_code = 500
        return response

def hist_flush(request):
    try:
        HistoryPart.objects.filter(user=request.user).delete()
        response = JsonResponse({"success": "history list flushed"})
        response.status_code = 200
        return response

    except Exception as e:
        raise e
        response = JsonResponse({"error": str(e)})
        response.status_code = 500
        return response

def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,)
        return r.content.decode()
        
# [START speech_transcribe_sync]
def transcribe_file(speech_file, frame_rate):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    import io
    client = speech.SpeechClient()

    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code='en-US')
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    response = client.recognize(config, audio)
    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.

    #logger = logging.getLogger("django")
    #logger.info("RRESPONSE:" + str(response))
    #return response

    ret = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        ret.append(format(result.alternatives[0].transcript))
    return ret
    # [END speech_python_migration_sync_response]
    # [END speech_transcribe_sync]