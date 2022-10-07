from django.http import HttpResponse
from django.template import loader

# Create your views here.


def main(request):
    context = {}
    template = loader.get_template("elite_insider_ui/dashboard.html")

    return HttpResponse(template.render(context, request))


def guilds(request):
    context = {}
    template = loader.get_template("elite_insider_ui/guilds.html")

    return HttpResponse(template.render(context, request))
