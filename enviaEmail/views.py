from django.http import HttpResponse
from django.shortcuts import render
from decouple import config
import smtplib
import email.message
from media.adrian.media.receitas import *

# Create your views here.


def envia_Email(emailcad,nome):
    subject = "Confirme sua conta"
    body = f'''Olá {nome},\nSeja bem vindo ao sistema
			de gerenciamento de listas de compras ADDLIST.\nPara finalizar o cadastro clique no link abaixo
			e siga as instruções:\nLINK FUTURO\nCaso tenha d
			úvidas entre em contato conosco pelo e-mail <EMAIL>.
			'''

    msg = email.message.Message()
    msg['Subject'] = subject
    msg['From'] = "COLOQUE_AQUI_O_EMAIL_DO_REMETENTE"
    msg['To'] = str(emailcad)
    password = 'bvylcstqotllgsns'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body)
    
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'],[msg['To']],msg.as_string().encode('utf-8'))





    