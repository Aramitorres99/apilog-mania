import psycopg2
from psycopg2 import OperationalError
import os 
from dotenv import load_dotenv

load_dotenv()

#realizar la conexion a la base de datos
def get_conexion():
    try:
        conn = psycopg2.connect(
            dbname = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            host= os.getenv('DB_HOST'),
            port = os.getenv('DB_PORT')
        )
        print("La conexion fue exitosa")
        return conn
    except OperationalError as e:
        print(f"Error de conexion: {e}")
        return None
    
    

if __name__ == '__main__':
    get_conexion()
 