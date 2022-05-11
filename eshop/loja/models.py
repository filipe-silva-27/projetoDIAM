
from django.db import models

from django.contrib.auth.models import User

# Create your models here.

##SELLER
class Vendedor(models.Model):
    who = models.OneToOneField(User, on_delete=models.CASCADE) #generalizacao

    def __str__(self):
        return self.who.username


##Criaçãodde produto
class Produto(models.Model):
    preco = models.IntegerField()
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300)
    personalizavel = models.BooleanField(default=False)
    pic = models.ImageField(upload_to='images', blank=True, null=True)
    seller = models.ForeignKey(Vendedor, on_delete=models.RESTRICT)

    def __str__(self):
        return self.nome

class Questao(models.Model):
    texto = models.CharField(max_length=200)
    produto = models.ForeignKey(Produto ,on_delete=models.CASCADE)

    def __str__(self):
        return self.texto


class Opcao(models.Model): #é uma opcão de escolha de um produto é como um produto filtrado
    texto = models.CharField(max_length=200)
    questao = models.ForeignKey(Questao ,on_delete=models.CASCADE)
   
   
    def __str__(self):
        return self.texto




##nao toca no carrinho que ta a dar
class Cart(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ProdutoCarrinho')

    def valor_carrinho(self):
        lista_produtos = self.produtos.all()
        lista_info = ProdutoCarrinho.objects.filter(carrinho=self)
        iterar=zip(lista_produtos,lista_info)
        valor=0
        for produto,info in iterar:
            valor=valor+ (produto.preco*info.quantidade)
        return valor

    def items_carrinho(self):
        lista_info = ProdutoCarrinho.objects.filter(carrinho=self)
        val=0
        for quant in lista_info:
            val+=quant.quantidade
        return val

class ProdutoCarrinho(models.Model): # <--- through model
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantidade = models.IntegerField()









# class Comentario(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.CharField(max_length=500)
#     produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.user.username + ' disse: ' + self.text




