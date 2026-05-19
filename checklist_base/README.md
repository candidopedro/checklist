# 🏛️ Monitoramento de Tribunais – PGE Digital

Este projeto realiza o **monitoramento automatizado** dos serviços WSDL dos tribunais. Ele executa consultas simuladas de processos judiciais e envia **alertas por e-mail** caso algum serviço esteja indisponível ou com falhas.

---

## 📁 Estrutura do Projeto

### `config.py`
Responsável pelas configurações principais do sistema:
- E-mail do destinatário dos alertas.
- Estado anterior dos serviços monitorados.

### `conexao.py`
- `conectar_banco()`: Estabelece a conexão com o banco de dados SQL Server.

### `dados.py`
Funções utilitárias para extração de dados:
- `carregar_tribunais()`: Busca os dados dos tribunais no banco.
- `obter_processo_e_data()`: Retorna o número de processo e a data de entrada mais recente.

### `email_alerta.py`
- `enviar_email()`: Envia alertas por e-mail usando protocolo SMTP.

### `soap_consulta.py`
Funções voltadas à comunicação com os webservices:
- `verificar_wsdl()`: Testa a disponibilidade do serviço WSDL.
- `consultar_processo()`: Realiza a requisição SOAP para consulta de processo.

### `monitoramento.py`
Módulo principal do sistema:
- `verificar_todos_os_tribunais()`: Executa o ciclo de verificação:
  - Checagem de status dos WSDLs.
  - Consulta de um processo de teste.
  - Geração de tabela com os resultados.
  - Envio de alerta se houver falhas detectadas.

### `main.py`
Script agendado para execução contínua:
- Dispara `verificar_todos_os_tribunais()` a cada 15 minutos.

---

## 🛠️ Finalidade

Projeto desenvolvido para **facilitar a manutenção preventiva** e **garantir a disponibilidade dos serviços** interligados ao sistema **PGE Digital**, promovendo agilidade na identificação de falhas.

---

