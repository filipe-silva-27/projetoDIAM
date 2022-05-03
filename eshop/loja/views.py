from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    return  HttpResponse(render(request, 'loja/main.html' ))

def loja(request):
    return  render(request, 'loja/loja.html' )

def cart(request):
    return  render(request, 'loja/cart.html' )

def checkout(request):
    return  render(request, 'loja/checkout.html')
