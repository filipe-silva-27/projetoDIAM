
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import *
from django.contrib.auth.models import User

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
    """ return  render(request, 'loja/checkout.html') """

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

""" 
def addCart(request, prod_id):
    prodAdicionar = Produto.objects.filter(id=prod_id)
    #se estiver logado: 
    carrinho = Cart.objects.filter(cliente=request.user)
    carrinho.adicionaAoCart(prodAdicionar)
    return HttpResponse("Yeahh")
    #else
    #return HttpResponseRedirect(reverse('loja:login1'))
     """
    