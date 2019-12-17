from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def home(request):
    return render(request, 'basic/home.html')
    
def handler404(request, *args, **argv):
    response = render_to_response('basic/404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'basic/home.html')
        else:
            return render(request, 'basic/login.html', {'fail': 1})
    else:
        return render(request, 'basic/login.html', {'fail': 0})
        
        
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return render(request, 'basic/home.html')
        else:
            return render(request, 'basic/register.html', {'form': form, 'fail': 1})
    else:
        form = UserCreationForm()
    return render(request, 'basic/register.html', {'form': form, 'fail': 0})