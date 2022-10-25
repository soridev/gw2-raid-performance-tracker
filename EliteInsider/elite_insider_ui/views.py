from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .forms import LoginForm

# Create your views here.

def login_view(request):
    
    if request.user.is_authenticated:
        return redirect(main)

    context = {}
    template = loader.get_template("elite_insider_ui/index.html")
    
    if request.method == "GET":
        return HttpResponse(template.render(context, request))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
            
            if user is not None:
                login(request, user)
                return redirect(main)

        context.update({'message': 'Invalid username / password.'})
        return HttpResponse(template.render(context, request))

def logout_view(request):
    
    logout(request)    
    return redirect(login_view)

def main(request):
    context = {}
    template = loader.get_template("elite_insider_ui/dashboard.html")

    return HttpResponse(template.render(context, request))


def guilds(request):
    context = {}
    template = loader.get_template("elite_insider_ui/guilds.html")

    return HttpResponse(template.render(context, request))
