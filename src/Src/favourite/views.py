from django.shortcuts import render

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

def favourite(request):	
        
    return render(request, 'favourite/favourite.html')
