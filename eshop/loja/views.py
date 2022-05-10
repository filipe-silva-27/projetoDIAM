import re
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

def index(request):
    return  HttpResponse(render(request, 'loja/main.html' ))

def loja(request):
    produtos = Produto.objects.all()
    return render(request, 'loja/loja.html' , {'products_list': produtos})

##CARINHO 
@login_required(login_url='loja:login1')
def cart(request):
    try:
        carrinho = Cart. objects.get(cliente=request.user)
        pr = ProdutoCarrinho.objects.filter(carrinho=carrinho)
        produtos = zip(carrinho.produtos.all(), pr)
        return render(request, 'loja/cart.html', {'carrinho':carrinho ,'produtos':produtos })
    except Cart.DoesNotExist:
        return render(request, 'loja/cart.html')

@login_required(login_url='loja:login1')
def add_cart(request,produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    carrinho,created = Cart.objects.get_or_create(cliente=request.user)
    if carrinho.produtos.filter(id=produto.id).exists():
        changes = ProdutoCarrinho.objects.get(produto=produto,carrinho=carrinho)
        changes.quantidade = changes.quantidade+1
        changes.save()
        return redirect('loja:cart')
    add = ProdutoCarrinho( produto=produto,
    carrinho=carrinho,
    quantidade=1)
    add.save()
    return redirect('loja:cart')

@login_required(login_url='loja:login1')
def remove_cart(request,produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    carrinho = Cart.objects.get(cliente=request.user) 
    carrinho.produtos.remove(produto)
    return redirect('loja:cart')

@login_required(login_url='loja:login1')
def remove_one(request,produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    carrinho = Cart.objects.get(cliente=request.user)
    if carrinho.produtos.filter(id=produto.id).exists():
        changes = ProdutoCarrinho.objects.get(produto=produto,carrinho=carrinho)
        if changes.quantidade == 1  :
            return redirect('loja:cart')
        changes.quantidade = changes.quantidade-1
        changes.save()
        return redirect('loja:cart')
##FIM CARRINHO

def checkout(request):
    carrinho = Cart.objects.get(cliente=request.user)
    return render(request, 'loja/checkout.html',{'cart':carrinho})

def detalheProd (request, produto_id):
    produto = Produto.objects.filter(id=produto_id).first()
    return render(request, 'loja/detalhesProd.html' , {'produtoID': produto_id, 'produto': produto})
   
#login/registo/lougout
def login1(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loja:loja'))
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
        username= request.POST['username']
        email=request.POST['email']
        password= request.POST['psw']
        User.objects.create_user(username=username,email=email,password=password)
        return HttpResponseRedirect(reverse('loja:loja'))
    else:
        return render(request,'loja/registo.html')

##Fim


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

        vendedor= Vendedor.objects.filter(who=request.user.id).first() #não testado

        novoProduto= Produto(preco=preco, nome=nome, descricao=descr, personalizavel=atributoPers, pic=uploaded_file_url, seller=vendedor)
        novoProduto.save()
        
        for questEscolhID in request.POST['questoes']:
            questEscolhida = Questao.objects.filter(id=questEscolhID).first()
            opcaoEsco = Opcao(texto="amarelo", produto=novoProduto, questao=questEscolhida)
            opcaoEsco.save()

        return HttpResponse("Produto guardado!!!!!")
    else:
        questoes=Questao.objects.all()
        return render(request, "loja/criaProduto.html", {"questoes": questoes})

def seller(request):
    return render(request,'loja/sellerpage.html')