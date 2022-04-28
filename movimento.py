import pyodbc as sql


def connection(driver, server, database, username, password):
    connected = sql.connect(f"Driver={driver};Server={server};Database={database};Trusted_Connection=yes;uid={username};pwd={password}")
    return connected


def getListagem(query, connected):
    lista = []

    cursor = connected.cursor()
    cursor.execute(query)

    for row in cursor:
        teste = '%r' % (row,)
        lista.append(teste)
    return lista
