import os

from deta import Deta
from dotenv import load_dotenv

#Cargar las variables de entorno

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

# Inicializar con una clave de proyecto

deta = Deta(DETA_KEY)

# Esto es como crear/conectar una base de datos

db = deta.Base("users_db")

def insert_user(username, name, password):

    """Devuelve el usuario tras una creación exitosa; de lo contrario, genera un error"""
    return db.put({"key": username, "name": name, "password": password})

insert_user("admin", "Elthon Rivas", "Qan40646")
