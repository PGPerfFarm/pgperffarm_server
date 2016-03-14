from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist, loader, Context

import datetime

# Handle the static pages
def index(request):
        return render_to_response('index.html', {
        })