from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from enviaEmail.views import *
#configuracoes do proprio django 
from django.contrib.auth.models import User
from django import forms

#para usuario autenticado
from django.contrib.auth import authenticate, login, logout

import datetime
# Create your views here.


#REDIRECIONA PARA PAGINA DE LOGIN
def page_login(request):
	return render(request,"index.html")

#REDIRECIONA PARA PAGINA DE CADASTRO
def page_cadastro(request):
	return render(request,"cadastro/cadastro.html")

#CRIA UM CADASTRO E REDIRECIONA PARA PAGINA DE LOGIN
def efetuar_Cadastro(request):
	nome = request.POST.get("name")
	emailcad = request.POST.get("email")
	senha = request.POST.get("password")
	confirmSenha = request.POST.get("password_repeat")
	
	user = User.objects.filter(username=nome).first()
	email = User.objects.filter(email=emailcad).first()

	if user:
		msg = {
			'msg': 'Usuário já cadastrado'
		}
		return render(request, "cadastro/cadastro.html", msg)
	elif email:
		msg = {
			'msg': 'E-mail já cadastrado'
			}
		return render(request, "cadastro/cadastro.html", msg)
	elif senha != confirmSenha:
		msg = {
			'msg': 'Senhas não conferem'
			}
		return render(request, "cadastro/cadastro.html", msg)
	else:
		try:
			envia_Email(emailcad=emailcad,nome=nome)
		
			user = User(
				username = User.first_name +''+ user.last_name,
				email = emailcad,
				password = senha,
				
			)
			user.save()
			
			
			msg = {
					'acao': 'Verifique seu email.',
					'msg': 'Usuário cadastrado com sucesso'
				}
			return render(request,'cadastro/cadastro_realizado.html',msg)
		except:
			msg ={
				'acao': 'Cadastrado não realizado, tente novamente!',
				'msg':'Não foi possível enviar a mensagem de confirmação.'
				}

			return render(request,'cadastro/cadastro_realizado.html',msg)
		

#VERIFICA SE O USUARIO EXISTE E SE EXISTIR REDIRECIONA PARA PAGINA MAIN/HOME
def efetuar_Login(request):
	username = request.POST.get('login')
	senha = request.POST.get('senha')
	

	user = authenticate(username=username, password=senha)
	

	if user:
		login(request,user)

		
		return redirect(page_home)
	else:
		return render(request,"index.html",{"msg": "Usuário ou senha incorretos"})
		
	
#LEVA PARA PAGINA DE PERFIL DO USUARIO
def page_perfil(request):
	if request.user.is_authenticated:
		userProfile = request.user.id
		user = User.objects.get(id = userProfile)
		listas = Lista.objects.filter(idUser = userProfile).count()
		produtos = Produto.objects.filter(idUser = userProfile).count()
		receitas = Receita.objects.filter(idUser = userProfile).count()
		mercados = Mercado.objects.filter(idUser = userProfile).count()

		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass
		context = {
			"usuario": user,
			'lista': listas,
			'receita': receitas,
			'mercado': mercados,
			'produto': produtos,
			}
		return render(request,"perfil/perfil.html", context)
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN PARA TER ACESSO A ESTÁ PAGINA')


#DESLOGA O USUARIO
def sair(request):
	logout(request)
	return render(request,"index.html")

#LEVA PARA PAGINA HOME
def page_home(request):
	if request.user.is_authenticated:
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass
		
		
		listas = Lista.objects.filter(idUser = iduser)

		context = {
			"listas": listas,
			"usuario": user,

		}
		
		return render(request,"home/home.html", context)
	
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN PARA TER ACESSO A ESTÁ PAGINA')


#-----------------------------
#-------- CRUD LISTA ---------
#-----------------------------
# OBS N COLOQUEI A FUNCAO PARA MOSTRAR TODAS AS LISTAS 
# POIS TODAS AS LISTAS ESTARÃO NA PAGINA HOME DA APLICAÇÃO

#LEVA PARA UMA LISTA EXPECIFICA
def page_lista(request,id):
	if request.user.is_authenticated:
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass

		#aqui pega uma lista e todas as suas informações
		try:
			lista = Lista.objects.filter(idUser = iduser).get(id = id)
			context = {
				"lista": lista,
				"usuario":user,
			
				}
			return render(request,"lista/lista.html",context)
		except Lista.DoesNotExist:
			return redirect(page_home)
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN PARA TER ACESSO A ESTÁ PAGINA') 

#LEVA PARA PAGINA DE ADICIONAR UMA NOVA LISTA
def page_adiciona_lista(request):
	if request.user.is_authenticated:
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass

		produtos = Produto.objects.filter(idUser = iduser)
		context = {
			"produtos": produtos,
			"usuario": user,
			}
		
		return render(request,"lista/adiciona_lista.html", context)
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN PARA TER ACESSO A ESTÁ PAGINA') 
	
#ADICIONA UMA NOVA LISTA
def adiciona_lista(request):
	if request.user.is_authenticated:
		nome = request.POST.get("titulo")
		descricao = request.POST.get("descricao")
		iduser = User.objects.get(id = request.user.id)
		produto_names = [x.nome for x in Produto.objects.all()]
		produto_ids = []
			
		for x in produto_names:
			produto_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("adrian")
				
		usuario = User.objects.get(id = request.user.id)
		lista = Lista.objects.create(
			nome = nome,
			descricao = descricao,
			idUser = usuario,
		)
		for x in produto_ids:
			lista.idproduto.add(Produto.objects.get(id=x))
		
		
		
		return redirect(page_home)
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN PARA TER ACESSO A ESTÁ PAGINA')

#LEVA PARA PAGINA DE EDITAR UMA LISTA EXPECIFICA	
def page_edita_lista(request,id):
	if request.user.is_authenticated:
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass


		lista = Lista.objects.get(id=id)

		produtos = lista.idproduto.all()
		produtos_ids = []
		for x in produtos:
			produtos_ids.append(x.id)

		produtosN = Produto.objects.filter(idUser=iduser).exclude(id__in=produtos_ids)

		data = {
			"lista": lista,
            "produtosN": produtosN,
	         "usuario": user,
            }
		return render(request, "lista/edita_lista.html", data)	
	else:
		return HttpResponse('EFETUE O LOGIN ANTES+')

#EDITA UMA LISTA EXPECIFICA
def lista_editada(request,id):
	if request.user.is_authenticated:
		updateLista = Lista.objects.get(id=id)
		updateLista.nome = request.POST.get("titulo")
		updateLista.descricao = request.POST.get("descricao")
		updateLista.idUser = User.objects.get(id = request.user.id)
		updateLista.data = datetime.datetime.now()
		produto_names = [x.nome for x in Produto.objects.all()]

			#produto_ids é referente ao html
		produto_ids = []
			#aqui o X vai pegar o valor la do html, tranformar para inteiro e jogar na lista produto_ids
		for x in produto_names:
			produto_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("adrian")
		print(produto_names)
		print(produto_ids)
		#aqui vai comparar os ids das tag html com os ids dos produtos		
		for x in produto_ids:
			#se id do html ja estiver na lista de ids de produtos
			if x in [x.id for x in updateLista.idproduto.all()]:	
				#remover idproduto			
				updateLista.idproduto.remove(Produto.objects.get(id=x))
			#se não estiver
			else:
				#adiciona idproduto a updateLista
				updateLista.idproduto.add(Produto.objects.get(id=x))
		
		updateLista.save()

		return redirect(page_home)
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN PARA TER ACESSO A ESTÁ PAGINA')

#DELETA UMA LISTA EXPECIFICA
def deleta_lista(request,id):
	if request.user.is_authenticated:
		deletaLista = Lista.objects.get(id=id)
		deletaLista.delete()
		return redirect(page_home)
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN PARA TER ACESSO A ESTÁ PAGINA')

#-----------------------------
#------- CRUD RECEITA --------
#-----------------------------


#FUNÇÃO PRA MOSTRAR TODAS AS RECEITAS NA TELA
def page_receitas(request):
	if request.user.is_authenticated:
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass

		receitas = Receita.objects.filter(idUser = iduser)
		return render(request,"receita/receitas.html",{"receitas":receitas, "usuario":user })
		
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN PARA TER ACESSO A ESTÁ PAGINA')

#FUNÇÃO PRA MOSTRAR UMA RECEITA EM ESPECIFICO
def page_receita(request,id):
	if request.user.is_authenticated:
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass

		try:
			receita = Receita.objects.filter(idUser = iduser).get(id = id)
			context = { 
				"receita": receita,
				"usuario": user,
			}
			return render(request, "receita/receita.html", context)
		except Receita.DoesNotExist:
			return redirect(page_receitas)
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN PARA TER ACESSO A ESTÁ PAGINA')

def add_ingredientes_a_lista(request,id):
	if request.user.is_authenticated:
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass



		receita = Receita.objects.filter(idUser = iduser).get(id = id)
		nomeReceita = receita.nome
		produto_names = receita.idproduto.all()
		
		usuario = User.objects.get(id = request.user.id)
		lista = Lista.objects.create(
				nome = f'Lista {nomeReceita}',
				descricao = f'COMRAR INGREDIENTES DA RECEITA {nomeReceita}',
				idUser = usuario,
			)
		
		for x in produto_names:
				lista.idproduto.add(receita.idproduto.get(id=x.id))
		context = {
			"receita": receita,
			#SE DER PROBLEMA NA HORA DE ADD PROD IN LIST MUDE ISSO
			"usuario": user,
		}

		return render(request, 'receita/receita.html', context)
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN')
				



#FUNÇÃO PRA ENVIAR O USUARIO A PAGINA DE ADICIONAR RECEITA JUNTO VAI DADOS SOBRE OS PRODUTOS
def page_adicionar_receita(request):
	if request.user.is_authenticated:
		produto = Produto.objects.filter(idUser = request.user.id )

		user = User.objects.get(id = request.user.id)

		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')

			user = " ".join(lista[0:space])
		except:
			pass

		context = { 
			"produto": produto,
			"usuario": user,
			}
		return render(request, "receita/adicionar_receita.html", context)
	else:
		return HttpResponse('VOCÊ NÃO ESTÁ LOGADO, FAÇA O LOGIN PARA TER ACESSO A ESTÁ PAGINA')
	
#FUNÇÃO PRA ADICIONAR UMA RECEITA
def add_receita(request):
	if request.user.is_authenticated:
		if request.method == "POST":

			titulo = request.POST.get("nome")
			imagem = request.FILES.get("imagem")
			
			mododepreparo = request.POST.get("mododepreparo")
		
			produto_names = [x.nome for x in Produto.objects.all()]
			produto_ids = []
			
			for x in produto_names:
				produto_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("adrian")
				
			usuario = User.objects.get(id = request.user.id)
			receita = Receita.objects.create(
				nome = titulo,
				image = imagem,
				modoPreparo = mododepreparo,
				idUser = usuario,
			)
			for x in produto_ids:
				receita.idproduto.add(Produto.objects.get(id=x))
			
			return redirect(page_receitas)
		else:
			msg = {
				"menssagem": "Não foi possivel adicionar receita, tente novamente!"
			}

			return render(request,"receita/adicionar_receita.html", msg)
	else:
		return redirect(page_login)

#FUNÇÃO PRA LEVAR À PAGINA DE EDITAR UMA RECEITA
def page_editar_receita(request,id):
	if request.user.is_authenticated:
		iduser =  request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass
		
		receita = Receita.objects.get(id=id)

		produtos = receita.idproduto.all()
		produtos_ids = []
		for x in produtos:
			produtos_ids.append(x.id)


		produtosN = Produto.objects.filter(idUser = iduser)

		
		data = {
			"receita":receita,
			"produtosN":produtosN,
			"usuario": user,
			}
		
		return render(request,"receita/editar_receita.html", data)
	else:
		return redirect(page_login)

#FUNCÃO PRA ATUALIZAR A RECEITA E RENDERIZAR A PAGINA COM A RECEITA EDITADA
def receita_editada(request,id):
	if request.user.is_authenticated:
		if request.method == "POST":
			
			titulo = request.POST.get("nome")
			mododepreparo = request.POST.get("mododepreparo",'')
			imagem = request.FILES.get("imagem")
			usuario = User.objects.get(id = request.user.id)

			receita = Receita.objects.get(id=id)

	
			receita.idUser = usuario
			if imagem:
				receita.image = imagem
			receita.nome = titulo
			receita.modoPreparo = mododepreparo
			
			produto_names = [x.nome for x in Produto.objects.all()]

			#produto_ids é referente ao html
			produto_ids = []
			#aqui o X vai pegar o valor la do html, tranformar para inteiro e jogar na lista produto_ids
			for x in produto_names:
				produto_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("adrian")
				
			#aqui vai comparar os ids das tag html com os ids dos produtos		
			for x in produto_ids:
				#se id do html ja estiver na lista de ids de produtos
				if x in [x.id for x in receita.idproduto.all()]:	
					#remover idproduto			
					receita.idproduto.remove(Produto.objects.get(id=x))
				#se não estiver
				else:
					#adiciona idproduto a receita
					receita.idproduto.add(Produto.objects.get(id=x))
			
			receita.save()

			return redirect(page_receitas)
		else:
			return render(request,"receita/adicionar_receita.html")
	else:
		return redirect(page_login)
	
#FUNÇÃO PRA EXCLUIR UMA RECEITA
def deleta_receita(request,id):
	if request.user.is_authenticated:

		receita = Receita.objects.get(id=id)
		receita.delete()
		return redirect(page_receitas)
	else:
		return redirect(page_login)

#-----------------------------
#------- CRUD MERCADO --------
#-----------------------------

#LEVA PARA PAGINA DE MERCADOS
def page_mercados(request):
	if request.user.is_authenticated:
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass

		mercados = Mercado.objects.filter(idUser = iduser)
		data = {
			"mercados":mercados,
			'usuario': user,
			}
		return render(request,"mercado/mercados.html", data)
	else:
		return redirect(page_login)

#LEVA PARA PAGINA DE ADICIONAR UM MERCADO
def page_adiciona_mercado(request):
	if request.user.is_authenticated:
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass
		context = {
			'usuario': user,
		}


		return render(request, "mercado/adicionar_mercado.html",context)
	else:
		return redirect(page_login)

#ADICIONA UM MERCCADO
def adiciona_mercado(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			mercado = request.POST.get("nome")
			endereco = request.POST.get("endereco")
			iduser = User.objects.get(id = request.user.id)

			Mercado.objects.create(nome=mercado,endereco=endereco, idUser=iduser)

			return redirect(page_home)
		else:
			return HttpResponse(f"Algo deu errado ao tentar cadastrar '{mercado}'")
	else:
		return redirect(page_login)
	
#VER MERCADO ESPECÍFICO
def page_mercado(request,id):
	if request.user.is_authenticated:
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass


		mercado = Mercado.objects.filter(idUser = iduser).get(id = id)
		#dps veja se ta funcionando certo na pagina de mercado 
		produtos = Produto.objects.filter(mercado = id).filter(idUser = iduser)
		data = {
			"mercado":mercado,
			"produtos":produtos,
			"usuario":user,
			}
		
		return render(request,"mercado/mercado.html", data)
	else:
		return redirect(page_login)

#LEVA PARA PAGINA DE EDITAR MERCADO
def page_edita_mercado(request,id):
	if request.user.is_authenticated:
		try:
			mercado = Mercado.objects.get(id=id)
			return render(request,"mercado/edita_mercado.html",{"mercado":mercado})
		except:
			return redirect(page_mercados)
	else:
		return HttpResponse("Efetue o login para editar um mercado")

#EDITA MERCADO
def mercado_editado(request,id):
	if request.user.is_authenticated:
		mercado = Mercado.objects.get(id=id)
		if request.method == "POST":
			form = Mercado(request.POST, instance=mercado)
			if form.is_valid():
				form.save()
				#pode ser que de erro aqui
				return redirect(page_mercado, id=id)
			else:
				return render(request,"mercado/edita_mercado.html", {"form":form})
		else:
			return render(request,"mercado/edita_mercado.html", {"form":form})
	else:
		return HttpResponse("Efetue o login para editar um mercado")

#DELETA UM MERCADO ESPECÍFICO
def deleta_mercado(request,id):
	if request.user.is_authenticated:
		mercado = Mercado.objects.get(id=id)
		mercado.delete()
		return redirect(page_mercados)
	else:
		return HttpResponse("Efetue o login para apagar um mercado")



#-----------------------------
#------- CRUD PRODUTO --------
#-----------------------------

#VER TODOS OS PRODUTOS
def page_produtos(request):
	if request.user.is_authenticated:
		iduser =  request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')

			user = " ".join(lista[0:space])
		except:
			pass

		produtos = Produto.objects.filter(idUser = iduser)
		data = {
			"produtos":produtos,
			"usuario": user,
			}
		return render(request,"produto/produtos.html", data)
	else:
		return redirect(page_login)

#VER UM PRODUTO ESPECÍFICO
def page_produto(request,id):
	if request.user.is_authenticated:
		produto = Produto.objects.get(id=id)
		user = User.objects.get(id = request.user.id)

		lista = []
		for i in user.username:
			lista.append(i)
		try:

			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass

		data = {
			"produto":produto,
	
			"usuario":user,
			}
		return render(request,"produto/produto.html", data)
	else:
		return redirect(page_login)

#LEVA PARA PAGINA DE ADICIONAR UM PRODUTO
def page_adiciona_produto(request):
	if request.user.is_authenticated:
		categoria = Categoria.objects.all()
		iduser = request.user.id
		user = User.objects.get(id = iduser)
		lista = []
		for i in user.username:
			lista.append(i)
		try:
			space = lista.index(' ')
			user = " ".join(lista[0:space])
		except:
			pass

		

		mercado = Mercado.objects.filter(idUser = iduser)
		data = {
			"categoria":categoria,
			"mercado":mercado,
			"usuario": user,
			
		}
		return render(request, "produto/adiciona_produto.html", data)
	else:
		return redirect(page_login)

#ADICIONA UM PRODUTO
def adiciona_produto(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			nomeProduto = request.POST.get("nomeProduto")
			iduser = User.objects.get(id = request.user.id)
			try:
				comparaProduto = Produto.objects.filter(idUser = iduser).filter(nome = nomeProduto)
				
			except Exception as e:
				pass
			if comparaProduto:

					return redirect(page_adiciona_produto)
			
			

			#será q da pra usar ?
			#preco = float(request.POST.get("preco"))

			imagem = request.FILES.get('imagem')
			preco = request.POST.get('preco')
			oferta = request.POST.get('oferta',"False")
			
	
			categoria = Categoria.objects.get(id = request.POST['categoria'])
			mercado = Mercado.objects.get(id = request.POST['mercado'])
			

			Produto.objects.create(
				nome=nomeProduto,
				image=imagem,
			  	categoria=categoria,
				mercado=mercado,
				preco=preco,
				oferta=oferta,
				idUser=iduser,
				
				)
			
			return redirect(page_produtos)
		else:
			return render(request,"produto/adiciona_produto.html")
	else:
		return redirect(page_login)

#LEVA PARA UM PRODUTO EXPECIFICO PARA SER EDITADO
def page_edita_produto(request,id):
	if request.user.is_authenticated:
		try:
			produto = Produto.objects.get(id=id)
			categoria = Categoria.objects.all()
			mercado = Mercado.objects.all()
			data = {
				"produto":produto,
				"categoria":categoria,
				"mercado":mercado,
				}
			return render(request,"produto/edita_produto.html", data)
		except:
			return redirect(page_produtos)
	else:
		return redirect(page_login)
	
#FUNÇÃO PARA EDITAR PRODUTO
def editar_produto(request,id):
	if request.user.is_authenticated:
		if request.method == "POST":
			nomeProduto = request.POST.get("nomeProduto","")
			preco = request.POST.get('preco')
			oferta = request.POST.get('oferta',"False")
			
			categoria = Categoria.objects.get(id = request.POST['categoria'])
			mercado = Mercado.objects.get(id = request.POST['mercado'])
			iduser = User.objects.get(id = request.user.id)
			produto = Produto.objects.get(id=id)
			produto.nome = nomeProduto
			produto.categoria = categoria
			produto.mercado = mercado
			produto.preco = preco
			produto.oferta = oferta
			produto.idUser = iduser
			produto.save()
			
			return redirect(page_home)
		else:
			return render(request,"produto/edita_produto.html")
	else:
		return redirect(page_login)

#DELETA UM PRODUTO ESPECÍFICO
def deleta_produto(request,id):
	if request.user.is_authenticated:
		produto = Produto.objects.get(id=id)
		produto.delete()
		return redirect(page_produtos)
	else:
		return redirect(page_login)