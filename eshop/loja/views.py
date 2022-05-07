from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import *
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

def index(request):
    return  HttpResponse(render(request, 'loja/main.html' ))

def loja(request):
    produtos = Produto.objects.all()
    prod1 = Produto(id=1, preco=40, nome="gar")
    prod2 = Produto(id=2, preco=50, nome="dois")
    lista_teste = {prod1, prod2}
    return render(request, 'loja/loja.html' , {'products_list': produtos})


def cart(request):
    return render(request, 'loja/cart.html' )

def checkout(request):
    return render(request, 'loja/checkout.html')

def detalheProd (request, produto_id):

    return render(request, 'loja/detalhesProd.html' , {'produto': produto_id})
    """ return  render(request, 'loja/checkout.html') """

def login1(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('loja:loja'))
        else:
            return HttpResponse("Erro ao logar Utilizador")
    else:
        return render(request, 'loja/login.html')

def logout1(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('loja:loja'))

    else:
        return HttpResponse("Erro no Logout do Utilizador feito ")

def register(request):
    if request.method=='POST': #falta aqui receber do form
        return HttpResponseRedirect(reverse('loja:loja'))
    else:
        return render(request,'loja/registo.html')

def criaProduto(request):
    if request.method == 'POST':
        nome = request.POST['novoP']
        descr = request.POST['desc']
        preco = request.POST['precoP']
        isPersonalizavel = request.POST['isPers']
        if isPersonalizavel == 'True':
            atributoPers = True
        else:
            atributoPers = False
        foto = request.FILES['fotoP']
        fs = FileSystemStorage()
        filename = fs.save(foto.name, foto)
        uploaded_file_url = fs.url(filename)

        vendedor= list(Vendedor.objects.filter(who=request.user.id))

        novoProduto= Produto(preco=preco, nome=nome, descricao=descr, personalizavel=atributoPers, pic=uploaded_file_url, seller=vendedor[0])
        novoProduto.save()
        return HttpResponse("Produto guardado!!!!!")
    else:
        questoes=Questao.objects.all()
        return render(request, "loja/criaProduto.html", {"questoes": questoes})

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
    