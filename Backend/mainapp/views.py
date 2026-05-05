from django.shortcuts import render

# Create your views here.

def homeView(request):
    template = 'mainapp/home.html'

    return render(request=request, template_name=template, context={})