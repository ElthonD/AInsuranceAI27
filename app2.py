import pandas as pd
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from datetime import datetime  # Core Python Module
from PIL import Image
import requests
import folium
from folium import plugins
from streamlit_folium import folium_static
import seaborn as sns; sns.set_theme()
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import database_users as user_db
import database_ainsurance as ainsurance_db


# Title of the main page
path_favicon = './img/favicon1.png'
im = Image.open(path_favicon)
st.set_page_config(page_title='AI27 AInsurance', page_icon=im, layout="wide")
path = './img/Logo AInsurance.png'
image = Image.open(path)
col1, col2, col3 = st.columns([1,2,1])
col2.image(image, use_column_width=True)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- USER AUTHENTICATION ---
users = user_db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "ai27_ainsurance", "abcdef", cookie_expiry_days=30)

# --- DATABASE INTERFACE ---
#def get_all_periods():
    #items = ainsurance_db.fetch_all_ainsurance()
    #periods = [item["Fecha"] for item in items]
    #return periods

col4, col5, col6 = st.columns([1,1,1])

with col5:
    name, authentication_status, username = authenticator.login("Ingresar", "main")
    
    if authentication_status == False:
        st.error("Usuario/Contraseña is incorrecta")
        
    if authentication_status == None:
        st.warning("Por favor, ingresa usuario y contraseña")

if authentication_status:

    # ---- SIDEBAR ----
    authenticator.logout("Salir", "sidebar")
    st.sidebar.title(f"Bienvenido {name}")
    # Mostrar tipo de auditoria a registrar
    options = st.sidebar.selectbox("Seleccionar Opciones:",("Registro de Eventos","Data Visualización","Mapa de Calor"))
    # Realizar auditorías seleccionadas

    if options=="Registro de Eventos":

        st.markdown("<h2 style='text-align: left;'>Registro de Eventos AInsurance</h2>", unsafe_allow_html=True)
        st.write(f"Registrar eventos de los servicios (Bitácoras) que fueron detonados como emergencia por los clientes AInsurance de AI27.")

        # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
        date = datetime.today()
        #usr = name
        cliente = ["SITRACK", "AUTOFLETES CHIHUAHUA", "TGT", "MAEDA", "MAVERICK", "TRANSPORTES MENDEZ","SETRAMEX"]
        notificacion = ["Llamada del Cliente", "Whatsapp del Cliente", "Alerta por Telegram", "Bitácora Centro Monitoreo", "Correo del Cliente"]
        marcatracto = ["KENWORTH", "INTERNACIONAL", "FREIGHTLINER", "VOLVO", "MERCEDES"]
        estado = ["Ciudad de México", "México", "Querétaro", "Puebla", "Guanajuato", "Veracruz", "Chiapas", "Jalisco", "Durango", "Hidalgo", "San Luis Potosí", "Nuevo León", "Chihuahua","Campeche", "Sonora","Zacatecas", "Sinaloa", "Tamaulipas", "Oaxaca", "Tabasco", "Michoacán", "Colima", "Guerrero", "Tlaxcala", "Morelos", "Baja California", "Quintana Roo", "Yucatán", "Aguascalientes", "Coahuila", "Nayarit"]
        estatus = ["RECUPERADO", "CONSUMADO"]

        with st.form("entry_form", clear_on_submit= True):
            col7, col8, col9, col10 = st.columns([1,1,1,1])
            with col7:
                fecha = st.text_input("Fecha:", placeholder="Fecha del Evento", key="fecha1")
            with col8:
                ndocumentador = st.text_input("Nombre Monitorista:", name, disabled=True, key="name1")
            with col9:
                nBitacora = st.text_input("Bitácora:", placeholder="Nro Bitácora", key="bitacora1")
            with col10:
                sCliente = st.selectbox("Cliente:", cliente, placeholder="Nombre Cliente", key="cliente1")
            col11, col12, col13, col14 = st.columns([1,1,1,1])   
            with col11: 
                mEntrada = st.selectbox("Motivo de Entrada:", notificacion, placeholder="Tipo de Notificación", key="notificacion1")  
            with col12: 
                marca = st.selectbox("Marca:", marcatracto, placeholder="Marca del Tracto", key="marca1")
            with col13: 
                modelo = st.text_input("Modelo:", placeholder="Año del Tracto", key="ao1")
            with col14: 
                placas = st.text_input("Placas:", placeholder="Placas del Tracto", key="placas1")
            col15, col16, col17, col18, col19 = st.columns([1,1,1,1,1])
            with col15:
                economico = st.text_input("Económico:", placeholder="Número Económico", key="economico1")
            with col16:    
                latitud = st.text_input("Latitud:", placeholder="Latitud", key="latitud1")
            with col17:    
                longitud = st.text_input("Longitud:", placeholder="Longitud", key="longitud1")
            with col18:
                estado = st.selectbox("Estado:", estado, key="estado1")
            with col19:    
                estatus = st.selectbox("Estatus:", estatus, key="estatus1")
        
            coment = st.text_area("Observaciones:", placeholder="Escriba Observaciones ...", key= "coments")
            "---"
            col19, col20, col21, col22, col23 = st.columns([1,1,1,1,1])
            with col21:
                submitted = st.form_submit_button("Guardar")
                if submitted:
                    ainsurance_db.insert_register_ainsurance(fecha, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, estatus, coment)
                    st.success("¡Guardado!")

    elif options=="Data Visualización":

        pass
        

    elif options=="Mapa de Calor":
        
        pass