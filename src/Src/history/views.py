from django.shortcuts import render

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

def history(request):	
        
    return render(request, 'history/history.html')
