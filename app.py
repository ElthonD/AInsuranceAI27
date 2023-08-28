### Librerías

from PIL import Image
import streamlit as st
import requests
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import folium_static
from dateutil.relativedelta import *
import seaborn as sns; sns.set_theme()
import streamlit as st
import io

# buffer to use for excel writer
buffer = io.BytesIO()

# Configuración warnings
# ==============================================================================
import warnings
warnings.filterwarnings('ignore')

path_favicon = './img/Logo AInsurance.png'
im = Image.open(path_favicon)
st.set_page_config(page_title='AI27 AInsurance', page_icon=im, layout="wide")
path = './img/Logo AInsurance.png'
image = Image.open(path)
col1, col2, col3 = st.columns([1,2,1])
col2.image(image, use_column_width=True)

@st.cache_data(show_spinner='Cargando Datos... Espere...', persist=True)
def load_df():

    ruta = './data/data.xlsx'
    df = pd.read_excel(ruta, sheet_name = "Sheet1")
    df['Fecha y Hora'] = pd.to_datetime(df['Fecha y Hora'], format='%Y-%m-%d %H:%M:%S')
    df['Eco'] = df['Eco'].astype('str')
    #df['Fecha'] = df['Fecha'].dt.strftime('%m/%d/%Y')
    #df['Fecha'] = pd.to_datetime(df['Fecha'], format="%Y/%m/%d", infer_datetime_format=True)
    df['Año'] = df['Fecha y Hora'].apply(lambda x: x.year)
    df['MesN'] = df['Fecha y Hora'].apply(lambda x: x.month)
    df['Mes'] = df['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
    df['Dia'] = df['Fecha y Hora'].apply(lambda x: x.day)
    return df

def GenerarMapaBase(Centro=[20.5223, -99.8883], zoom=8):
        MapaBase = folium.Map(location=Centro, control_scale=True, zoom_start=zoom)
        return MapaBase

def map_coropleta_fol(df):
    
    geojson_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'
    mx_estados_geo = requests.get(geojson_url).json()

    MapaMexico = GenerarMapaBase()

    #Mapa Coropleta
    df1 = pd.DataFrame(pd.value_counts(df['Estado']))
    df1 = df1.reset_index()
    df1.rename(columns={'index':'Estado','Estado':'Total'},inplace=True)

    folium.Choropleth(
        geo_data=mx_estados_geo,
        name="Mapa Coropleta",
        data=df1,
        columns=["Estado", "Total"],
        key_on="feature.properties.name",
        fill_color="OrRd",
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name="Total de Robos",
        nan_fill_color = "White",
        show=True,
        overlay=True,
        Highlight= True,
        ).add_to(MapaMexico)

    #Insertar Robos
    FeatRobo = folium.FeatureGroup(name='Robos')
    #Recorrer marco de datos y agregar cada punto de datos al grupo de marcadores
    Latitudes2 = df['Latitud'].to_list()
    Longitudes2 = df['Longitud'].to_list()
    Popups2 = df['Fecha y Hora'].to_list()
    Popups3 = df['Estatus'].to_list()
    Popups4 = df['Estado'].to_list()
    Popups5 = df['Municipio'].to_list()
    Popups6 = df['Tramo'].to_list()
 
    for lat2, long2, pop2, pop3, pop4, pop5, pop6 in list(zip(Latitudes2, Longitudes2, Popups2, Popups3, Popups4, Popups5, Popups6)):
        fLat2 = float(lat2)
        fLon2 = float(long2)
        if pop3 == "CONSUMADO":
            folium.Circle(
                radius=1500,
                location=[fLat2,fLon2],
                popup= [pop2,pop3,pop4, pop5, pop6],
                fill=False,
                color="darkred").add_to(FeatRobo)
        else:
            folium.Circle(
                radius=1500,
                location=[fLat2,fLon2],
                popup= [pop2,pop3,pop4, pop5, pop6],
                fill=False,
                color="darkgreen").add_to(FeatRobo)
        
    MapaMexico.add_child(FeatRobo)
    folium.LayerControl().add_to(MapaMexico)
    #Agregar Botón de Pantalla Completa 
    plugins.Fullscreen(position="topright").add_to(MapaMexico)

    #Mostrar Mapa
    folium_static(MapaMexico, width=1370)

try:

    df = load_df()
    st.markdown("<h3 style='text-align: left;'>Histórico de Robos</h3>", unsafe_allow_html=True)
    st.write(f"Este marco de datos contiene información histórica de los robos en el proyecto Ainsurance desde **{df.Mes.values[0]} {df.Año.values[0].astype(int)}** a **{df.Mes.values[-1]} {df.Año.values[-1].astype(int)}**")

    def callback1(key_name):
        st.session_state[key_name]

    key_name = 'my_df'
    edited_df = st.data_editor(data=df[['Fecha y Hora','Dia','Motivo Entrada','Placas','Eco','Marca','Modelo','Latitud','Longitud','Estado','Municipio','Tramo','Estatus']], 
                               num_rows="dynamic",
                               on_change=callback1,
                               args=[key_name],
                               key=key_name)

    if st.button("Guardar"):
        path1 = './data/data.xlsx'
        edited_df.to_excel(path1, index=False)
        st.write("Se han guardador los cambios")

    #st.write(st.session_state["my_df"])
    #st.data_editor(df, num_rows="dynamic")

    st.markdown("<h3 style='text-align: left;'>Mapa de Robos</h3>", unsafe_allow_html=True)

    mapa = map_coropleta_fol(edited_df)

except NameError as e:
    print("Seleccionar: ", e)

except ZeroDivisionError as e:
    print("Seleccionar: ", e)
    
except KeyError as e:
    print("Seleccionar: ", e)

except ValueError as e:
    print("Seleccionar: ", e)
    
except IndexError as e:
    print("Seleccionar: ", e)

    # ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

