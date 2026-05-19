import os

def log_monitoramento():
    log_monitoramento_teste = "LOGs/monitoramento_teste"
    os.makedirs(log_monitoramento_teste, exist_ok=True)

    return log_monitoramento_teste

#LOCAL-PDF
def local_relatorios():
    local_relatorios = "relatorios"
    os.makedirs(local_relatorios, exist_ok=True)

    return local_relatorios

#LOCAL-ESTIMATIVA-DE-EMAIL
def local_estimativa_de_email():
    local_estimativa_de_email = "LOGs/estimativa_de_email"
    os.makedirs(local_estimativa_de_email, exist_ok=True)

    return local_estimativa_de_email

#LOG VERIFICACAO_1
def local_verificacao_1():
    local_verificacao_1 = "LOGs/verificacao_1"
    os.makedirs(local_verificacao_1, exist_ok=True)

    return local_verificacao_1