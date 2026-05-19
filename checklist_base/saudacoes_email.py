from datetime import datetime, time

def saudacao():
    if datetime.now().time() >= time(18,00,00):
        inicio_email = 'Prezados, boa noite!\n\n'
    elif datetime.now().time() >= time(12,00,00):
        inicio_email = 'Prezados, boa tarde!\n\n'
    elif datetime.now().time() >= time(5,00,00):
        inicio_email = 'Prezados, bom dia!\n\n'
    else:
        inicio_email = 'Prezados, bom dia!\n\n'

    return inicio_email