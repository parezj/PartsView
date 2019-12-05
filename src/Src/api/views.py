from django.shortcuts import render
from django.urls import include, path
    

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

def api(request):	
        
    return render(request, 'api/api.html')
