from django.shortcuts import render
from django.http import HttpResponse
from .application import prediction
from .application import training
from dotenv import load_dotenv
from os.path import join, dirname
from .forms import trainingForm
from datetime import datetime

import os

# Create your views here.
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

#contact view rendering contact.html page
def contact(request):
    index_file_path = PROJECT_PATH + '\pages\contact.html'
    return render(request,index_file_path)

#about view rendering about.html page
def about(request):
    index_file_path = PROJECT_PATH + '\pages\\about.html'
    return render(request,index_file_path)

#default view rendering home.html page
def home(request):
    index_file_path = PROJECT_PATH + '\pages\home.html'
    return render(request,index_file_path)

#predict view rendering predict.html page
def predict(request):
    index_file_path = PROJECT_PATH + '\pages\predict.html'
    return render(request, index_file_path)

#train view rendering train.html page along with trainingform controls
def train(request):
    context = {}
    output = ''

    if request.POST:
        try:
            form = trainingForm(request.POST, request.FILES)
            print(request.POST)
            print(request.FILES)
            if form.is_valid():
                files = request.FILES.getlist('excel_path')
                for i in files:
                    if not (i.name.endswith('.xls') or i.name.endswith('.xlsx')):
                        raise AttributeError()
                output = training.train(files)
                if output.__contains__("error"):
                    context['style'] = 'style=color:red;'
                else:
                    context['style'] = 'style=color:#2BD6B4;'
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        print(f"Field '{field}' : {error}")
                raise AttributeError()

        except AttributeError:
            output = "There is an error with the supplied files. Please supply excel files only"
            print(output)
            context['style'] = 'style=color:red;'
        except:
            output = "There is an error in the processing. Please contact the site owner"
            context['style'] = 'style=color:red;'
    form = trainingForm()
    context['form'] = form
    context['output']=output
    index_file_path = PROJECT_PATH + '\pages\\train.html'
    return render(request, index_file_path, context)


#Ajax call in prediction to be invoked from predict.html page
def call_isr(req):
    output = ''
    if req.method == 'GET' and req.GET.get('action') == 'predict':
        param1 = req.GET.get('short_desc')
        param2 = req.GET.get('top_n_results')
        try:
            if param2 != "":
                out = prediction.predict(param1,True,param2)
            else:
                out = prediction.predict(param1,True)
        except:
            output = "There is an error in the processing. Please contact the site owner"
            return HttpResponse(output)

        """Setup to read env file for various parameters"""
        dotenv_path = join(dirname(__file__), 'application\\var.env')
        load_dotenv(dotenv_path)

        """Read Parameters from env file"""
        delimiter = os.getenv('delimiter')

        if len(out) > 1:
            for o in out:
                print(o)
                output = output + "Record No. " + str(out.index(o) + 1) + '</br></br>'
                print(output)
                o = o.replace(delimiter, "</br></br>")
                output = output + o + "</br></br>" + \
                         "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" + \
                         "</br>"
        elif len(out) == 1 and (out[0] != "No Suitable Match Found" or out[0] != "There is an error in the processing. Please contact the site owner"):
            output = out[0].replace(delimiter, "</br></br>")
        else:
            output = out[0]

        return HttpResponse(output)
