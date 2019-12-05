from django.shortcuts import render

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

def part(request):	
        
    return render(request, 'part/part.html')
