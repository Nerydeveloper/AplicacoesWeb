from django import forms
from django.db import models
from hashlib import sha256
from django.contrib.auth.models import User

def upload_image_receita(instance, filename):

    return f"{instance.idUser}/media/receitas/img/{filename}"

def upload_image_produto(instance, filename):

    return f"{instance.idUser}/produtos/img/{filename}"

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile_pics', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
  

    
class Categoria(models.Model):
    nome = models.CharField(max_length=45)

    def __str__(self):
        return self.nome


class Mercado(models.Model):
    nome = models.TextField(max_length=50)
    endereco = models.TextField(max_length=250, null=True, blank=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.nome} - {self.endereco}'

class Produto(models.Model):
    nome = models.TextField(max_length=50,default='Sem nome')
    categoria = models.ForeignKey(Categoria,on_delete=models.DO_NOTHING)
    mercado = models.ForeignKey(Mercado, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    oferta = models.BooleanField()
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_produto, blank=True, null=True)


    def __str__(self):
        return f'{self.image}'

# na views pegar o valor do preco e enviar para o historicoPreco

class HistoricoPreco(models.Model):
    historicoPreco = models.ForeignKey(Produto,on_delete=models.CASCADE)
    data = models.DateTimeField(auto_created=True, auto_now_add=True)
    
    def __str__(self):
        return f'{self.historicoPreco}'
    
class Lista(models.Model):
    nome = models.CharField(max_length=45, default='')
    descricao = models.TextField(max_length=520, blank=True, null=True)
    data = models.DateTimeField(auto_created=True, auto_now_add=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idproduto = models.ManyToManyField(Produto)

   
    def __str__(self):
        return f'{self.id} - {self.nome} - {self.data}'
    
class Receita(models.Model):
    nome = models.CharField(max_length=45)
    idproduto = models.ManyToManyField(Produto)
    ingredientes = models.TextField(max_length=1000, null=True, blank=True)
    modoPreparo = models.CharField(max_length=1000)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_receita, blank=True, null=True)
    
    def __str__(self):
        return f'{self.image}'


