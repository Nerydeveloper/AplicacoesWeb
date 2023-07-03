
from django.urls import include, path
from .views import *

urlpatterns = [
    #INICIO NA TELA DE LOGIN
    path('', page_login, name='index'),


    #FUNÇÕES
    #LINK PARA ENTRAR NA CONTA
    path('home', efetuar_Login, name='entrar'),
    
    #LINK DE SAIR DA CONTA
    path('logout/', sair, name='logout'),

    #LINK PARA REALIZAR CADASTRO
    path('cadastro/', efetuar_Cadastro, name='cadastrar'),

    #LINKS PARA DIRECIONAR PARA PAGINA GERAL
    path('cadastro', page_cadastro, name='page_efetuar_cadastro'),
    path('addlist', page_home, name='home'),
    path('perfil', page_perfil, name='page_perfil'),
     
    #LINKS FUNCIONAIS DE VER
    #obs casso precise do id use a url com paremetro int:id
    path('lista/', page_lista, name='lista'),
    path('lista/<int:id>', page_lista, name='lista_id'),
    path('receita/<int:id>', page_receita, name='receita_id'),

    path('mercado/', page_mercado, name='mercado'),
    path('mercado/<int:id>', page_mercado, name='mercado_id'),

    path('produto/', page_produto, name='produto'),
    path('produto/<int:id>', page_produto, name='produto_id'),

    path('produtos/', page_produtos, name='produtos'),
    path('receitas/', page_receitas, name='receitas'),
    path('mercados/', page_mercados, name='mercados'),

    #LEVA PARA PAGINA DE ADICIONAR
    path('lista/adicionar', page_adiciona_lista, name="page_adiciona_lista"),
    path('receita/adicionar', page_adicionar_receita, name='page_adicionar_receita'),
    path('mercado/adicionar', page_adiciona_mercado, name='page_adiciona_mercado'),
    path('produto/adicionar', page_adiciona_produto, name='page_adiciona_produto'),

    #LINKS FUNCIONAIS DE ADICIONAR
    path('lista/add', adiciona_lista, name='adiciona_lista'),
    path('receita/add', add_receita, name='add_receita'),
    path('mercado/add', adiciona_mercado, name='adiciona_mercado'),
    path('produto/add', adiciona_produto, name='adiciona_produto'),
    path('receita/<int:id>/', add_ingredientes_a_lista, name='add_ingredientes_a_lista'),

    

    
    #LEVAR PARA PAGINA DE EDITAR
    path('produto/editar/<int:id>', page_edita_produto, name='page_editar_produto'),
    path('mercado/editar/<int:id>', page_edita_mercado, name='page_editar_mercado'),
    path('receita/editar/<int:id>', page_editar_receita, name='page_editar_receita'),
    path('lista/editar/<int:id>', page_edita_lista, name='page_editar_lista'),

    
    

    #LINKS FUNCIONAIS DE EDITAR
    path('receita/editar/<int:id>/', receita_editada, name='editar_receita'),
    path('lista/editar/<int:id>/', lista_editada, name='editar_lista'),
    path('mercado/editar', mercado_editado, name='editar_mercado'),
    path('produto/editar', editar_produto, name='editar_produto'),
    

    #LINKS FUNCIONAIS DE DELETAR
    path('lista/remover/<int:id>', deleta_lista, name='remover_lista'),
    path('receita/remover/<int:id>', deleta_receita, name='remover_receita'),
    path('mercado/remover/<int:id>', deleta_mercado, name='remover_mercado'),
    path('produto/remover/<int:id>', deleta_produto, name='remover_produto'),



    #dps veja pra que serve essa linha
    #path('login/', include('django.contrib.auth.urls')),

    #LINK PARA REALIZAR ALTERAÇÃO DE DADOS
    #path('alterar/', efetuar_Alteracao, name='alterar'),
    #LINK PARA REALIZAR ALTERAÇÃO DE DADOS
    #path('alterar_senha/', efetuar_Alteracao_Senha, name='alterar_senha'),
    #LINK PARA REALIZAR ALTERAÇÃO DE DADOS
    #path('alterar_email/', efetuar_Alteracao_Email, name='alterar_email'),
    #LINK PARA REALIZAR ALTERAÇÃO DE DADOS
    #path('alterar_telefone/', efetuar_Alteracao_Telefone, name='alterar_telefone'),
    #LINK PARA REALIZAR ALTERAÇÃO DE DADOS
    #path('alterar_endereco/', efetuar_Alteracao_Endereco, name='alterar_endereco'),
    #LINK PARA REALIZAR ALTERAÇÃO DE DADOS
    #...

]