import os

#------------EM TESTE------------
def log_monitoramento_teste():
    log_monitoramento_teste = "LOGs/monitoramento_teste"
    os.makedirs(log_monitoramento_teste, exist_ok=True)

    return log_monitoramento_teste
#-------------------------------

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