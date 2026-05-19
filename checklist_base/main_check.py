# Limpeza e reestruturação  
# Objetivo: Enviar notificações (Email, telegram & --Whatsapp--) baseando-se nas informações extraidas de um banco de dados MySQL
# 
# Criar planilha via Pandas - NEW!!


import os
import re
from datetime import datetime
import time

from queries_handler import obter_processo_e_data
from soap_consulta import verificar_wsdl, consultar_processo
from notificacao import enviar_email, mensagem_telegram
from gerenciador_diretorios import log_monitoramento
from saudacoes_email import saudacao

LOG_DIR = log_monitoramento()

# ------------- LOG
def salvar_log(nome_arquivo, mensagens):
    caminho = os.path.join(LOG_DIR, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        for mensagem in mensagens:
            hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{hora}] {mensagem}\n\n")

def extrair_erros_do_log(texto_log):
    padrao = re.compile(
        r"🏛️ Tribunal\s*:\s*(\S+)\n"
        r"📌 Status\s*:\s*🔴 FALHA - (.+?)\n"
        r"📄 Tipo\s*:\s*(.+?)\n"
        r"📝 Detalhe\s*:\s*(.+?)\n"
    )
    return {
        sigla: f"{falha} - {tipo} - {detalhe}"
        for sigla, falha, tipo, detalhe in padrao.findall(texto_log)
    }

# ---------- Geração da mensagem
def gerar_mensagem_alerta(sigla, tipo, mensagem):
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return (
        f"🏛️ Tribunal : {sigla}\n"
        f"📌 Status   : 🔴 FALHA - {tipo}\n"
        f"📄 Tipo     : {tipo}\n"
        f"📝 Detalhe  : {mensagem}\n"
        f"🕒 Horário  : {horario}"
    )

def verificar_tribunal(tribunal_id, dados):
    sigla = dados['sigla']
    wsdl = dados['wsdl']
    horario = datetime.now().strftime("%d/%m/%Y %H:%M")

    status_ok, resposta_wsdl = verificar_wsdl(wsdl)
    conexao_wsdl = "🟢 Sucesso" if status_ok else "🔴 Falha"
    numero, data = obter_processo_e_data(tribunal_id)

    # --- Falha no WSDL
    if not status_ok:
        tipo = "WSDL indisponível"
        msg = str(resposta_wsdl)
        erro_msg = gerar_mensagem_alerta(sigla, tipo, msg)

        bloco = (
            f"🏛️ Tribunal : {sigla}\n"
            f"📜 CNJ      : {numero}\n"
            f"🔗 WSDL     : {wsdl}\n"
            f"🌐 Conexão  : {conexao_wsdl}\n"
            f"📌 Status   : 🔴 FALHA - {tipo}\n"
            f"📝 Detalhe   : {msg}\n"
            f"🕒 Horário  : {horario}"
        )
        return sigla, erro_msg, bloco

    # --- Sem processo disponível
    if not numero:
        bloco = (
            f"🏛️ Tribunal : {sigla}\n"
            f"🔗 WSDL     : {wsdl}\n"
            f"🌐 Conexão  : {conexao_wsdl}\n"
            f"📌 Status   : ⚠️ Sem processo disponível\n"
            f"🕒 Horário  : {horario}"
        )
        return sigla, None, bloco

    # --- Falha na consulta
    resposta, erro = consultar_processo(numero, dados)
    if erro:
        tipo = "Consulta falhou"
        msg = str(erro)
        erro_msg = gerar_mensagem_alerta(sigla, tipo, msg)

        bloco = (
            f"🏛️ Tribunal : {sigla}\n"
            f"📜 CNJ      : {numero}\n"
            f"🔗 WSDL     : {wsdl}\n"
            f"🌐 Conexão  : {conexao_wsdl}\n"
            f"📌 Status   : 🔴 FALHA - {tipo}\n"
            f"📝 Detalhe   : {msg}\n"
            f"🕒 Horário  : {horario}"
        )
        return sigla, erro_msg, bloco

    # --- Sucesso
    bloco = (
        f"🏛️ Tribunal : {sigla}\n"
        f"📜 CNJ      : {numero}\n"
        f"🔗 WSDL     : {wsdl}\n"
        f"🌐 Conexão  : {conexao_wsdl}\n"
        f"📌 Status   : 🟢 OK - Consulta realizada\n"
        f"📝 Processo : {numero}\n"
        f"🗓️ Data     : {data}\n"
        f"🕒 Horário  : {horario}"
    )
    return sigla, None, bloco

def verificar_todos_os_tribunais():
    print("\n" + "═" * 55)
    print("🔍 Verificando disponibilidade dos tribunais")
    print(f"\n🕒 Verificação iniciada: {datetime.now().strftime('%d/%m/%Y ás %H:%M:%S')}")
    print("═" * 55)


    alertas = []
    mensagens_finais = []
    blocos_por_tribunal = {}


    # --- Corpo do email / mensagem
    inicio_email = saudacao()
    corpo_mensagem = inicio_email + "Segue o status atualizado das consultas via MNI:\n\n"

    
if __name__ == "__main__" :
    while True:
        verificar_todos_os_tribunais()
        time.sleep(300)