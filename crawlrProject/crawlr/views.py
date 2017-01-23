from django.shortcuts import render

def application(request):
    page = render(request, 'application.html')
    return page
