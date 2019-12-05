from django.shortcuts import render

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

def about(request):	
        
    return render(request, 'about/about.html')
