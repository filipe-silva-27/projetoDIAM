from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *

def index(request):
    return  HttpResponse(render(request, 'loja/main.html' ))

def loja(request):
    produtos = Produto.objects.all()
    prod1 = Produto(id=1, preco=40, nome="gar")
    prod2 = Produto(id=2, preco=50, nome="dois")
    lista_teste = {prod1, prod2}
    return render(request, 'loja/loja.html' , {'products_list': lista_teste})

def cart(request):
    return render(request, 'loja/cart.html' )

def checkout(request):
    return render(request, 'loja/checkout.html')

def detalheProd (request, produto_id):
    return render(request, 'loja/detalhesProd.html' , {'produto': produto_id})