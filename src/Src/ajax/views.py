from django.shortcuts import render
from django.http import JsonResponse
import json
import urllib
from urllib.parse import unquote
import time
import requests
import argparse

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ajax/google.json"
ocr_api_key = ""

OFFLINE = True

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

def upload(request):	      
    timestr = time.strftime("%Y%m%d_%H%M%S")
    try:
        if 'rec' in request.FILES:
            f = request.FILES['rec']
            foo = "ajax/upload/rec_" + timestr + ".wav"
            with open(foo, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            text = transcribe_file(foo)         
            response = JsonResponse({"speech": text})
            response.status_code = 200
            return response
            
        elif 'capture' in request.FILES and 'ext' in request.POST:
            f = request.FILES['capture']
            ext = request.POST['ext']
            foo = "ajax/upload/capture_" + timestr + ext
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
        response = JsonResponse({"error": e})
        response.status_code = 500
        return response
        
def query(request):	
    
    if OFFLINE == True:
        response = JsonResponse({"error": "offline mode"})
        response.status_code = 500
        return response
        
    if 'part' in request.POST:
        part = request.POST['part']
    else:
        response = JsonResponse({"error": "GET part missing"})
        response.status_code = 404
        return response
        
    try:   
        with open('ajax/query/' + part + '.json', 'r') as f:
            response = JsonResponse({"success": "offline cache"})
            response.status_code = 200
            return response
    except Exception as e: 
        url = "http://octopart.com/api/v3/parts/search"
        url += "?apikey=" 
        url += "&include[]=imagesets"
        ## url += "&include[]=descriptions"
        url += "&include[]=datasheets"
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
        
            with open('ajax/query/' + part + '.json', 'w') as f:
                json.dump(search_response, f, indent=4, sort_keys=True)
                    
            response = JsonResponse({"success": "online"})
            response.status_code = 200
            return response
            
        except Exception as e:
            response = JsonResponse({"error": e})
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
def transcribe_file(speech_file):
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
        sample_rate_hertz=16000,
        language_code='en-US')
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    response = client.recognize(config, audio)
    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    ret = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        ret.append(format(result.alternatives[0].transcript))
    return ret
    # [END speech_python_migration_sync_response]
    # [END speech_transcribe_sync]