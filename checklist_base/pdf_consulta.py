import os
from datetime import datetime
from reportlab.lib import colors
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from notificacao import enviar_pdf_telegram
from notificacao import enviar_pdf_email
from saudacoes_email import saudacao
from gerenciador_diretorios import local_relatorios
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

#Verificações externas
from mni_tribunais_pdf import verificar_status_tribunais
from avisos_pendentes_pdf import consulta_avisos_pendentes

"""
    O  que está como "TÓPICO INDEFINIDO" deve ser revisado e ajustado para o relatório oficial.
"""

def gerar_pdf_relatorio(dados_pdf):

    # A serem ajustados
    feriados = dados_pdf.feriados
    madrugada = dados_pdf.consulta_madrugada
    avisos = dados_pdf.consulta_avisos
    consulta_srv_pro_223 = dados_pdf.consulta_srv_pro_223
    erros_srv_pro_223 = dados_pdf.consulta_erros

    # Se houver comunicações sem documento
    sem_doc_vinculado = dados_pdf.comun_sem_doc_vinculado
    detalhes_completos = dados_pdf.detalhes_completos
    erro_consumo_log = dados_pdf.erro_consumo_log

    # Parte de Junções
    comunicacao_candidata = dados_pdf.comunicacao_candidata
    comunicacoes_criadas = dados_pdf.comunicacoes_criadas
    juncoes = dados_pdf.juncoes
    diagnostico_nao_juntada = dados_pdf.diagnostico_nao_juntada

    # Parte de Avisos pendentes
    avisos_pendentes_sem_comunicacao = dados_pdf.avisos_pendentes_sem_comunicacao
    comunicacoes_com_erro = dados_pdf.comunicacoes_com_erro
    avisos_com_processo = dados_pdf.avisos_com_processo_judicial

    # Parte de Atualizações judiciais
    processos_consumidos = dados_pdf.processos_judiciais_com_avisos_consumidos
    originarios_desatualizados = dados_pdf.processos_originarios_desatualizados
    vinculados_desatualizados = dados_pdf.processos_vinculados_desatualizados

    # Parte de GSP
    pas_para_gsp = dados_pdf.pas_para_gsp

    # Parte de PAs para especializada
    pas_para_especializada = dados_pdf.pas_para_especializada_lista
    quantidade_de_pas = dados_pdf.quantidade_de_pas_especializada
    foi_distrubuicao_automaitica = dados_pdf.foi_distrubuicao_automaitica_especializada
    nao_foi_distribuicao_automatica = dados_pdf.nao_foi_distribuicao_automatica_especializada

    # Estimativas de e-mail
    estimativa_email = dados_pdf.estimativa_email
    
    # Comunicações que exigem tratamento especial
    comunicacoes_que_exigem_tratamento_especial = dados_pdf.comunicacoes_que_exigem_tratamento_especial
    avisos_pendentes_sem_comunicacao = dados_pdf.avisos_que_nao_geraram_comunicacao

    # PAs em trâmite sem carga
    pas_em_tramite_sem_carga = dados_pdf.processos_administrativos_existentes

    # Processos administrativos existentes
    processos_existentes = dados_pdf.processos_administrativos_existentes

    dados = {
        "retorno_srv_pro_223": consulta_srv_pro_223,
        "feriados": feriados,
        "consulta_avisos": avisos,
        "consulta_madrugada": madrugada,
        "consulta_erros": erros_srv_pro_223,
        
        "comun_sem_doc_vinculado": sem_doc_vinculado,
        "detalhes_completos": detalhes_completos,
        "erro_consumo_log": erro_consumo_log,
        
        "pas_para_especializada": pas_para_especializada,

        "comunicacao_candidata": comunicacao_candidata,
        "comunicacoes_criadas": comunicacoes_criadas,
        "juncoes": juncoes,
        "diagnostico_nao_juntada": diagnostico_nao_juntada,

        "avisos_pendentes_sem_comunicacao": avisos_pendentes_sem_comunicacao,
        "comunicacoes_com_erro": comunicacoes_com_erro,
        "avisos_com_processo_judicial": avisos_com_processo,

        "processos_judiciais_processos_consumidos": processos_consumidos,
        "processos_originarios_desatualizados": originarios_desatualizados,
        "processos_vinculados_desatualizados": vinculados_desatualizados,

        "pas_para_gsp": pas_para_gsp,


        "estimativa_email": estimativa_email,

        "comunicacoes_que_exigem_tratamento_especial": comunicacoes_que_exigem_tratamento_especial,
        "avisos_que_nao_geraram_comunicacao": avisos_pendentes_sem_comunicacao,

        "processos_administrativos_existentes": processos_existentes,
    }

    pasta_destino = local_relatorios()
    
    # Estilo para tabelas
    estilo_paragrafo_tabela = ParagraphStyle(
        'paragrafo_tabela',
        fontSize=7,
        wordWrap='CJK'
    )

    #Defição dos tópicos ->
    topicos = []
    
    # feriados ✔
    if feriados:
        topicos.extend([
            {
                "texto": 'Verificando se existe feriado ou ponto facultativo para os tribunais no 58',
                "chave_dados": "feriados",
                "mostrar_tabela": True,
                "intercorrencia": True
            }
        ])
    else:
        topicos.extend([
            {
                "texto": 'Verificando se existe feriado ou ponto facultativo para os tribunais no 58',
                "chave_dados": "feriados",
                "mostrar_tabela": False,
                "texto_se_vazio": "- Nenhum feriado encontrado.",
                "intercorrencia": False
            }
        ])

    # retorno_srv_pro_223 ✔
    if consulta_srv_pro_223: 
        topicos.extend([
            {
                "texto": 'Verificando se a rotina automática de retorno foi executada com a query na tabela log da base Eventos do SRV-PRO-223',
                "chave_dados": "retorno_srv_pro_223",
                "mostrar_tabela": False,
                "texto_se_vazio": "- Rotina realizada no período previsto.",
                "intercorrencia": False
            }
        ])
    else:
        topicos.extend([
            {
                "texto": 'Verificando se a rotina automática de retorno foi executada com a query na tabela log da base Eventos do SRV-PRO-223',
                "chave_dados": "retorno_srv_pro_223",
                "mostrar_tabela": False,
                "texto_se_vazio": "- ROTINA NÃO FOI REALIZADA NO PERÍODO PREVISTO.",
                "intercorrencia": True,
            }
        ])
    
    # consulta_avisos ✔
    if  not avisos:
        topicos.extend([
            {
                "texto": 'Verificando se a rotina de Atualiza JudiciaisComAvisoDisponível está sendo executada de hora em hora no minuto 50 na SRV-PRO-223',
                "chave_dados": "consulta_avisos",
                "mostrar_tabela": False,
                "texto_se_vazio": "- Nenhuma consulta atualiza judiciais com aviso disponível.",
                "intercorrencia": False

            }
        ])
    else:
        topicos.extend([
            {
                "texto": 'Verificando se a rotina de Atualiza JudiciaisComAvisoDisponível está sendo executada de hora em hora no minuto 50 na SRV-PRO-223',
                "chave_dados": "consulta_avisos",
                "mostrar_tabela": True,
                "intercorrencia": False
            }
        ])
    
    # consulta_madrugada ✔
    if not madrugada:
        topicos.extend([
            {
                "texto": 'Verificando se a rotina de consumo foi executada durante a madrugada em SRV-PRO-223',
                "chave_dados": "consulta_madrugada",
                "texto_se_vazio": "- NENHUM CONSUMO NA MADRUGADA ENCONTRADO.",
                "intercorrencia": True
            }
        ])
    else:
        topicos.extend([
            {
                "texto": 'Verificando se a rotina de consumo foi executada durante a madrugada em SRV-PRO-223',
                "chave_dados": "consulta_madrugada",
                "mostrar_tabela": True,
                "intercorrencia": False
            }
        ])

    # consulta erros log SRV-PRO-223 ✔
    if erros_srv_pro_223:
        topicos.extend([
            {
                "texto": 'Verificando os erros do log de execução em Eventos em SRV-PRO-223',
                "chave_dados": "consulta_erros",
                "mostrar_tabela": True,
                "texto_se_vazio": "- Nenhum erro foi encontrado.",
                "intercorrencia": True
            }
        ])

    else:
        topicos.extend([
            {
                "texto": 'Verificando os erros do log de execução em Eventos em SRV-PRO-223',
                "chave_dados": "consulta_erros",
                "mostrar_tabela": True,
                "texto_se_vazio": "- Nenhum erro foi encontrado.",
                "intercorrencia": False
            }
        ])
    
    # comunicação sem documento vinculado ✔
    topicos.extend([
        {
            "texto": 'Verificando se existe comunicação sem documento em SRV-PRO-058',
            "texto_se_vazio": " ",
            "titulo_vazio": True,
        }
    ])

    if sem_doc_vinculado:
        fontes = ""
        for lista in sem_doc_vinculado:
            fontes += lista['fonte'] + ", "

        fontes = fontes.rstrip(", ")

        bloco_sem_doc_vinculado = (
            f"● EXISTE COMUNICAÇÃO SEM DOCUMENTO PARA {fontes}, A ROTINA consumo_aviso FICA TRAVADA.<br/><br/>"
        )
        texto_sem_doc_vinculado = []
        texto_sem_doc_vinculado.append(bloco_sem_doc_vinculado)

        texto_sem_doc_vinculado = "".join(texto_sem_doc_vinculado)

        topicos.extend([
            {
                "texto": '- Verificando se existe comunicação sem documento em SRV-PRO-058',
                "chave_dados": "comun_sem_doc_vinculado",
                "mostrar_tabela": False,
                "texto_se_vazio": texto_sem_doc_vinculado,
                "intercorrencia": True,
                "backgroud_texto": True,
                "sub_topico": True
            }
        ])

    if detalhes_completos:
        topicos.extend([
            {
                "texto": '- Detalhes completos dos registros de comunicação sem documento',
                "chave_dados": "detalhes_completos",
                "mostrar_tabela": True,
                "texto_se_vazio": texto_sem_doc_vinculado,
                "intercorrencia": True,
                "sub_topico": True
            }
        ])

    if erro_consumo_log:
        topicos.extend([
            {
                "texto": '- Verifica se houve erro de consumo no log, no servidor SRV-PRO-223',
                "chave_dados": "erro_consumo_log",
                "mostrar_tabela": True,
                "intercorrencia": True,
                "sub_topico": True
            }
        ])

    else: 
        topicos.extend([
            {
                "texto": 'Verificando se existe comunicação sem documento em SRV-PRO-058',
                "chave_dados": "comun_sem_doc_vinculado",
                "mostrar_tabela": False,
                "texto_se_vazio": "- Nenhum registro foi encontrado.",
                "intercorrencia": False
            }
        ])
        
    #Avisos pendentes ----------------------------->
    tribunais_avisos = [
        "TJRJ",
        "EPROC1",
        "EPROC2",
        "TRT1",
        "TRT2",
        "PJE1",
        "STF",
        "TST",
        "TJSP",
        "TRF11G",
        "TRF12G"   
    ]

    erro_aviso = False

    for tribunal in tribunais_avisos:
        _, deteccao_erros = consulta_avisos_pendentes(tribunal)
        if deteccao_erros == True:
            erro_aviso = True
        break

    topicos.append({
            "texto": 'Iniciando a consulta de avisos pendentes',
            "mostrar_tabela": False,
            "titulo_vazio": True,
            **({"intercorrencia": True} if erro_aviso == True else {"intercorrencia": False})
        })
    
    for tribunal in tribunais_avisos:
        retorno,deteccao_erros = consulta_avisos_pendentes(tribunal)
        topicos.append({
            "texto": " ",
            "texto_se_vazio": f"- {tribunal} {retorno}",
            "mostrar_tabela": False,
            **({"intercorrencia": True} if deteccao_erros == True else {"intercorrencia": False})
        })
    
    # Parte de Junções ✔
    if (
        dados["comunicacao_candidata"] == dados["comunicacoes_criadas"] ==
        dados["juncoes"]
    ):
        topicos.append({
            "texto": "Verificando Comunicações & Junções na 58",
            "mostrar_tabela": False,
            "texto_se_vazio": "- Nenhum erro foi encontrado nas junções.",       
        })

    else:
        lista_juncoes = diagnostico_nao_juntada
        if lista_juncoes:
            blocos_texto = []
            for j in lista_juncoes:
                bloco = (
                    f"● Tribunal: {j.get('fonte tribunal', '')}<br/><br/>"
                    f"- ID: {j.get('pj.id', '')}<br/>"
                    f"- CNJ: {j.get('cnj', '')}<br/>"
                    f"- Data disponibilização: {j.get('data_disponibilizacao', '')}<br/>"
                    f"- Quantidade de avisos: {j.get('aviso_pendente.id', '')}<br/>"
                    f"- ID Aviso: {j.get('id_aviso', '')}<br/>"
                    f"- Comunicações: {j.get('comunicacao.id', '')}<br/>"
                    f"- Data de recebimento: {j.get('data_recebimento', '')}<br/>"
                    f"- PA: {j.get('pa_id', '')}<br/>"
                    f"- Localidade: {j.get('localidade', '')}<br/>"
                    f"- Especializada: {j.get('especializada do PA', '')}<br/>"
                    f"- Usa PGE Digital: {j.get('usa_pge_digital', '')}<br/>"
                    f"- Acervo migrado: {j.get('acervo migrado', '')}<br/>"
                    f"- Predição ML: {j.get('predicao ML', '')}<br/>"
                    f"- Possui Documento: {j.get('Tem Doc', '')}<br/>"
                    f"- Juntou na PA: {j.get('juntou no PA', '')}<br/>"
                    f"- Enviou por email: {j.get('Enviou Por Email', '')}<br/><br/>"
                )
                blocos_texto.append(bloco)

            texto_juncoes = "".join(blocos_texto)

            topicos.append({
                "texto": "Verificando Comunicações & Junções na 58:",
                "mostrar_tabela": False,
                "texto_se_vazio": texto_juncoes,
                "intercorrencia": True,
                "backgroud_texto": True
            })

        else:
            topicos.append({
                "texto": "Verificando Comunicações & Junções na 58:",
                "mostrar_tabela": False,
                "texto_se_vazio": "- Nenhum erro foi encontrado nas junções."
            })

    # Veriﬁcação se algum aviso pendente deixou de ter comunicação criada no 58  - AINDA NÃO ESTÁ COMO O RELATÓRIO OFICIAL/ SUB TOPICO
    topicos.append({
        "texto": 'Verificação se algum aviso pendente deixou de ter comunicação criada no 58:',
        "texto_se_vazio": "",
        "titulo_vazio": True,
    })

    if avisos_pendentes_sem_comunicacao:
        texto_avisos_pendentes_sem_comunicacao = []
        for a in avisos_pendentes_sem_comunicacao:
            bloco_avisos_pendentes_sem_comunicacao = (
                f"● Tribunal:  {str(a.get('fonte', ''))}<br/><br/>"
                f"- ID: {str(a.get('id', ''))}<br/><br/>"
                f"- CNJ: {str(a.get('cnj', ''))}<br/><br/>"
                f"- Data Disponibilização: {str(a.get('data_disponibilizacao', ''))}<br/><br/>"
                f"- Quantidade de Avisos: {str(a.get('aviso_pendente.id', ''))}<br/><br/>"
                f"- ID Aviso: {str(a.get('id_aviso', ''))}<br/><br/>"
                f"- Comunicações: {str(a.get('comunicacao.id', ''))}<br/><br/>"
                f"- Data de Recebimento: {str(a.get('data_recebimento', ''))}<br/><br/>"
                f"- PA: {str(a.get('pa_id', ''))}<br/><br/>"
                f"- Localidade: {str(a.get('localidade', ''))}<br/><br/>"
                f"- Especializada: {str(a.get('especializada do PA', ''))}<br/><br/>"
                f"- Usa PGE Digital: {str(a.get('usa_pge_digital', ''))}<br/><br/>"
                f"- Acervo Migrado: {str(a.get('acervo migrado', ''))}<br/><br/>"
                f"- Predição ML: {str(a.get('predicao ML', ''))}<br/><br/>"
                f"- Possui Documento: {str(a.get('Tem Doc', ''))}<br/><br/>"
                f"- Juntou na PA: {str(a.get('juntou no PA', ''))}<br/><br/>"
                f"- Enviou por Email: {str(a.get('Enviou Por Email', ''))}<br/><br/>"
            )
        texto_avisos_pendentes_sem_comunicacao.append(bloco_avisos_pendentes_sem_comunicacao)
        texto_avisos_pendentes_sem_comunicacao = "".join(bloco_avisos_pendentes_sem_comunicacao)

        topicos.append({
            "texto": '- Avisos pendentes sem comunicação criada',
            "chave_dados": "avisos_pendentes_sem_comunicacao",
            "mostrar_tabela": False,
            "texto_se_vazio": texto_avisos_pendentes_sem_comunicacao,
            "intercorrencia": True,
            "backgroud_texto": True,
            "sub_topico": True
        })

    else:
        topicos.append({
            "texto": '',
            "chave_dados": "avisos_pendentes_sem_comunicacao",
            "mostrar_tabela": False,
            "texto_se_vazio": "- Nenhum aviso pendente deixou de ter comunicação criada.",
            "backgroud_texto": True,
            "sub_topico": True
        })

    if comunicacoes_com_erro:
        texto_comunicacoes_com_erro = []
        for a in comunicacoes_com_erro:
            bloco_comunicacoes_com_erro = (
                f"● Comunicação Recebida<br/><br/>"
                f"- ID: {str(a.get('id', ''))}<br/><br/>"
                f"- Processo: {str(a.get('processo', ''))}<br/><br/>"
                f"- Teor: {str(a.get('teor', ''))}<br/><br/>"
                f"- Tipo Comunicação ID: {str(a.get('tipo_comunicacao_id', ''))}<br/><br/>"
                f"- Aviso Pendente ID: {str(a.get('aviso_pendente_id', ''))}<br/><br/>"
                f"- Tipo Prazo ID: {str(a.get('tipo_prazo_id', ''))}<br/><br/>"
                f"- Data Referência: {str(a.get('data_referencia', ''))}<br/><br/>"
                f"- Prazo: {str(a.get('prazo', ''))}<br/><br/>"
                f"- Nível Sigilo ID: {str(a.get('nivel_sigilo_id', ''))}<br/><br/>"
                f"- Mensagem: {str(a.get('mensagem', ''))}<br/><br/>"
                f"- Sucesso: {str(a.get('sucesso', ''))}<br/><br/>"
                f"- Responsável ID: {str(a.get('responsavel_id', ''))}<br/><br/>"
                f"- Comunicação Física: {str(a.get('comunicacao_fisica', ''))}<br/><br/>"
                f"- Processo Judicial ID: {str(a.get('processo_judicial_id', ''))}<br/><br/>"
                f"- Número Registro: {str(a.get('numero_registro', ''))}<br/><br/>"
                f"- Data Recebimento: {str(a.get('data_recebimento', ''))}<br/><br/>"
                f"- Processo Administrativo ID: {str(a.get('processo_administrativo_id', ''))}<br/><br/>"
                f"- Prazo Atendimento Hora: {str(a.get('prazo_atendimento_hora', ''))}<br/><br/>"
                f"- Prazo Atendimento Dia: {str(a.get('prazo_atendimento_dia', ''))}<br/><br/>"
                f"- Estado ID: {str(a.get('estado_id', ''))}<br/><br/>"
                f"- Competência: {str(a.get('competencia', ''))}<br/><br/>"
                f"- Classe Processual: {str(a.get('classe_processual', ''))}<br/><br/>"
                f"- Código Órgão: {str(a.get('codigo_orgao', ''))}<br/><br/>"
                f"- Nome Órgão: {str(a.get('nome_orgao', ''))}<br/><br/>"
                f"- Código Localidade: {str(a.get('codigo_localidade', ''))}<br/><br/>"
                f"- Número Comunicação: {str(a.get('numero_comunicacao', ''))}<br/><br/>"
            )
        texto_comunicacoes_com_erro.append(bloco_comunicacoes_com_erro)
        texto_comunicacoes_com_erro = "".join(bloco_comunicacoes_com_erro)

        topicos.append({
            "texto": '- Verificando se existe comunicações com erro sem sucesso posteriormente',
            "chave_dados": "comunicacoes_com_erro",
            "mostrar_tabela": False,
            "texto_se_vazio": texto_comunicacoes_com_erro,
            "intercorrencia": True,
            "backgroud_texto": True,
            "sub_topico": True
        })

    else:
        topicos.append({
            "texto": '',
            "chave_dados": "avisos_pendentes_sem_comunicacao",
            "mostrar_tabela": False,
            "texto_se_vazio": "- Nenhuma comunicação que por acaso tenha dado erro no consumo, deixou de ser consumida com sucesso em uma nova tentativa",
            "backgroud_texto": True,
            "sub_topico": True
        })

    if avisos_com_processo:
        texto_avisos_com_processo = []
        for a in avisos_com_processo:
            bloco_avisos_com_processo = (
                    f"● Tribunal:  {str(a.get('fonte', ''))}<br/><br/>"
                    f"- ID: {str(a.get('id', ''))}<br/><br/>"
                    f"- ID Aviso: {str(a.get('id_aviso', ''))}<br/><br/>"
                    f"- ID Destinatário: {str(a.get('destinatario_id', ''))}<br/><br/>"
                    f"- ID Processo: {str(a.get('processo_id', ''))}<br/><br/>"
                    f"- Data Disponibilização: {str(a.get('data_disponibilizacao', ''))}<br/><br/>"
                    f"- ID do tipo de Comunicação: {str(a.get('tipo_comunicacao_id', ''))}<br/><br/>"
                    f"- Sucesso: {str(a.get('sucesso', ''))}<br/><br/>"
                    f"- Mensagem: {str(a.get('mensagem', ''))}<br/><br/>"
                    f"- Data do Consultado: {str(a.get('data_consultado', ''))}<br/><br/>"
                    f"- Baixado: {str(a.get('baixado', ''))}<br/><br/>"
                    f"- Origem: {str(a.get('origem', ''))}<br/><br/>"
            )

        texto_avisos_com_processo.append(bloco_avisos_com_processo)
        texto_avisos_com_processo = "".join(bloco_avisos_com_processo)

        topicos.append({
            "texto": '- Verificando se existe avisos com processo judicial',
            "chave_dados": "avisos_com_processo_judicial",
            "mostrar_tabela": False,
            "texto_se_vazio": texto_avisos_com_processo,
            "intercorrencia": True,
            "backgroud_texto": True,
            "sub_topico": True
        })

    else:
        topicos.append({
            "texto": '',
            "mostrar_tabela": False,
            "texto_se_vazio": "- Nenhum aviso pendente de processo judicial sem processo administrativo deixou de ser enviado",
            "backgroud_texto": True,
            "sub_topico": True
        })
    
    # Verificando se a rotina atualiza judiciais com avisos consumidos está sendo executada na máquina 10.120.100.162->"
    if (processos_consumidos and originarios_desatualizados 
        and vinculados_desatualizados) == 0:

        topicos.append({
            "texto": 'Verificando se a rotina atualiza judiciais com avisos consumidos está sendo executada na máquina 10.120.100.162',
            "mostrar_tabela": False,
            "texto_se_vazio": "- A execução foi bem-sucedida",
            "backgroud_texto": True
        })

    else:
        topicos.append({
            "texto": 'Verificando se a rotina atualiza judiciais com avisos consumidos está sendo executada na máquina 10.120.100.162',
            "chave_dados": "processos_judiciais_processos_consumidos",
            "mostrar_tabela": True,
            "intercorrencia": True,
            "backgroud_texto": True
        })

        topicos.append({
            "texto": ' ',
            "chave_dados": "processos_originarios_desatualizados",
            "mostrar_tabela": True,
            "intercorrencia": True,
        })

        topicos.append({
            "texto": ' ',
            "chave_dados": "processos_vinculados_desatualizados",
            "mostrar_tabela": True,
            "intercorrencia": True,
        })

    # Veriﬁcando quantidade de PAs distribuídos para GSP no 58 ✔
    texto_pas_para_gsp = []

    if pas_para_gsp == 0: 
        bloco_pas_para_gps = (f"- NÃO HOUVE DISTRIBUIÇÃO DE PROCESSOS ADMINISTRATIVOS PARA A GSP HOJE<br/><br/>")
        
        texto_pas_para_gsp.append(bloco_pas_para_gps)
        texto_pas_para_gsp = "".join(bloco_pas_para_gps)
        
        topicos.append({
            "texto": 'Verificando quantidade de PAs distribuídos para GSP no 58',
            "mostrar_tabela": False,
            "texto_se_vazio": texto_pas_para_gsp,
            "intercorrencia": True,
            "backgroud_texto": True
        })

    elif pas_para_gsp == 1:
        bloco_pas_para_gps = (f"- Foi distribuído {pas_para_gsp} Processo Administrativo para a GSP.<br/><br/>")

        texto_pas_para_gsp.append(bloco_pas_para_gps)
        texto_pas_para_gsp = "".join(bloco_pas_para_gps)
        
        topicos.append({
            "texto": 'Verificação de PAs para GSP',
            "mostrar_tabela": False,
            "texto_se_vazio": texto_pas_para_gsp,
            "backgroud_texto": True
        })
        
    elif pas_para_gsp > 1:
        bloco_pas_para_gps = (f"- Foram distribuídos {pas_para_gsp} Processos Administrativos para a GSP.<br/><br/>")

        texto_pas_para_gsp.append(bloco_pas_para_gps)
        texto_pas_para_gsp = "".join(bloco_pas_para_gps)

        topicos.append({
            "texto": 'Verificação de PAs para GSP',
            "mostrar_tabela": False,
            "texto_se_vazio": texto_pas_para_gsp,
            "backgroud_texto": True
        })

    # Veriﬁcando quandade de PAs distribuídos no 58 ✔
    if (quantidade_de_pas + foi_distrubuicao_automaitica + nao_foi_distribuicao_automatica ) == 0:
        topicos.extend([
            {
                "texto": 'Verificando quantidade de PAs distribuídos no 58',
                "chave_dados": "pas_para_especializada",
                "mostrar_tabela": True,
                "intercorrencia": True
            }
        ])
    else:
        topicos.extend([
            {
                "texto": 'Verificando quantidade de PAs distribuídos no 58',
                "chave_dados": "pas_para_especializada",
                "mostrar_tabela": True,
                "intercorrencia": False
            }
        ])

    # Iniciando a execução da estimativa de envio de e-mail ✔ 
    topicos.extend([
        {
            "texto": 'Iniciando a execução da estimativa de envio de e-mail ',
            "chave_dados": "estimativa_email",
            "mostrar_tabela": True,
        }
    ])

    #Querys finais -------------------------->

    #Parte de Comunicações que exigem tratamento especial:
    topicos.append({
        "texto": 'Verificando Querys Finais no 58',
        "mostrar_tabela": False,
        "titulo_vazio": True,
    })

    if comunicacoes_que_exigem_tratamento_especial:
        texto_comunicacoes_que_exigem_tratamento_especial = []
        for b in comunicacoes_que_exigem_tratamento_especial:
            bloco_comunicacoes_que_exigem_tratamento_especial = (
                f"● Tribunal: {str(b.get('fonte', ''))}<br/><br/>"
                f"- Data recebimento: {str(b.get('data_recebimento', ''))}<br/><br/>"
                f"- Data disponibilização: {str(b.get('data_disponibilizacao', ''))}<br/><br/>"
                f"- CNJ: {str(b.get('cnj', ''))}<br/><br/>"
                f"- Aviso pendente ID: {str(b.get('aviso_pendente_id', ''))}<br/><br/>"
                f"- ID Aviso: {str(b.get('id_aviso', ''))}<br/><br/>"
                f"- Com ID: {str(b.get('com_id', ''))}<br/><br/>"
                f"- VW Juntar: {str(b.get('vw_Juntar', ''))}<br/><br/>"
                f"- Tem Doc: {str(b.get('tem_doc', ''))}<br/><br/>"
                f"- Localidade: {str(b.get('localidade', ''))}<br/><br/>"
                f"- PA ID: {str(b.get('pa_id', ''))}<br/><br/>"
                f"- Especializada do PA: {str(b.get('especializada_do_pa', ''))}<br/><br/>"
                f"- Predição ML: {str(b.get('predicao_ml', ''))}<br/><br/>"
                f"- PJ ID: {str(b.get('pj_id', ''))}<br/><br/>"
            )
        texto_comunicacoes_que_exigem_tratamento_especial.append(bloco_comunicacoes_que_exigem_tratamento_especial)
        texto_comunicacoes_que_exigem_tratamento_especial = "".join(bloco_comunicacoes_que_exigem_tratamento_especial)

        topicos.append({
            "texto": '- Verificando se existe Comunicações encontradas que exigem tratamento especial',
            "chave_dados": "comunicacoes_que_exigem_tratamento_especial",
            "mostrar_tabela": False,
            "texto_se_vazio": texto_comunicacoes_que_exigem_tratamento_especial,
            "intercorrencia": True,
            "backgroud_texto": True,
            "sub_topico": True
        })

        if avisos_pendentes_sem_comunicacao:
            texto_avisos_nao_geram = []
            for b in avisos_pendentes_sem_comunicacao:
                bloco_avisos_nao_geram = (
                    f"● Tribunal: {str(b.get('fonte', ''))}<br/><br/>"
                    f"- CNJ: {str(b.get('CNJ', ''))}<br/><br/>"
                    f"- Data disponibilização: {str(b.get('data_disponibilizacao', ''))}<br/><br/>"
                    f"- Data consultado: {str(b.get('data_consultado', ''))}<br/><br/>"
                    f"- Aviso pendente ID: {str(b.get('aviso_pendente.id', ''))}<br/><br/>"
                    f"- Tipo comunicação ID: {str(b.get('tipo_comunicacao_id', ''))}<br/><br/>"
                    f"- Localidade: {str(b.get('localidade', ''))}<br/><br/>"
                    f"- Código PA: {str(b.get('codigo_pa', ''))}<br/><br/>"
                    f"- ID PA: {str(b.get('pa_id', ''))}<br/><br/>"
                    f"- ID aviso: {str(b.get('id_aviso', ''))}<br/><br/>"
                )
            texto_avisos_nao_geram.append(bloco_avisos_nao_geram)
            texto_avisos_nao_geram = "".join(bloco_avisos_nao_geram)

            topicos.append({
                "texto": '- Verificando se existe Avisos que não geraram comunicação',
                "chave_dados": "avisos_que_nao_geraram_comunicacao",
                "mostrar_tabela": False,
                "texto_se_vazio": texto_avisos_nao_geram,
                "intercorrencia": True,
                "backgroud_texto": True,
                "sub_topico": True
            })
        else:
            topicos.append({
                "texto": ' ',
                "mostrar_tabela": False,
                "texto_se_vazio": "- As querys de verifcação finais não existem valores que venham criar alguma ação.",
                "sub_topico": True
        })

    # topicos.append({
    #     "texto": "Verificando bloqueios no banco de dados e funcionamento",
    #     "mostrar_tabela": False,
    #     "texto_se_vazio": "TÓPICO INDEFINIDO",
    #     "backgroud_texto": True
    # })

    # MNI dos tribunais ->
    # Ainda não está com a detecção de intercorrência

    tribunais_mni = [
        "TRF11G",
        "TRF12G",
        "EPROC1",
        "EPROC2",
        "TJSP",
        "STJ",
        "TST",
        "STF",
        "PJE1",
        "TRT1",
        "TRT2",
        "TJRJ"
    ]

    erro_mni = False

    for tribunal in tribunais_mni:
        _, deteccao_erros = verificar_status_tribunais(tribunal)
        if deteccao_erros == True:
            erro_mni = True
        break

    topicos.append({
        "texto": "Verificando consultas de processos e MNI dos tribunais",
        "titulo_vazio": True,
        "intercorrencia": True,
        **({"intercorrencia": True} if erro_mni == True else {"intercorrencia": False})
    })

    for tribunal in tribunais_mni: 
        status, deteccao_erros = verificar_status_tribunais(tribunal)
        topicos.append({
            "texto": " ",
            "texto_se_vazio": f"- Consulta de processos no PGEDigital ao {tribunal} {status}.",
            "mostrar_tabela": False,
            **({"intercorrencia": True} if deteccao_erros == True else {"intercorrencia": False})
        })

    # topicos.append({
    #     "texto": "Verificando publicações do Diário Oficial no horário 07:10 no 223",
    #     "mostrar_tabela": False,
    #     "chave_dados": "TÓPICO INDEFINIDO",
    #     "texto_se_vazio": "TÓPICO INDEFINIDO",
    #     "backgroud_texto": True
    # })
    
    # PAs considerados em trâmite e que não possuem carga ->
    if pas_em_tramite_sem_carga:
        texto_pas_em_tramite_sem_carga = []
        for linha in pas_em_tramite_sem_carga:
            bloco_pas_em_tramite_sem_carga = (
                f"● PA em trâmite e sem carga<br/><br/>"
                f"- Código PA: {str(linha.get('codigo_pa', ''))}<br/><br/>"
                f"- Última tramitação registrada: {str(linha.get('ultima_tramitacao_registrada', ''))}<br/><br/>"
                f"- Estado PA: {str(linha.get('estado', ''))}<br/><br/>"
                f"- Especializada: {str(linha.get('especializada', ''))}<br/><br/>"
                f"- Acervo: {str(linha.get('acervo', ''))}<br/><br/>"
                f"- Responsável Adm: {str(linha.get('responsavel_adm', ''))}<br/><br/>"
                f"- Procurador Titular: {str(linha.get('procurador_titular', ''))}<br/><br/>"
                f"- Data última tramitação: {str(linha.get('data_hora_tramitacao', ''))}<br/><br/>"
                f"- Estado da comunicação: {str(linha.get('estado_comunicacao', ''))}<br/><br/>"
                f"- Data recebimento comunicação: {str(linha.get('data_recebimento_comunicacao', ''))}<br/><br/>"
                f"- Data criação providência: {str(linha.get('data_criacao_providencia', ''))}<br/><br/>"
                f"- Prazo providência: {str(linha.get('prazo_providencia', ''))}<br/><br/>"
                f"<br/><br/>"
            )
            texto_pas_em_tramite_sem_carga.append(bloco_pas_em_tramite_sem_carga)

        texto_pas_em_tramite_sem_carga = "".join(texto_pas_em_tramite_sem_carga)

        topicos.append({
            "texto": "Verificando se existem Processos Administrativos que são considerados em trâmite e não possuem carga no 58",
            "chave_dados": "processos_administrativos_existentes",
            "mostrar_tabela": False,
            "texto_se_vazio": texto_pas_em_tramite_sem_carga,
            "intercorrencia": True,
            "backgroud_texto": True
        })
    else:
        topicos.append({
            "texto": "Verificando se existem Processos Administrativos que são considerados em trâmite e não possuem carga no 58",
            "mostrar_tabela": False,
            "texto_se_vazio": "- Nenhum registro foi encontrado. ",
            "sub_topico": True
    })

    # topicos.append({
    #     "texto": "Verificando a atualização da rotina diária processarUnidadesUsuarios na API SEI",
    #     "mostrar_tabela": False,
    #     "chave_dados": "TÓPICO INDEFINIDO",
    #     "texto_se_vazio": "TÓPICO INDEFINIDO",
    #     "backgroud_texto": True
    # })

    #Estilos ->

    # Estilo titulo vazio:
    estilo_titulo_vazio = ParagraphStyle(
        name="TopicoEstilo",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceAfter=10,
        textColor=colors.red
    )

    # Estilo titulo vazio:
    estilo_titulo_vazio_alerta = ParagraphStyle(
        name="TopicoEstilo",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceAfter=10,
        textColor=colors.black
    )

    # Estilo para títulos dos tópicos
    estilo_topico = ParagraphStyle(
        name="TopicoEstilo",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceAfter=10,
        textColor=colors.black
    )

    # Topico em alerta - QUANDO TIVER INTERCORRÊNCIA
    estilo_topico_alerta = ParagraphStyle(
        name="TopicoEstiloAlerta",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceAfter=10,
        textColor=colors.red,
        borderPadding=(4, 6, 4, 6)
    )

    # Estilo para SUB títulos dos tópicos - SEM INTERCORRÊNCIA
    estilo_topico_sub = ParagraphStyle(
        name="TopicoEstilo",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceAfter=10,
        textColor=colors.black,
        leftIndent=20 
    )

    # Estilo para SUB títulos dos tópicos - COM INTERCORRÊNCIA
    estilo_topico_sub_erro = ParagraphStyle(
        name="TopicoEstilo",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceAfter=10,
        textColor=colors.red,
        leftIndent=20 
    )

    styles = getSampleStyleSheet()

    # Estilo textos com fundo - COM INTERCORRÊNCIA
    estilo_texto_com_fundo_intercorrencia = ParagraphStyle(
        name="TextoComFundo",
        fontName='Helvetica-Bold',
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.red,
        backColor=colors.HexColor("#FFF4CC"),
        borderPadding=(6, 6, 6, 6),
    )

    # Estilo textos com fundo - SEM INTERCORRÊNCIA
    estilo_texto_com_fundo = ParagraphStyle(
        name="TextoComFundo",
        fontName='Helvetica-Bold',
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.black,
        backColor=colors.HexColor("#FFF4CC"),
        borderPadding=(6, 6, 6, 6)
    )

    # Estilo textos com fundo - COM INTERCORRÊNCIA/SUB TÓPICO
    estilo_texto_com_fundo_intercorrencia_sub = ParagraphStyle(
        name="TextoComFundo",
        fontName='Helvetica-Bold',
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.red,
        backColor=colors.HexColor("#FFF4CC"),
        borderPadding=(6, 6, 6, 6),
        leftIndent=20 
    )

    # Estilo textos com fundo - SEM INTERCORRÊNCIA/SUB TÓPICO
    estilo_texto_com_fundo_sub = ParagraphStyle(
        name="TextoComFundo",
        fontName='Helvetica-Bold',
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.black,
        backColor=colors.HexColor("#FFF4CC"),
        borderPadding=(6, 6, 6, 6),
        leftIndent=20 
    )

    # Cria o PDF em formato A4 retrato
    data_atual = datetime.now().strftime("%d-%m-%Y")
    arquivo_pdf = f"Report Checklist Diário_{data_atual}.pdf"
    caminho_arquivo_pdf = os.path.join(pasta_destino, arquivo_pdf)
    doc = SimpleDocTemplate(caminho_arquivo_pdf, pagesize=A4)

    Story = []

    # Status no título
    for topico in topicos:
        if topico.get("intercorrencia"):
            status_titulo = "COM INTERCORRÊNCIA"
            break
        else:
            status_titulo = "SEM INTERCORRÊNCIA"

    # Título
    data_titulo = datetime.now().strftime("%d/%m/%Y")
    titulo = Paragraph(f"<b>Report Checklist Diário - {data_titulo}</b>", styles['Title'])
    titulo_status = Paragraph(f"<b>{status_titulo}</b>", styles['Title'])

    Story.append(titulo)
    Story.append(titulo_status)
    Story.append(Spacer(1, 20))

    # Monta tópicos
    for topico in topicos:

        #Titulo vazio
        if topico.get("titulo_vazio") == True:
            Story.append(Paragraph(topico["texto"], estilo_titulo_vazio))
            continue

        #Titulo vazio - com intercorrência
        if topico.get("titulo_vazio") == True and topico.get("intercorrencia") == True:
            Story.append(Paragraph(topico["texto"], estilo_titulo_vazio_alerta))
            continue

        # Estilo do tópico/título
        if topico.get("intercorrencia") == True and not topico.get("sub_topico") and not topico.get("titulo_vazio"):
            Story.append(Paragraph(topico["texto"], estilo_topico_alerta))
        elif not topico.get("sub_topico") and not topico.get("titulo_vazio"):
            Story.append(Paragraph(topico["texto"], estilo_topico))

        # Estilo do sub tópico
        if topico.get("sub_topico") == True and topico.get("intercorrencia") == True and not topico.get("titulo_vazio"):
            Story.append(Paragraph(topico["texto"], estilo_topico_sub_erro))
        elif topico.get("sub_topico") == True and not topico.get("titulo_vazio"):
            Story.append(Paragraph(topico["texto"], estilo_topico_sub))
        Story.append(Spacer(1, 8))

        # Texto com fundo
        if not topico.get("mostrar_tabela", False) and topico.get("intercorrencia") == True and not topico.get("sub_topico"):
            Story.append(Paragraph(topico.get("texto_se_vazio", "- Nenhum registro."), estilo_texto_com_fundo_intercorrencia))
            Story.append(Spacer(1, 15))
            continue
        elif not topico.get("mostrar_tabela", False) and not topico.get("sub_topico"): 
            Story.append(Paragraph(topico.get("texto_se_vazio", "- Nenhum registro."), estilo_texto_com_fundo))
            Story.append(Spacer(1, 15))
            continue

        # Texto com fundo - SUB TÓPICOS
        if not topico.get("mostrar_tabela", False) and topico.get("intercorrencia") == True and topico.get("sub_topico") == True:
            Story.append(Paragraph(topico.get("texto_se_vazio", "- Nenhum registro."), estilo_texto_com_fundo_intercorrencia_sub))
            Story.append(Spacer(1, 15))
            continue
        elif not topico.get("mostrar_tabela", False) and topico.get("sub_topico") == True: 
            Story.append(Paragraph(topico.get("texto_se_vazio", "- Nenhum registro."), estilo_texto_com_fundo_sub))
            Story.append(Spacer(1, 15))
            continue

        lista_dados = dados.get(topico.get("chave_dados", []), [])

        if not lista_dados or not isinstance(lista_dados, list) or not isinstance(lista_dados[0], dict):
            Story.append(Paragraph(topico.get("texto_se_vazio", "- Nenhum registro."), estilo_texto_com_fundo))
            Story.append(Spacer(1, 15))
            continue

        cabecalho = list(lista_dados[0].keys())
        corpo = [
            [Paragraph(escape(str(item.get(col, ""))), estilo_paragrafo_tabela) for col in cabecalho]
            for item in lista_dados
        ]
        tabela_dados = [cabecalho] + corpo
        t = Table(tabela_dados, repeatRows=1)

        if not topico.get("sub_topico"):
            t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#222222")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                    ('BACKGROUND', (0, 1), (-1, -1),colors.HexColor("#FFF4CC")),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            Story.append(t)

        else:
            t.hAlign = "RIGHT",
            t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#222222")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                    ('BACKGROUND', (0, 1), (-1, -1),colors.HexColor("#FFF4CC")),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            Story.append(t)

        Story.append(Spacer(1, 15))

    # Gera PDF
    doc.build(Story)
    data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    if status_titulo == "COM INTERCORRÊNCIA":
        enviar_pdf_telegram(caminho_arquivo_pdf, f"⚠️ Report Checklist {data_hora} - {status_titulo}")
    else:
        enviar_pdf_telegram(caminho_arquivo_pdf, f"✅ Report Checklist {data_hora} - {status_titulo}")

    inicio_email = saudacao()

    if status_titulo == "COM INTERCORRÊNCIA":
        enviar_pdf_email(f"⚠️ Report Checklist {data_hora} - {status_titulo}", 
                        inicio_email + f"Segue o Relatório atualizado de hoje: \n", caminho_arquivo_pdf)
    else:
        enviar_pdf_email(f"✅ Report Checklist {data_hora} - {status_titulo}", 
                        inicio_email + f"Segue o Relatório atualizado de hoje: \n", caminho_arquivo_pdf)
    print(" "*20, "✔ Relatório gerado e enviado")