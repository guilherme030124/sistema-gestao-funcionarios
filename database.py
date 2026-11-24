import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

conexao = mysql.connector.connect(
    host=os.getenv("db_host"),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    database=os.getenv("db_database"),
    port=3306,
    use_pure=True
)


def conectar():
    return mysql.connector.connect(
        host=os.getenv("db_host"),
        user=os.getenv("db_user"),
        password=os.getenv("db_password"),
        database=os.getenv("db_database"),
        port=3306,
        use_pure=True
    )


print("Conexão realizada com sucesso!")