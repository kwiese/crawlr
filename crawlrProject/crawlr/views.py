from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
import os,sys
import datetime
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from calculate import start_chain
from crawlr.models import Feedback
from crawlr.form_info import form_constraints

from log import log

def application(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        log("starting collect....")
        data = request.POST
        #fb = Feedback(fb_neg=data["NegativeFeedback"], fb_pos=data["PositiveFeedback"], fb_date=datetime.datetime.now())
        #fb.save()
        route_info = start_chain(data)
        log("route_info received:")
        log(route_info)
        return JsonResponse(route_info)
    log("fetched main page")
    return render(request, 'application-new.html', {'form_info': form_constraints})
