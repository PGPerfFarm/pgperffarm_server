"""Views for the core PGPerfFarm app"""

from django.shortcuts import render_to_response
from django.template import RequestContext

import datetime


# Handle the static pages
def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))


def licence(request):
    return render_to_response('licence.html',
                              context_instance=RequestContext(request))


def ppolicy(request):
    return render_to_response('ppolicy.html',
                              context_instance=RequestContext(request))
