# soap_consulta.py
import hashlib
import requests
from zeep import Client
from datetime import date

def verificar_wsdl(wsdl_url):
    try:
        r = requests.get(wsdl_url, timeout=10)
        return (r.status_code == 200), f"HTTP {r.status_code}"
    except Exception as e:
        return False, "Erro de conexão"