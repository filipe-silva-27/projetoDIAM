import re
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,permission_required, user_passes_test
from django.core.files.storage import FileSystemStorage

def index(request):
    return  HttpResponse(render(request, 'loja/main.html' ))

def loja(request):
    produtos = Produto.objects.all()
    return render(request, 'loja/loja.html' , {'products_list': produtos,'isvender': Vendedor.isVendedor(request.user)})
    #várias vezes enviamos isVendedor para templates que parece que não o usam, mas a razão foi: quando um template dá extend à navbar, os argumentos não são enviados para esta.                                                                        
    #Precisámos de enviar isvender para mostrar no dropdown o "Espaço Vendedor" só quando utilizador não está nágina Espaço Vendedor e SE utilizador for mesmo Vendedor

##CARINHO 
@login_required(login_url='loja:login1')
def cart(request):
    isVendedor = Vendedor.isVendedor(request.user)
    try:
        carrinho = Cart.objects.get(cliente=request.user)              
        pr = ProdutoCarrinho.objects.filter(carrinho=carrinho)          
        produtos = zip(carrinho.produtos.all(), pr)
        
        return render(request, 'loja/cart.html', {'carrinho':carrinho ,'produtos':produtos,'isvender':isVendedor})
    except Cart.DoesNotExist:
        return render(request, 'loja/cart.html',{'isvender': isVendedor})

@login_required(login_url='loja:login1')                                    #reutilizámos a variável produto_id para, se entrar no if do POST significa que se clicou no adicionar carrinho
def add_cart(request,produto_id):                                           #logo podemos ainda não ter ProdutoCarrinho e portanto precisamos de usar o id de Produto para criar/encontrar o ProdutoCarrinho
    especs=""                                                               #MAS SE entrar no else do POST significa que estamos a receber da view cart, onde já existe o ProdutoCarrinho, assim
    carrinho,created = Cart.objects.get_or_create(cliente=request.user)    #encontrámos uma forma eficiente de enviar como argumento o id do ProdutoCarrinho no qual se clicou (seta para baixo) para ultrapassar a dificuldade de ter um produto sem personalizacao
    if request.method == 'POST':             #para quando se dá submit com o botão "Adicionar ao Carrinho"                                                                                       
        produto = get_object_or_404(Produto, pk=produto_id)            
        for questao in Questao.objects.filter(produto_id=produto_id):                               #descricao da personalizacao com as questoes e opcoes                                                                         
            especs += str(questao)+": "+request.POST[str(questao.id)]+" \n" 

        if ProdutoCarrinho.objects.filter(produto=produto, carrinho=carrinho, opcs=especs).exists():  #se mesmo clicando no Adicionar ao Carrinho já houver um item igualzinho
            prodCart=ProdutoCarrinho.objects.get(produto=produto, carrinho=carrinho, opcs=especs)
            prodCart.quantidade = prodCart.quantidade+1
            prodCart.save()
        else:    
            add = ProdutoCarrinho(produto=produto, carrinho=carrinho, quantidade=1, opcs=especs)
            add.save()        
    else:                                                                                         #para quando se clica na seta para cima no carrinho e adiciona apenas quantidade
        prodCart = ProdutoCarrinho.objects.get(pk=produto_id)                                     
        prodCart.quantidade = prodCart.quantidade+1                 
        prodCart.save()
    return redirect('loja:cart')

@login_required(login_url='loja:login1')
def remove_cart(request,produto_id, btnDel):
    carrinho = Cart.objects.get(cliente=request.user) 
    produtoCarrinho = ProdutoCarrinho.objects.get(pk=produto_id)
    if (btnDel == 'false'):                                                     #para saber se retiramos o produto do carrinho ou diminuímos quantidade
        if carrinho.produtos.filter(id=produtoCarrinho.produto.id).exists():    #para reduzir a quantidade
            changes = ProdutoCarrinho.objects.get(pk=produto_id)
            if changes.quantidade == 1:                                         #se a quantidade for só 1 e tentar diminuir a quantidade, remove do carrinho
                produtoCarrinho.delete()
                return redirect('loja:cart')
            changes.quantidade = changes.quantidade-1                           #diminui a quantidade quando se clica na seta para baixo da quantidade (no carrinho)
            changes.save()
            return redirect('loja:cart')
    else:
        produtoCarrinho.delete()                                    #remove quando se clica em Remover no carrinho
        return redirect('loja:cart')


""" @login_required(login_url='loja:login1')
def remove_one(request,produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    carrinho = Cart.objects.get(cliente=request.user)
    if carrinho.produtos.filter(id=produto.id).exists(): #para reduzir a quantidade
        changes = ProdutoCarrinho.objects.get(produto=produto,carrinho=carrinho)
        if changes.quantidade == 1:
            return redirect('loja:cart')
        changes.quantidade = changes.quantidade-1
        changes.save()
        return redirect('loja:cart') """
##FIM CARRINHO

@login_required(login_url='loja:login1')
def checkout(request):                                              #carrega a página do checkout
    carrinho = Cart.objects.get(cliente=request.user)        
    return render(request, 'loja/checkout.html',{'cart':carrinho,'isvender': Vendedor.isVendedor(request.user)})


def detalheProd (request, produto_id):                              #pagina do detalhe do produto
    isVendedor = Vendedor.isVendedor(request.user)                  #é vendedor
    produto = get_object_or_404(Produto,id=produto_id)              #mas será vendedor DESTE produto?
    isVendedorProduto= (produto.seller.who.id==request.user.id)     #para saber se mostramos o adicionar ao carrinho ou apagar produto
    questoes=Questao.objects.filter(produto_id=produto_id)
    list=[]
    for questao in questoes:                                        #passa as questoes 
        list.append(Opcao.objects.filter(questao_id=questao.id))
    lista = zip(questoes,list)
    return render(request, 'loja/detalhesProd.html' , {'produto': produto,'isvender':isVendedorProduto,'perguntas':lista})
   
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

@login_required(login_url='loja:login1')
def logout1(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('loja:loja'))
    else:
        return HttpResponse("Erro no Logout do Utilizador feito ")

def register(request):
    if request.method=='POST':
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

@login_required(login_url='loja:login1')
def detailConta(request):
    if request.method == 'POST':
        company = request.POST['empresa']
        new_vender=Vendedor(who=request.user,empresa=company)
        new_vender.save()
        return redirect('loja:seller')
    else:
       
        return render(request,'loja/detalhesConta.html', {"isvender" : Vendedor.isVendedor(request.user)})

@user_passes_test(Vendedor.isVendedor, login_url='loja:loja')
def seller(request):                                                #carrega Espaço Vendedor
    vendedor = get_object_or_404(Vendedor, who=request.user)
    produtos_vendedor = Produto.objects.filter(seller=vendedor)
    return render(request,'loja/sellerpage.html', {'products_list': produtos_vendedor})

def search(request):                                                #faz pesquisa na barra de pesquisa
    pesquisa = request.GET.get('search')
    resultado = Produto.objects.filter(nome__icontains=pesquisa)

    return render(request, 'loja/loja.html' , {'products_list': resultado, 'isvender': Vendedor.isVendedor(request.user)})

def apagar(request, produto_id):                            #quando vendedor já não quer vender aquele produto
    produto = get_object_or_404(Produto, pk=produto_id)
    Produto.delete(produto)
    return redirect('loja:seller')




