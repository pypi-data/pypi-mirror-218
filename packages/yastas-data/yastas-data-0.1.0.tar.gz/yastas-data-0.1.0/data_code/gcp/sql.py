from secrets import get_secret
import psycopg2
import logging
import os

class Proxy():
    """Funcionalidades relacionadas al proxy para lograr comunicación con bases de datos.
    """
    def logprint_i(self,msg):
        logging.info(msg)
        print(msg)

    def raise_proxy(self, string_connection:str):
        self.logprint_i("Inicia levantacion del proxy.....")
        PROXYUP_COMMANDS = [
            f"rm -fr DTF && mkdir DTF && cd DTF && \
            wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy && ls -la cloud_sql_proxy && \
            chmod 755 cloud_sql_proxy && ls -la cloud_sql_proxy && pwd && ls -latrh && \
            nohup ./{string_connection} -ip_address_types=PRIVATE  & \&& \
            sleep 5 ",
        ]

        self.logprint_i("Inicia descarga proxy")
        for command in PROXYUP_COMMANDS:
            os.system(command)
        self.logprint_i("termina levantacion del proxy.....")

        self.logprint_i("proxy_up_executed")
    
    def shut_down_proxy(self):
        #TODO: Crear la baja del proxy para evitar vulnerabilidades.
        os.system("rm -fr DTF")
        print("\t\t\t\tShut down proxy")

class Database(Proxy):
    """_summary_

    Args:
        Proxy (Proxy): _description_
    """
    def __init__(self, host, port, database, secret_user, secret_pswd, project_id):
        self.host = host
        self.port = port
        self.database_name = database
        user = get_secret(secret_user,project_id)
        password = get_secret(secret_pswd,project_id)
        self.user = user
        self.password = password
        
    def get_connection(self):
        # Establecer la conexión con la base de datos
        connection = psycopg2.connect(
            host=self.host,
            port=self.port, 
            database=self.database_name,
            user=self.user,
            password=self.password
        )
        return connection
    
    def get_tables(self, connection:psycopg2):

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()
        

        # Obtener los nombres de las tablas
        cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                    """)

        # Obtener los resultados
        filas = cursor.fetchall()

        # Procesar los resultados
        tablen="Tablenames"
        print(f"\n/ {tablen.upper():^20} \\")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        
        for fila in filas:
            print(f"| {fila[0]:^20} |")
            print("________________________")
        print("\n")
        # Cerrar el cursor y la conexión
        cursor.close()
        
    def execute_query(self, connection:psycopg2, query:str):

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()

        # Ejecutar una consulta de ejemplo
        cursor.execute(query)

        # Obtener los resultados de la consulta
        filas = cursor.fetchall()

        # Procesar los resultados
        for fila in filas:
            print(fila)

        # Cerrar el cursor y la conexión
        cursor.close()

    def close_connection(self, connection:psycopg2):
        # Cerrar el cursor y la conexión
        connection.close()

host='127.0.0.1'
port=5432
database='yas-inversiones'
query = "SELECT * FROM estatus_movimiento"
string_conn = "cloud_sql_proxy -instances=yas-dev-infraestructura:us-east1:yas-inversiones=tcp:5432"
project_id = "yas-dev-infraestructura"
secret_name = "yas-cierre-user-sql-name-infraestructura-2891887f"
secret_password = "yas-cierre-user-sql-password-infraestructura-2891887f"

postgres = Database(host,port,database,secret_name,secret_password, project_id)
postgres.raise_proxy(string_conn)
conn = postgres.get_connection()
postgres.get_tables(conn)
postgres.execute_query(conn, query=query)
postgres.close_connection(conn)
postgres.shut_down_proxy()