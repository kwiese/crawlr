from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# from calculate import start_chain
from crawlr.form_info import form_constraints
from crawlr.models import Feedback, CredentialsModel
# from log import log

def home(request):
    context = {}
    if not request.user.is_authenticated:
        template = 'index_home.html'
        return render(request, template, context)
    else:
        return redirect("/members")

def login(request):
    context = {}
    if not request.user.is_authenticated:
        template = 'login.html'
        return render(request, template, context)
    else:
        return redirect("/members")


def members(request):
    context = {}
    print(request.user.email)
    template = 'members.html'
    return render(request, template, context)

def logout(request):
    auth_logout(request)
    return redirect('/')

#@login_required
def application(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # log("starting collect....")
        data = request.POST
        #fb = Feedback(fb_neg=data["NegativeFeedback"], fb_pos=data["PositiveFeedback"], fb_date=datetime.datetime.now())
        #fb.save()
        # route_info = start_chain(data)
        # log("route_info received:")
        # log(route_info)
        # return JsonResponse(route_info)
    # log("fetched main page")
    return render(request, 'feedback.html', {'form_info': form_constraints})

##################################################################################
# from django.shortcuts import render
# from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, HttpResponse
# import os,sys
# import datetime
#
# import httplib2
# #from googleapiclient.discovery import build
# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from oauth2client.contrib import xsrfutil
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.contrib.django_util.storage import DjangoORMStorage
#
# sys.path.insert(1, os.path.join(sys.path[0], '..'))
# #from calculate import start_chain
# from crawlr.form_info import form_constraints
# from crawlr.models import Feedback, CredentialsModel
# from crawlrProject import settings
# #from log import log
#
# CLIENT_SECRETS = os.path.join(os.path.dirname(__file__),'..', 'client_secrets.json')
# FLOW = flow_from_clientsecrets(
#     CLIENT_SECRETS,
#     scope='https://www.googleapis.com/auth/plus.me',
#     redirect_uri='http://127.0.0.1:8000/oauth2callback')
#
# @login_required
# def index(request):
#     print(request.user.id)
#     storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
#     credential = storage.locked_get()
#     exit()
#     print("index")
#     print(credential)
#     if credential is None or credential.invalid == True:
#         FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user.id)
#         authorize_url = FLOW.step1_get_authorize_url()
#         return HttpResponseRedirect(authorize_url)
#     else:
#         return render(request, 'index_home.html')
#
# @login_required
# def auth_return(request):
#     #print(type(request.GET['state']))
#     if xsrfutil.validate_token(settings.SECRET_KEY, request.GET["state"].encode('utf-8'), request.user.id):
#         print("in deny")
#         return HttpResponseBadRequest()
#     credential = FLOW.step2_exchange(request.GET['code'])
#     print("ret")
#     print(request.user.id)
#     storage = DjangoORMStorage(CredentialsModel, 'id', request.user.id, 'credential')
#     storage.put(credential)
#     return HttpResponseRedirect("/")
#
# def application(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # log("starting collect....")
#         data = request.POST
#         #fb = Feedback(fb_neg=data["NegativeFeedback"], fb_pos=data["PositiveFeedback"], fb_date=datetime.datetime.now())
#         #fb.save()
#         # route_info = start_chain(data)
#         # log("route_info received:")
#         # log(route_info)
#         # return JsonResponse(route_info)
#     # log("fetched main page")
#     return render(request, 'feedback.html', {'form_info': form_constraints})
