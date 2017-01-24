from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ApplicationForm

def application(request):
    # if this is a POST request we need to process the form data
    form_class = ApplicationForm
    if request.method == 'POST':
        print("In post!")
        print(request.POST.get('username'))
        # create a form instance and populate it with data from the request:
        # form = form_class(data=request.POST)
        # # check whether it's valid:
        # if form.is_valid():
        #     #get data and call application
        #     start_address = form.cleaned_data['start_address']
        #     budget = form.cleaned_data['budget']
        #     search_radius = form.cleaned_data['search_radius']
        #     user_time = form.cleaned_data['user_time']
        return render(request, 'application-test.html')

            #redirect to results page?


    return render(request, 'application-test.html')

# def application(request):
#     page = render(request, 'application.html')
#     return page
