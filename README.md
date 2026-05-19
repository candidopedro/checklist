# 🛠️ Sistema de Monitoramento de Tribunais

Este projeto em Python realiza o **monitoramento automatizado de serviços de tribunais**, com funcionalidades como verificação de WSDLs, consumo de avisos/documentos, detecção de feriados, envio de notificações e geração de logs.

## 📁 Estrutura do Projeto

- `main.py` – Ponto de entrada principal do sistema.
- `monitoramento.py` – Orquestra verificações e relatórios.
- `consulta_avisos.py`, `consulta_madrugada.py`, `consulta_retorno.py` – Módulos específicos de consulta a serviços judiciais.
- `consulta_feriados.py`, `feriados_teste.py` – Verificação de feriados nacionais e locais.
- `soap_consulta.py`, `wsdl.py` – Integração com serviços SOAP dos tribunais.
- `pdf_consulta.py` – Processamento de documentos PDF retornados.
- `notificacao.py`, `enderecos_email.py`, `numeros_whatsapp.py` – Envio de alertas via e-mail e WhatsApp.
- `banco.py` – Conexão e consultas ao banco de dados.
- `log_comparacao.py` – Análise de mudanças nos logs.
- `__init__.py` – Arquivo para definir como pacote.

## ⚙️ Requisitos

- Python 3.8+
- Bibliotecas:
  - `requests`
  - `zeep`
  - `pandas`
  - `pyodbc`
  - `python-dotenv`
  - `smtplib`, `email`

## ▶️ Como executar

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd nome-do-projeto
   ```

2. Instale os requisitos:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente (ex: credenciais, endpoints) no arquivo `.env`.

4. Execute o script principal:
   ```bash
   python main.py
   ```

## 📬 Funcionalidades

- 🔍 Consulta automatizada de processos judiciais por tribunal.
- 📤 Envio de notificações por e-mail e WhatsApp.
- 📊 Geração de logs comparativos e relatórios de falhas.
- 📅 Verificação de feriados e controle de execução por horário.