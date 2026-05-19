import os
import time
import smtplib
from datetime import datetime
from collections import Counter
from enderecos_email_pdf import lista_emails_pdf
from notificacao import mensagem_telegram
from gerenciador_diretorios import local_estimativa_de_email

#variaveis globais

def validacao_emails_e_tempo_de_envio():
    with smtplib.SMTP("smtp.pge.rj.gov.br", 25) as server:
        inicio_teste_envio = time.time()
        server.ehlo() 
        server.mail("candidop@pge.rj.gov.br")

        email_validos = 0
        email_invalidos = ""
        for email in lista_emails_pdf:
            code, message = server.rcpt(email)
            if code in (250, 251):
                email_validos += 1
            else:
                email_invalidos += f"✘ Recusado: {email} (código {code}, mensagem {message.decode(errors='ignore')})\n\n"
                resultado_verificacao_smtp = (email_invalidos)

        if email_validos == len(lista_emails_pdf):
            resultado_verificacao_smtp = ("✓ Todos emails cadastrados são válidos\n\n")
        fim_teste_envio = time.time()

        tempo_de_envio = f"{(fim_teste_envio-inicio_teste_envio):.2f}"

    return resultado_verificacao_smtp, tempo_de_envio

def verificando_estimativa_de_email():
    quantidade_de_emails_cadastrados = len(lista_emails_pdf)
    data_e_hora = datetime.now().strftime("%d/%m/%y ás %H:%M")
    emails_validados, tempo_de_envio_emails = validacao_emails_e_tempo_de_envio()

    corpo_mensagem = f"\n➭ Estimativa de E-mail - {data_e_hora}\n"
    corpo_mensagem += ("="*22 +"\n")
    corpo_mensagem +="\n"
    corpo_mensagem += f"➭ Total de destinatários: {quantidade_de_emails_cadastrados}\n"

    #Validação via SMTP dos emails
    corpo_mensagem += emails_validados

    #Emails Duplicados
    contador = Counter(lista_emails_pdf)
    duplicados = [item for item, count in contador.items() if count > 1]
    if duplicados:
        corpo_mensagem += "➭ Detecção de Duplicados:\n\n"
        for emails in duplicados:
            corpo_mensagem += f"- {emails}\n"
    else: 
        corpo_mensagem += "➭ Sem emails duplicados\n"

    #Tempo de envio
    corpo_mensagem +="\n"
    corpo_mensagem += f"➭ Tempo estimado: {(tempo_de_envio_emails)} segundos\n\n"
    corpo_mensagem += ("="*22 +"\n")

    mensagem_telegram(corpo_mensagem)
    print (corpo_mensagem)

def obter_lista_estimativa_email():
    quantidade_de_emails_cadastrados = len(lista_emails_pdf)
    emails_validados, tempo_de_envio_emails = validacao_emails_e_tempo_de_envio()

    #Emails Duplicados
    contador = Counter(lista_emails_pdf)
    duplicados = [item for item, count in contador.items() if count > 1]
    if duplicados:
        existe_emails_duplicados = "Detecção de Duplicados:\n\n"
        for emails in duplicados:
            existe_emails_duplicados += f"- {emails}\n"
    else: 
        existe_emails_duplicados = "Sem emails duplicados\n"

    validacao_emails = []
    
    validacao_emails.append({
        "Total de destinatários": quantidade_de_emails_cadastrados,
        "Validação de emails": emails_validados,
        "Emails duplicados": existe_emails_duplicados,
        "Tempo de envio (segundos)": tempo_de_envio_emails
    })

    #LOG
    data_atual = datetime.now().date()
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    horario_atual = datetime.now()
    nome_arquivo = f"estimativa_email_{data_hora}.log"

    LOG_DIR = local_estimativa_de_email()
    caminho_arquivo = os.path.join(LOG_DIR, nome_arquivo)

    with open(caminho_arquivo, "a", encoding="utf-8") as f:
        f.write(f"🗓️ Verificação realizada: {data_atual} ({horario_atual.strftime('%H:%M:%S')})\n")
        f.write("\n" + "="*50 + "\n")

        quantidade_de_emails_cadastrados = len(lista_emails_pdf)
        f.write("\n")
        f.write(f"➭ Total de destinatários: {quantidade_de_emails_cadastrados}\n")
        
        #Verificando se há e-mails inválidos
        emails_validados, tempo_de_envio_emails = validacao_emails_e_tempo_de_envio()
        f.write("\n")
        f.write(f"➭ Validação de E-mails: {emails_validados}")
        
        #Emails Duplicados
        contador = Counter(lista_emails_pdf)
        duplicados = [item for item, count in contador.items() if count > 1]
        if duplicados:
            f.write("➭ Detecção de Duplicados:\n\n")
            for emails in duplicados:
                f.write(f"- {emails}\n")
        else: 
            f.write("➭ Sem emails duplicados\n")

        #Tempo de envio
        f.write("\n")
        f.write(f"➭ Tempo estimado: {(tempo_de_envio_emails)} segundos\n\n")
        f.write("="*50 + "\n")

    return validacao_emails