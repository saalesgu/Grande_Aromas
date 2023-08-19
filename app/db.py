import psycopg2

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='Josari242008',
            database='Grande_Aromas'
        )
        print('Conexión a la base de datos exitosa')
        return connection
    except Exception as ex:
        print('Error al conectar a la base de datos:', ex)
        return None
