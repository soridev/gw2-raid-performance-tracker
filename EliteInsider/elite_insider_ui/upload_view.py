from re import template
from django.http import HttpResponse
from django.template import loader


def upload(request):
    context = {}
    template = loader.get_template("elite_insider_ui/upload.html")

    return HttpResponse(template.render(context, request))
