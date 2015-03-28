DB_HOST = '172.17.0.3'
DB_NAME = 'home_state'
DB_USER = 'hs'
DB_PASSWORD = 'hspass'
DB_PORT=5432

DSN = '''
    dbname={db}
    user={user}
    password={password}
    host={host}
    port={port}
'''.format(
    host=DB_HOST,
    db=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=DB_PORT
)

BIND='127.0.0.1'
PORT=8080
