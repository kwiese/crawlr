from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import datetime
import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# from calculate import start_chain
from crawlr.form_info import form_constraints
from crawlr.models import Feedback

# from log import log

def home(request):
    context = {}
    context["is_authenticated"] = False
    if request.session.has_key('username') or request.user.is_authenticated:
        context["is_authenticated"] = True
    template = 'index_home.html'
    return render(request, template, {'context': context})

def login(request):
    if request.session.has_key('username') or request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        print("in post")
        data = request.POST
        print(data["email"])
        if User.objects.filter(username=data["email"]).exists():
            hasher = PBKDF2PasswordHasher()
            req_user = User.objects.get(username=data["email"])
            if req_user.username == data["email"] and req_user.password == hasher.encode(password= data['password'], salt="salt", iterations=1000):
                print("Authenticated!")
                request.session['username'] = data["email"]
                return redirect("/")
            else:
                print("boo")
    template = 'login.html'
    return render(request, template)

def signup(request):
    if request.session.has_key('username') or request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        data = request.POST
        if User.objects.filter(username=data["email"]).exists():
            print("exists")
        else:
            hasher = PBKDF2PasswordHasher()
            user = User(username=data["email"], first_name=data["firstname"], last_name=data["lastname"], email=data["email"], date_joined=timezone.now())
            user.password = hasher.encode(password= data['new-password'], salt="salt", iterations=1000)
            user.save()
            request.session['username'] = data["email"]
            return redirect("/")

    template = 'signup.html'
    return render(request, template)

def logout(request):
    if request.session.has_key('username') or request.user.is_authenticated:
        auth_logout(request)
    return redirect('/')

#@login_required
def application(request):
    # if this is a POST request we need to process the form data
    if not (request.session.has_key('username') or request.user.is_authenticated):
        return redirect("/login")
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
