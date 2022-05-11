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

@login_required(login_url='loja:login1')
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
    isvender=Vendedor.objects.filter(who=request.user).exists()
    vendedor = get_object_or_404(Vendedor, who=request.user)
    produtos_vendedor = Produto.objects.filter(seller=vendedor)
    return render(request, 'loja/detalhesProd.html' , {'produtoID': produto_id, 'produto': produto,'isVendedor':isvender, 'listadoVend': produtos_vendedor})


   
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
            error_message = "Your username or password may be incorrect" 
            return render(request, 'loja/login.html',{'error_message': error_message})
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
        isSeller = request.POST.get("isVendedor", None)

        return HttpResponseRedirect(reverse('loja:loja'))
    else:
        return render(request,'loja/registo.html')

##Fim


def criaProduto(request):
    if request.method == 'POST':
        ##Buscar_foto
        foto = request.FILES['fotoP']
        fs = FileSystemStorage()
        filename = fs.save(foto.name, foto)
        uploaded_file_url = fs.url(filename)
        ##fim
        ##dados_base
        nome = request.POST['novoP']
        descr = request.POST['desc']
        preco = request.POST['precoP']
        isPersonalizavel = request.POST.get("isPers", None)
        vendedor= get_object_or_404(Vendedor,who=request.user.id) 
    
        ##fim
        if isPersonalizavel is None :
             atributoPers = False
        else:
            atributoPers = True

        novoProduto= Produto(preco=preco, nome=nome, descricao=descr, personalizavel=atributoPers, pic=uploaded_file_url, seller=vendedor)
        novoProduto.save()



      
        if atributoPers==True :
            perguntas = request.POST.getlist('questao')
            i=0
            for pergunta in perguntas:
                i+=1
                quest = Questao(texto=pergunta,produto=novoProduto)
                quest.save()
                ops = request.POST.getlist('questao_'+str(i))
                for opcao in ops:
                    new_op = Opcao(texto=opcao,questao=quest)
                    new_op.save()
            return redirect('loja:seller')
        else:
            return redirect('loja:seller')
    else:
        questoes=Questao.objects.all()
        return render(request, "loja/criaProduto.html", {"questoes": questoes})

def detailConta(request):
    if request.method == 'POST':
<<<<<<< HEAD
        return redirect('loja:seller')
=======
        nomeEmpresa=request.POST['empresa']
        novoVendedor = Vendedor(who=request.user, empresa=nomeEmpresa)
        novoVendedor.save()
        return HttpResponseRedirect(reverse('loja:loja'))
>>>>>>> d42477051b39d7a61910b6b8065225d24be4c7ad
    else:
        isVendedor = Vendedor.objects.filter(who=request.user).exists()
        return render(request,'loja/detalhesConta.html', {"isVendedor" : isVendedor})


def seller(request):
    vendedor = get_object_or_404(Vendedor, who=request.user)
    produtos_vendedor = Produto.objects.filter(seller=vendedor)
    return render(request,'loja/sellerpage.html', {'products_list': produtos_vendedor})

def search(request):
    pesquisa = request.GET.get('search')
    resultado = Produto.objects.filter(nome__icontains=pesquisa)
    return render(request, 'loja/loja.html' , {'products_list': resultado})

def apagar(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    Produto.delete(produto)
    return redirect('loja:seller')




