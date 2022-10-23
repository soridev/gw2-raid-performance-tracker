from curses.ascii import HT
from re import template
from django.http import HttpResponse
from django.template import loader
from yaml import load

# Create your views here.

def login(request):
    context = {}
    template = loader.get_template("elite_insider_ui/index.html")

    return HttpResponse(template.render(context, request))


def main(request):
    context = {}
    template = loader.get_template("elite_insider_ui/dashboard.html")

    return HttpResponse(template.render(context, request))


def guilds(request):
    context = {}
    template = loader.get_template("elite_insider_ui/guilds.html")

    return HttpResponse(template.render(context, request))
