# Limpeza e reestruturação  
# Objetivo: Enviar notificações (Email, telegram & --Whatsapp--) baseando-se nas informações extraidas de um banco de dados MySQL
# 
# Criar planilha via Pandas - NEW!!
# Padronização dos logs para APRIMORAMENTO da COMPARAÇÃO dos LOG's - NEW!!
# Implementação de Container - NEW!!

import os
import re
from datetime import datetime
import time

from soap_consulta import verificar_wsdl
from notificacao import enviar_email, mensagem_telegram
from gerenciador_diretorios import log_monitoramento
from saudacoes_email import saudacao

LOG_DIR = log_monitoramento()

# ------------- GERAR LOG/ COMPARAR 
#def salvar_log():


#def extrair_erros_do_log():

def verificar_itens():
    print("\n" + "═" * 55)
    print("🔍 Iniciando Verificação ")
    print(f"\n🕒 Verificação iniciada: {datetime.now().strftime('%d/%m/%Y ás %H:%M:%S')}")
    print("═" * 55)


    alertas = []
    mensagens_finais = []
    blocos_por_tribunal = {}


    # --- Corpo do email / mensagem
    inicio_email = saudacao()
    corpo_mensagem = inicio_email

    
if __name__ == "__main__" :
    while True:
        verificar_itens()
        time.sleep(300)