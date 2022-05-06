
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.contrib.auth.models import User

def index(request):
    return  HttpResponse(render(request, 'loja/main.html' ))

def loja(request):  
    return  render(request, 'loja/loja.html' )

def cart(request):
    return  render(request, 'loja/cart.html' )

def checkout(request):
    return  render(request, 'loja/checkout.html')

def login1(request):
    if request.method=='POST':
        return HttpResponseRedirect(reverse('loja:index'))
    else:
        return  render(request, 'loja/login.html')

def register(request):
    if request.method=='POST':
        return HttpResponseRedirect(reverse('loja:index'))
    else:
        return render(request,'loja/registo.html')