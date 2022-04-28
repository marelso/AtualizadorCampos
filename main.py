from bs4 import BeautifulSoup
#import movimento
import pandas as panda
import os

path = ''
archive = ''
column = ''
dataframe = ''
tablename = ''
driver = ''
server = ''
database = ''
username = ''
password = ''

items = []


def config():
    global path, archive, column, dataframe, tablename, driver, server, database, username, password

    with open('config.xml', 'r') as f:
        data = f.read()
    bs_data = BeautifulSoup(data, 'xml')

    path = str(bs_data.find('path').get('key').replace('user', os.getlogin()))
    archive = str(bs_data.find('archive').get('key'))
    dataframe = str(bs_data.find('dataframe').get('key'))
    tablename = str(bs_data.find('tablename').get('key'))
    column = str(bs_data.find('column').get('key'))
    driver = str(bs_data.find('driver').get('key'))
    server = str(bs_data.find('server').get('key'))
    database = str(bs_data.find('database').get('key'))
    username = str(bs_data.find('username').get('key'))
    password = str(bs_data.find('password').get('key'))


def validar_valor(valor, anterior):
    resultado = ''
    centena = anterior.split('.')
    decimo_anterior = anterior[1] if len(centena[0]) == 3 else anterior[0]

    if int(centena[0]) <= 99 and int(valor[1:4]) <= 99:
        for i, letra in enumerate(valor):
            resultado = resultado + letra + '.' if i == 1 else resultado + letra
    else:
        for i, letra in enumerate(valor):
            resultado = resultado + '.' if i == 3 else resultado + letra

    return resultado


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config()
    #connection = movimento.connection(driver, server, database, username, password)

    #items = movimento.getListagem(query, connection)

    frame = panda.read_excel(archive, sheet_name=dataframe, index_col=None, dtype=str)
    frame.columns = ["CÓDIGO", "DESCRIÇÃO", "DT_INI", "DT_FIM", "TIPO", "FORMATO", "FÓRMULA", "TIPO_LANÇ", "RELAC", "Voltar"]

    print(len(frame.index))

    valor_anterior = '0.00'
    for index, row in frame.iterrows():
        codigo = row["CÓDIGO"]
        coluna = row[column]

        if index != 0 and (float(codigo) > float(valor_anterior) + 100):
            codigo = validar_valor(codigo, str(valor_anterior))
            print(codigo.replace('\n', '') + ' ' + coluna)
        else:            
            print(codigo + " " + coluna)

        query = f'UPDATE {tablename} SET {column} = {coluna} WHERE CODIGO = {codigo} and Layer = {dataframe} FROM '

        print(query)
        valor_anterior = codigo

    teste = input('digite para encerrar')
