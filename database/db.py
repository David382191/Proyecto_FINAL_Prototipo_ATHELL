######################################################################################
######################################################################################
import psycopg2
from psycopg2 import Error

def get_db():
    try:
        connection = psycopg2.connect(
            host="localhost",        # 🔴 LOCAL
            port="5433",
            user="postgres",         # o el usuario que creaste
            password="1234",
            dbname="chatbot_secretaria",
            sslmode="disable"        # 🔴 LOCAL → SIN SSL
        )
        return connection

    except Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None
######################################################################################
######################################################################################