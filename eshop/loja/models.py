from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Vendedor(models.Model):
    who = models.OneToOneField(User, on_delete=models.CASCADE) #generalizacao
    def __str__(self):
        return self.who.username

class Produto(models.Model):
    preco = models.IntegerField()
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300)
    personalizavel = models.BooleanField(default=False)
    pic = models.ImageField(upload_to='images', blank=True, null=True)
    seller = models.ForeignKey(Vendedor, on_delete=models.RESTRICT)

    def __str__(self):
        return self.nome



class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + ' disse: ' + self.text
class Questao(models.Model):
    texto = models.CharField(max_length=200)
    """ pub_data = models.DateTimeField('data de publicacao') """

    def __str__(self):
        return self.texto

    """ def foi_publicada_recentemente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)
 """

class QuestaoDoProduto(models.Model): #primary key composta
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
     
class Opcao(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    opcao_texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.opcao_texto

class OpcaoDaQuestaoProd(models.Model): #aqui é primary key composta, é uma ternária?
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    opcao = models.ForeignKey(Opcao, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

class Pedido(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    opcao = models.ForeignKey(Opcao, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)

