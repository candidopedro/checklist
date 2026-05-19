from dataclasses import dataclass, field

#Faz a ligação de informações entre as verificações

@dataclass
class DadosPDF:
    feriados: list = field(default_factory=list)
    consulta_madrugada: list = field(default_factory=list)
    consulta_avisos: list = field(default_factory=list)
    consulta_srv_pro_223: list = field(default_factory=list)
    consulta_erros: list = field(default_factory=list)
    comun_sem_doc_vinculado: list = field(default_factory=list)
    detalhes_completos: list = field(default_factory=list)
    erro_consumo_log: list = field(default_factory=list)
    comunicacao_candidata: list = field(default_factory=list)
    comunicacoes_criadas: list = field(default_factory=list)
    juncoes: list = field(default_factory=list)
    diagnostico_nao_juntada: list = field(default_factory=list)
    avisos_pendentes_sem_comunicacao: list = field(default_factory=list)
    comunicacoes_com_erro: list = field(default_factory=list)
    avisos_com_processo_judicial: list = field(default_factory=list)

    processos_judiciais_com_avisos_consumidos: list = field(default_factory=list)
    processos_originarios_desatualizados: list = field(default_factory=list)
    processos_vinculados_desatualizados: list = field(default_factory=list)

    #pas_para_especializada:
    pas_para_especializada_lista: list = field(default_factory=list)
    quantidade_de_pas_especializada: int = field(default_factory=int)
    foi_distrubuicao_automaitica_especializada: int = field(default_factory=int)
    nao_foi_distribuicao_automatica_especializada: int = field(default_factory=int)


    pas_para_gsp: int = field(default_factory=int)

    estimativa_email: list = field(default_factory=list)
    comunicacoes_que_exigem_tratamento_especial: list = field(default_factory=list)
    pas_em_tramite_sem_carga: list = field(default_factory=list)
    avisos_que_nao_geraram_comunicacao: list = field(default_factory=list)
    processos_administrativos_existentes: list = field(default_factory=list)