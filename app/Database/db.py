import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def connection_postgres():
    return psycopg2.connect(
        host=os.getenv("HOST_POSTGRES"),
        dbname=os.getenv("DATABASE_POSTGRES"),
        user=os.getenv("USER_POSTGRES"),
        password=os.getenv("PASSWORD_POSTGRES"),
        port=os.getenv("PORT_POSTGRES")
    )
