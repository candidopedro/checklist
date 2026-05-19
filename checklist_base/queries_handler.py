from banco import banco_pge_digital_58, banco_eventos_223

# <<<<<<<<<<<<<<<<<-Disponibilidade dos Tribunais-<<<<<<<<<<<<<<<<<<<<< -HU1/HU2
def carregar_tribunais(sigla):
    conn = banco_pge_digital_58()
    cursor = conn.cursor()
    cursor.execute(f'''
            SELECT id, sigla, descricao, identificador_cnj, wsdl, id_consultante, senha_consultante 
        FROM dbo.mni_tribunal
        where sigla = '{sigla}';
        ''')
    
    tribunais = []
    
    row = cursor.fetchall()[0]
    tribunal_id, sigla, descricao, _, wsdl, id_consultante, senha_consultante = row
    tribunais.append({
        "id": tribunal_id,
        "sigla": sigla or descricao,
        "wsdl": wsdl,
        "id_consultante": id_consultante,
        "senha_consultante": senha_consultante
    })

    conn.close()
    return tribunais