from banco import banco_main

# <<<<<<<<<<<<<<<<<-Disponibilidade dos Tribunais-<<<<<<<<<<<<<<<<<<<<< -HU1/HU2
def carregar_informacoes(sigla):
    conn = banco_main()
    cursor = conn.cursor()
    cursor.execute(f'''
            SELECT ';
        ''')
    
    dados = []
    
    row = cursor.fetchall()[0]
    tribunal_id, sigla, descricao, _, wsdl, id_consultante, senha_consultante = row
    dados.append({
        "id": tribunal_id,
        "sigla": sigla or descricao,
        "wsdl": wsdl,
    })

    conn.close()
    return dados