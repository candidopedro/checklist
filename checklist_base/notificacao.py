# mensagens_alerta.py
import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from enderecos_email_pdf import lista_emails_pdf
from enderecos_email import lista_emails
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# WHATSAPP - DESATIVADO

# TELEGRAM
def mensagem_telegram(corpo):
    print(" "*15 , "🤖 Enviando notificação via Telegram...")

    TOKEN = '7825831398:AAGXvmrUH1b0vAxMNNLf_ux-3p9cjvwk3qU'
    CHAT_ID = '-1002625784842'
    MAX_LENGTH = 4096

    def enviar_parte(texto):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": texto
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"{' '*10}✅ Parte da mensagem enviada com sucesso via Telegram.")
        else:
            print(f"{' '*12}⚠️ Erro ao enviar notificação via Telegram. Código: {response.status_code}")
            print("Resposta da API:", response.text)

    if len(corpo) <= MAX_LENGTH:
        enviar_parte(corpo)
    else:
        print(f"{' '*12}⚠️ Mensagem muito longa. Enviando em partes...")
        for i in range(0, len(corpo), MAX_LENGTH):
            parte = corpo[i:i + MAX_LENGTH]
            enviar_parte(parte)

#TELEGRAM - PDF
def enviar_pdf_telegram(caminho_pdf, legenda=None):
    print(f"{' '*20}📄 Enviando PDF via Telegram...")

    TOKEN = '7825831398:AAGXvmrUH1b0vAxMNNLf_ux-3p9cjvwk3qU'
    CHAT_ID = '-1002625784842'
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"

    with open(caminho_pdf, 'rb') as pdf_file:
        files = {'document': (os.path.basename(caminho_pdf), pdf_file)}
        data = {
            'chat_id': CHAT_ID,
            'caption': legenda or 'Checklist Diário',
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        print(f"{' '*18}✅ PDF enviado com sucesso via Telegram.\n")
    else:
        print(f"{' '*12}⚠️ Erro ao enviar PDF. Código: {response.status_code}")
        print("Resposta da API:", response.text)

# EMAIL
def enviar_email(assunto, corpo):
    remetente = 'candidop@pge.rj.gov.br'

    try:
        server = smtplib.SMTP('smtp.pge.rj.gov.br', 25)
        for destinatario in lista_emails:
            mensagem = MIMEMultipart()
            mensagem['From'] = remetente
            mensagem['To'] = destinatario
            mensagem['Subject'] = assunto
            mensagem.attach(MIMEText(corpo, 'plain'))
            server.sendmail(remetente, destinatario, mensagem.as_string())
            print(f"{' '*12}✅ E-mail enviado para {destinatario}")
        server.quit()
    except Exception as e:
        print(f"{' '*12}⚠️ Falha ao enviar e-mail: {e}\n")
        
#PDF POR EMAIL
def enviar_pdf_email(assunto, corpo, caminho_pdf):
    remetente = 'candidop@pge.rj.gov.br'

    if not os.path.exists(caminho_pdf):
        print(f"{' '*12}⚠️ Arquivo PDF não encontrado: {caminho_pdf}")
        return
    
    try:
        server = smtplib.SMTP('smtp.pge.rj.gov.br', 25)
        server.ehlo()

        for destinatario in lista_emails_pdf:
            mensagem = MIMEMultipart()
            mensagem['From'] = remetente
            mensagem['To'] = destinatario
            mensagem['Subject'] = assunto

            mensagem.attach(MIMEText(corpo, 'plain'))

            # Anexa PDF com tipo MIME correto
            with open(caminho_pdf, "rb") as anexo_pdf:
                part = MIMEBase('application', 'pdf')
                part.set_payload(anexo_pdf.read())
                encoders.encode_base64(part)
                
                # Nome do arquivo no email
                data_hora = datetime.now().strftime("%d_%m_%Y-%H-%M")
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="Report Checklist - {data_hora}.pdf"'
                )
                mensagem.attach(part)

            server.sendmail(remetente, destinatario, mensagem.as_string())
            print(f"{' '*12}✅ E-mail enviado com PDF para {destinatario}")

        server.quit()
        print(f"{' '*18}📤 Todos os e-mails enviados com sucesso.\n")

    except Exception as e:
        print(f"{' '*12}⚠️ Falha ao enviar e-mail: {e}\n")