import pyodbc

def banco_main():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'Encrypt=no;'
        'SERVER=10.120.100.58;'
        'DATABASE=//DIGITE O DATABASE//;'
        'UID=//USURIO//;'
        'PWD=//PWD//'
    )

