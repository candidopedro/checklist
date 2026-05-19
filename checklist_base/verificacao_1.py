import os
from datetime import datetime
from notificacao import mensagem_telegram
from gerenciador_diretorios import local_verificacao_1
from queries_handler import carregar_informacoes

def verificando_atualizacoes_judiciais():

    corpo_mensagem = "➭ 🔄 Verificando Alterações:\n"
    corpo_mensagem += ("\n")    

    mensagem_telegram(corpo_mensagem)

    #LOG
    data_atual = datetime.now().date()
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    horario_atual = datetime.now()
    nome_arquivo = f"consulta_atualiza_judiciais_{data_hora}.log"

    LOG_DIR = local_verificacao_1()
    caminho_arquivo = os.path.join(LOG_DIR, nome_arquivo)

    with open(caminho_arquivo, "a", encoding="utf-8") as f:
        f.write(f"🗓️ Verificação realizada: {data_atual} ({horario_atual.strftime('%H:%M:%S')})\n")
        f.write("\n" + "="*55 + "\n\n")
        # if (houver alteração escreva no script) 
        f.write("🟢 Nenhum erro foi encontado, execução foi bem-sucedida\n")
                    
        f.write("\n")        
        f.write("="*55)

    #return (o resultado da verficicação) 
verificando_atualizacoes_judiciais()