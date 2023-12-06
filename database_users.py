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

def fetch_all_users():
    """Devuelve un diccionario de todos los usuarios."""
    res = db.fetch()
    return res.items

def get_user(username):
    """Si no se encuentra, la función devolverá None"""
    return db.get(username)

def update_user(username, updates):
    """Si el elemento se actualiza, devuelve None. De lo contrario, se plantea una excepción."""
    return db.update(updates, username)


def delete_user(username):
    """Siempre devuelve None, incluso si la clave no existe"""
    return db.delete(username)
