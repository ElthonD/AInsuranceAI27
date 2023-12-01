import os

from deta import Deta
from dotenv import load_dotenv

#Cargar las variables de entorno

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

# Inicializar con una clave de proyecto

deta = Deta(DETA_KEY)

# Esto es como crear/conectar una base de datos

db_ainsurance = deta.Base("ainsurance_db")          

def insert_register_ainsurance(fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, estatus, coment):

    """Devuelve el registro tras una creación exitosa; de lo contrario, genera un error"""
    return db_ainsurance.put({"Fecha": fecha, "Nombre Monitorista": ndocumentador,"Bitácora": nBitacora, "Cliente": sCliente, "Motivo de Entrada": mEntrada, "Marca": marca, "Modelo": modelo,"Placas": placas, "Economico": economico, "Latitud": latitud, "Longitud": longitud, "Estado": estado, "Estatus": estatus, "Observaciones": coment})

def fetch_all_ainsurance():
    """Devuelve un diccionario de todos los registros."""
    res = db_ainsurance.fetch()
    return res.items

def update_ainsurance(fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, estatus, coment, updates):
    """Si el elemento se actualiza, devuelve None. De lo contrario, se plantea una excepción."""
    return db_ainsurance.update(updates, fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, estatus, coment)

def delete_ainsurance(fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, estatus, coment):
    """Siempre devuelve None, incluso si la clave no existe"""
    return db_ainsurance.delete(fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, estatus, coment)