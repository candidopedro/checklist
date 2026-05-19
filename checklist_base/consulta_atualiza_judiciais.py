import os
from datetime import datetime
from notificacao import mensagem_telegram
from gerenciador_diretorios import log_atualiza_judiciais
from queries_handler import (obter_processos_judiciais_com_avisos_consumidos, 
obter_processos_originarios_com_data_entrada_nula_ou_desatualizada, obter_processos_vinculados_com_data_entrada_nula_ou_desatualizada)

def verificando_atualizacoes_judiciais():
    com_avisos_consumidos = obter_processos_judiciais_com_avisos_consumidos()
    originarios_com_data_entrada_nula_ou_desatualizada = obter_processos_originarios_com_data_entrada_nula_ou_desatualizada()
    vinculados_com_data_entrada_nula_ou_desatualizada = obter_processos_vinculados_com_data_entrada_nula_ou_desatualizada()

    corpo_mensagem = "➭ 🔄 Verificando Atualizações Judiciais:\n"
    corpo_mensagem += ("\n")    
    if (com_avisos_consumidos and originarios_com_data_entrada_nula_ou_desatualizada and vinculados_com_data_entrada_nula_ou_desatualizada) == 0:
        corpo_mensagem += "🟢 Nenhum erro foi encontado, execução foi bem-sucedida.\n"
    
    else:
        if com_avisos_consumidos:
            corpo_mensagem += "🚨 Alerta:\n"
            corpo_mensagem += f"- Identificados {com_avisos_consumidos[0]['Nenhum nome de coluna']} processos judiciais com avisos consumidos.\n"
        if originarios_com_data_entrada_nula_ou_desatualizada:
            corpo_mensagem += "🚨 Alerta: \n"
            corpo_mensagem += f"- Identificados {originarios_com_data_entrada_nula_ou_desatualizada[0]['Nenhum nome de coluna']}processos originários com data_entrada nula ou desatualizada.\n"
        if vinculados_com_data_entrada_nula_ou_desatualizada:
            corpo_mensagem += "🚨 Alerta: \n"
            corpo_mensagem += f"- Identificados {originarios_com_data_entrada_nula_ou_desatualizada[0]['Nenhum nome de coluna']} processos vinculados com data_entrada nula ou desatualizada.\n"        

    mensagem_telegram(corpo_mensagem)

    #LOG
    data_atual = datetime.now().date()
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    horario_atual = datetime.now()
    nome_arquivo = f"consulta_atualiza_judiciais_{data_hora}.log"

    LOG_DIR = log_atualiza_judiciais()
    caminho_arquivo = os.path.join(LOG_DIR, nome_arquivo)

    with open(caminho_arquivo, "a", encoding="utf-8") as f:
        f.write(f"🗓️ Verificação realizada: {data_atual} ({horario_atual.strftime('%H:%M:%S')})\n")
        f.write("\n" + "="*55 + "\n\n")
        if (com_avisos_consumidos and originarios_com_data_entrada_nula_ou_desatualizada and vinculados_com_data_entrada_nula_ou_desatualizada) == 0:
            f.write("🟢 Nenhum erro foi encontado, execução foi bem-sucedida\n")
        
        else:
            if com_avisos_consumidos:
                f.write("- Alerta:\n")
                f.write(f"- Identificados {com_avisos_consumidos[0]['Nenhum nome de coluna']} processos judiciais com avisos consumidos\n")
            if originarios_com_data_entrada_nula_ou_desatualizada:
                f.write("- Alerta: \n")
                f.write(f"- Identificados {originarios_com_data_entrada_nula_ou_desatualizada[0]['Nenhum nome de coluna']}processos originários com data_entrada nula ou desatualizada\n")
            if vinculados_com_data_entrada_nula_ou_desatualizada:
                f.write("- Alerta: \n")
                f.write(f"- Identificados {originarios_com_data_entrada_nula_ou_desatualizada[0]['Nenhum nome de coluna']} processos vinculados com data_entrada nula ou desatualizada\n")
                    
        f.write("\n")        
        f.write("="*55)

    return com_avisos_consumidos, originarios_com_data_entrada_nula_ou_desatualizada, vinculados_com_data_entrada_nula_ou_desatualizada
verificando_atualizacoes_judiciais()