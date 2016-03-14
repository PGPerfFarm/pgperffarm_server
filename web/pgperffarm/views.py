"""Views for the core PGPerfFarm app"""

from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist, loader, Context

import datetime

# Handle the static pages
def index(request):
        return render_to_response('index.html')
        
def licence(request):
        return render_to_response('licence.html')
        
def ppolicy(request):
        return render_to_response('ppolicy.html')