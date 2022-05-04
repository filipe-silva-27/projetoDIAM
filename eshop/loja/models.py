from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Produto(models.Model):
    preco = models.IntegerField()
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300)
    personalizavel = models.BooleanField(default=False)
    pic = models.ImageField(upload_to='images', blank=True, null=True)
    seller = models.ForeignKey(Vendedor, on_delete=models.RESTRICT)

    def __str__(self):
        return self.nome
class Vendedor(models.Model):
    who = models.OneToOneField(User, on_delete=models.CASCADE) #generalizacao
    

class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)