import apache_beam as beam
from gcp.sql import Database

class GetQuery(beam.DoFn):
    def __init__(self, host, port, database, query, string_conn, project_id, secret_user, secret_password):
        self.host=host
        self.port=port
        self.database=database
        self.query = query
        self.string_conn = string_conn
        self.project_id = project_id
        self.secret_user = secret_user
        self.secret_password = secret_password
        self.postgres = Database(self.host,self.port,self.database,self.secret_user,self.secret_password, self.project_id)
        self.conn = self.postgres.get_connection()

    def setup(self):
        self.postgres.raise_proxy(string_conn)

    def process(self, element, *args, **kwargs):
        
        
        query_result=self.postgres.execute_query(self.conn, query=query)
        
        yield query_result

    def teardown(self):
        self.postgres.close_connection(self.conn)
        self.postgres.shut_down_proxy()
        return super().teardown()

host='127.0.0.1'
port=5432
database='yas-inversiones'
query = """SELECT column_name, udt_name 
                            FROM information_schema.columns 
                            WHERE table_name='estatus_movimiento'
                            AND table_schema='public'
                            ORDER BY ordinal_position"""
string_conn = "cloud_sql_proxy -instances=yas-dev-infraestructura:us-east1:yas-inversiones=tcp:5432"
project_id = "yas-dev-infraestructura"
secret_user = "yas-cierre-user-sql-name-infraestructura-2891887f"
secret_password = "yas-cierre-user-sql-password-infraestructura-2891887f"