import pyodbc

def banco_main():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'Encrypt=no;'
        'SERVER=//DIGITE O ENDERECO DO BANCO//;'
        'DATABASE=//DIGITE O DATABASE//;'
        'UID=//USURIO//;'
        'PWD=//PWD//'
    )

