import os
import streamlit as st
from deta import Deta
from dotenv import load_dotenv

#Cargar las variables de entorno

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

# Inicializar con una clave de proyecto

deta = Deta(DETA_KEY)

# Esto es como crear/conectar una base de datos

db_ainsurance = deta.Base("ainsurance_db")          

def insert_register_ainsurance(fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment):

    """Devuelve el registro tras una creación exitosa; de lo contrario, genera un error"""
    return db_ainsurance.put({"Fecha": fecha, "Nombre Monitorista": ndocumentador,"Bitácora": nBitacora, "Cliente": sCliente, "Motivo de Entrada": mEntrada, "Marca": marca, "Modelo": modelo,"Placas": placas, "Economico": economico, "Latitud": latitud, "Longitud": longitud, "Estado": estado,"Municipio": municipio,"Tramo": tramo, "Estatus": estatus, "Observaciones": coment})

def fetch_all_ainsurance():
    """Devuelve un diccionario de todos los registros."""
    res = db_ainsurance.fetch()
    return res.items

def update_ainsurance(fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment, updates):
    #"""Si el elemento se actualiza, devuelve None. De lo contrario, se plantea una excepción."""
    return db_ainsurance.update(updates, fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)

def delete_ainsurance(fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment):
    """Siempre devuelve None, incluso si la clave no existe"""
    return db_ainsurance.delete(fecha, ndocumentador, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)

# Funciones para actualizar DB

def delete_all_registers():
    items: list[dict] = fetch_all_ainsurance()
    for d in items:
        db_ainsurance.delete(d['key'])

def put_new_register(edited_df):
    
    if len(edited_df):
        cnt = 0

        # 1. Delete
        delete_all_registers()

        # 2. Add
        list_of_dict = edited_df.to_dict('records')
        for d in list_of_dict:
            # There should be username, because the deta db needs a key
            # and our key is the username.
            if d['key'] is None:
                continue
            key = d['key']
            d.pop('key')
            db_ainsurance.put(d, key=key)
            cnt += 1

        if cnt:
            st.success('Actualizado')


