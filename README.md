# 🛠️ Sistema de Monitoramento de Tribunais

Este projeto em Python realiza o **monitoramento automatizado de serviços de tribunais**, com funcionalidades como verificação de WSDLs, consumo de avisos/documentos, detecção de feriados, envio de notificações e geração de logs.

## 📁 Estrutura do Projeto

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

- 🔍 Consulta automatizada de processos.
- 📤 Envio de notificações por e-mail e WhatsApp.
- 📊 Geração de logs comparativos e relatórios de falhas.
