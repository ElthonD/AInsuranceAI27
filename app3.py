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

#Metodos

# Grafico Sankey
       
def genSankey(df,cat_cols=[],value_cols='', title='Sankey Diagram'):
    # maximum of 6 value cols -> 6 colors
    colorPalette = ['#4B8BBE','#306998','#FFE873','#FFD43B','#646464']
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp
        
    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))
    
    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum
        
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
    
    # creating the sankey diagram
    data = dict(
        type='sankey',
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(
                color = "black",
                width = 0.5
            ),
            label = labelList,
            color = colorList
        ),
        link = dict(
            source = sourceTargetDf['sourceID'],
            target = sourceTargetDf['targetID'],
            value = sourceTargetDf['count']
        )
    )   
    layout =  dict(
        title = title,
        font = dict(
            size = 10
            )
    )
       
    fig = dict(data=[data], layout=layout)        
    return fig

def df_grafico(df):
    
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d', errors='coerce')

    # Para Cumplimiento
    df1 = df.copy()
    df1 = df1.loc[df1.loc[:, 'Estatus'] == 'RECUPERADO']
    df1.drop(['Motivo de Entrada', 'Economico', 'Marca', 'Modelo', 'Latitud', 'Longitud','Estado', 'Municipio', 'Tramo'], axis = 'columns', inplace=True)    
    df1 = df1.set_index('Fecha')
    df2 = pd.DataFrame(df1['Placas'].resample('M').count())
    df2 = df2.rename(columns={'Placas':'RECUPERADO'})

    # Para No Cumplimiento
    df3 = df.copy()
    df3 = df3.loc[df3.loc[:, 'Estatus'] == 'CONSUMADO']
    df3.drop(['Motivo de Entrada', 'Economico', 'Marca', 'Modelo', 'Latitud', 'Longitud','Estado', 'Municipio', 'Tramo'], axis = 'columns', inplace=True)    
    df3 = df3.set_index('Fecha')
    df4 = pd.DataFrame(df3['Placas'].resample('M').count())
    df4 = df4.rename(columns={'Placas':'CONSUMADO'})

    # Unir dataframe
    df5 = pd.concat([df2, df4], axis=1)
    
    # Reset Indíces
    df5 = df5.reset_index()

    # Preparar Dataframe Final
    df5['MesN'] = df5['Fecha'].apply(lambda x: x.month)
    df5['Mes'] = df5['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
    df5['Año'] = df5['Fecha'].dt.year
    df5 = df5.fillna(0)
    df5['Total'] = (df5['RECUPERADO'] + df5['CONSUMADO'])
    df5['% Recuperado'] = round((df5['RECUPERADO'] / df5['Total']),2) * 100
    df5['% Consumado'] = round((df5['CONSUMADO'] / df5['Total']),2) * 100
    df5['Recuperados (%)'] = round((df5['RECUPERADO'] / df5['Total']),2) * 100
    df5['Mes Año'] = df5['Mes'] + ' ' + df5['Año'].astype(str)
        
    df5 = df5.dropna()

    return df5

def g_recuperacion(df):
    
    sr_data1 = go.Bar(x = df['Fecha'],
                      y=df['RECUPERADO'],
                      opacity=0.8,
                      yaxis = 'y1',
                      name='Recuperados',
                      text= [f'Recuperado(s): {x:.0f}' for x in df['RECUPERADO']]
                      )
    
    sr_data2 = go.Bar(x = df['Fecha'],
                      y=df['CONSUMADO'],
                      opacity=0.8,
                      yaxis = 'y1',
                      name='Consumados',
                      text= [f'Consumado(s): {x:.0f}' for x in df['CONSUMADO']]
                      )
    
    sr_data3 = go.Bar(x = df['Fecha'],
                      y=df['Total'],
                      opacity=0.8,
                      yaxis = 'y1',
                      name='Intentos',
                      text= [f'Intentos: {x:.0f}' for x in df['Total']]
                      )
    
    sr_data4 = go.Scatter(x = df['Fecha'],
                          y=df['Recuperados (%)'],
                          line=go.scatter.Line(color='green', width = 0.6),
                          opacity=0.8,
                          yaxis = 'y2',
                          hoverinfo = 'text',
                          name='% Recuperados',
                          text= [f'Recuperados(s): {x:.0f}%' for x in df['Recuperados (%)']])
    
    # Create a layout with interactive elements and two yaxes
    layout = go.Layout(height=700, width=700, font=dict(size=7), hovermode="x unified",
                       plot_bgcolor="#FFF",
                       xaxis=dict(showgrid=False, title='Fecha',
                                        # Range selector with buttons
                                         rangeselector=dict(
                                             # Buttons for selecting time scale
                                             buttons=list([
                                                 # 1 month
                                                 dict(count=1,
                                                      label='1m',
                                                      step='month',
                                                      stepmode='backward'),
                                                # 3 month
                                                 dict(count=3,
                                                      label='3m',
                                                      step='month',
                                                      stepmode='backward'),
                                                 # Entire scale
                                                 dict(step='all')
                                             ])
                                         ),
                                         # Sliding for selecting time window
                                         rangeslider=dict(visible=True),
                                         # Type of xaxis
                                         type='date'),
                        yaxis=dict(showgrid=False, title='Cantidad de Robos', color='red', side = 'left'),
                        # Add a second yaxis to the right of the plot
                        yaxis2=dict(showgrid=False, title='% Recuperación/Mes', color='blue',
                                          overlaying='y1',
                                          side='right')
                        )
    fig = go.Figure(data=[sr_data1, sr_data2, sr_data3, sr_data4], layout=layout)
    fig.update_layout(barmode='stack')
    st.plotly_chart(fig, use_container_width=True)

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
    Popups2 = df['Fecha'].to_list()
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

# --- USER AUTHENTICATION ---
users = user_db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

#authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "ai27_ainsurance", "abcdef", cookie_expiry_days=30)
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "ai27_ainsurance", "abcdef")

# --- DATABASE INTERFACE ---

def obtener_df():
    data = ainsurance_db.fetch_all_ainsurance()
    return data

def get_all_entries_from_deta_db():
    response = ainsurance_db.fetch_all_ainsurance()
    items: list[dict] = response.items
    return items

#DF_HEADER = ['key', 'Bitácora', 'Cliente', 'Economico', 'Estado', 'Estatus', 'Fecha', 'Latitud', 'Longitud', 'Marca', 'Modelo', 'Motivo de Entrada', 'Municipio', 'Nombre Monitorista', 'Observaciones', 'Placas', 'Tramo']
DF_HEADER = ['key','Fecha', 'Nombre Monitorista', 'Bitácora', 'Cliente', 'Motivo de Entrada', 'Marca', 'Modelo', 'Placas', 'Economico', 'Latitud', 'Longitud', 'Estado', 'Municipio', 'Tramo', 'Estatus', 'Observaciones']
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

    if username == 'admin':
        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Registro y Edición de Eventos","Data Visualización","Mapa de Calor"))
        # Realizar auditorías seleccionadas

        if options=="Registro y Edición de Eventos":
                
            st.markdown("<h2 style='text-align: left;'>Registro de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Registrar eventos de los servicios (Bitácoras) que fueron detonados como emergencia por los clientes AInsurance de AI27.")

            # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
            date = datetime.today()
            #usr = name
            cliente = ["SITRACK", "AUTOFLETES CHIHUAHUA", "TGT", "MAEDA", "MAVERICK", "TRANSPORTES MENDEZ","SETRAMEX"]
            notificacion = ["Llamada del Cliente", "Whatsapp del Cliente", "Alerta por Telegram", "Bitácora Centro Monitoreo", "Correo del Cliente"]
            marcatracto = ["KENWORTH", "INTERNACIONAL", "FREIGHTLINER", "VOLVO", "MERCEDES"]
            estado = ["Ciudad de México", "México", "Querétaro", "Puebla", "Guanajuato", "Veracruz", "Chiapas", "Jalisco", "Durango", "Hidalgo", "San Luis Potosí", "Nuevo León", "Chihuahua","Campeche", "Sonora","Zacatecas", "Sinaloa", "Tamaulipas", "Oaxaca", "Tabasco", "Michoacán", "Colima", "Guerrero", "Tlaxcala", "Morelos", "Baja California", "Quintana Roo", "Yucatán", "Aguascalientes", "Coahuila", "Nayarit"]
            estatus = ["RECUPERADO", "CONSUMADO", "FRUSTADO", "PENDIENTE","NO APLICA"]

            with st.form("entry_form", clear_on_submit= True):
                col7, col8, col9, col10, col11 = st.columns([1,1,1,1,1])
                with col7:
                    fecha = st.text_input("Fecha:", placeholder="Fecha del Evento", key="fecha1")
                with col8:
                    ndocumentador = st.text_input("Nombre Monitorista:", name, disabled=True, key="name1")
                with col9:
                    nBitacora = st.text_input("Bitácora:", placeholder="Nro Bitácora", key="bitacora1")
                with col10:
                    sCliente = st.selectbox("Cliente:", cliente, placeholder="Nombre Cliente", key="cliente1")
                with col11: 
                    mEntrada = st.selectbox("Motivo de Entrada:", notificacion, placeholder="Tipo de Notificación", key="notificacion1")
                col12, col13, col14, col15, col16 = st.columns([1,1,1,1,1])   
                with col12: 
                    marca = st.selectbox("Marca:", marcatracto, placeholder="Marca del Tracto", key="marca1")
                with col13: 
                    modelo = st.text_input("Modelo:", placeholder="Año del Tracto", key="ao1")
                with col14: 
                    placas = st.text_input("Placas:", placeholder="Placas del Tracto", key="placas1")
                with col15:
                    economico = st.text_input("Económico:", placeholder="Número Económico", key="economico1")
                with col16:    
                    latitud = st.text_input("Latitud:", placeholder="Latitud", key="latitud1")
                col17, col18, col19, col20, col21, = st.columns([1,1,1,1,1])
                with col17:    
                    longitud = st.text_input("Longitud:", placeholder="Longitud", key="longitud1")
                with col18:
                    estado = st.selectbox("Estado:", estado, key="estado1")
                with col19:    
                    municipio = st.text_input("Municipio:", placeholder="Municipio", key="municipio")
                with col20:    
                    tramo = st.text_input("Tramo:", placeholder="Tramo Carretero", key="tramo1")
                with col21:    
                    estatus = st.selectbox("Estatus:", estatus, key="estatus1")

                coment = st.text_area("Observaciones:", placeholder="Escriba Observaciones ...", key= "coments1")
                "---"
                col19, col20, col21, col22, col23 = st.columns([1,1,1,1,1])
                with col21:
                    submitted = st.form_submit_button("Guardar")
                    if submitted:
                        ainsurance_db.insert_register_ainsurance(fecha, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)
                        st.success("¡Guardado!")

            st.markdown("<h2 style='text-align: left;'>Edición de Marco de Datos de los Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Marco de datos para editar eventos de los servicios (Bitácoras) AInsurance de AI27 registrados con errores o cambios de estatus posteriores.")
                
            elementos = ainsurance_db.fetch_all_ainsurance()
            if len(elementos) < 1:
                df1 = pd.DataFrame(columns=DF_HEADER)
            else:
                df1 = pd.DataFrame(elementos)

            # Hide the key in display. In Deta db, the key is the username.
            edited_df = st.data_editor(
                df1,
                num_rows="dynamic",
                key='account',
                column_config={"key": None}
            )
            col24, col25, col26, col27, col28 = st.columns([1,1,1,1,1])
            with col26:
                if st.button("Actualizar"):
                    ainsurance_db.put_new_register(edited_df)

        elif options=="Data Visualización":
                
            df = pd.DataFrame(obtener_df())
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y', errors='coerce')
            df['Año'] = df['Fecha'].apply(lambda x: x.year)
            df['MesN'] = df['Fecha'].apply(lambda x: x.month)
            df['Mes'] = df['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
        
            st.markdown("<h2 style='text-align: left;'>Visualización de Datos del Histórico de Eventos</h2>", unsafe_allow_html=True)
            st.write(f"Marco de datos del histórico de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df.Mes.min()} {df.Año.min().astype(int)}*** a ***{df.Mes.max()} {df.Año.max().astype(int)}***.")
        
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                container1 = st.container()
                allC1 = st.checkbox("Seleccionar Todos", key="chk1")
                if allC1:
                    sorted_unique_cliente = sorted(df['Cliente'].unique())
                    selected_cliente = container1.multiselect('Cliente(es):', sorted_unique_cliente, sorted_unique_cliente, key="cliente1")
                    df_selected_cliente = df[df['Cliente'].isin(selected_cliente)].astype(str)
                else:
                    sorted_unique_cliente = sorted(df['Cliente'].unique())
                    selected_cliente = container1.multiselect('Cliente(es)', sorted_unique_cliente, key="cliente2")
                    df_selected_cliente = df[df['Cliente'].isin(selected_cliente)].astype(str)
            
            with c2:
                container2 = st.container()
                allC2 = st.checkbox("Seleccionar Todos", key="chk2")
                if allC2:
                    sorted_unique_ao = sorted(df_selected_cliente['Año'].unique())
                    selected_ao = container2.multiselect('Año(s):', sorted_unique_ao, sorted_unique_ao, key="año1") 
                    df_selected_ao = df_selected_cliente[df_selected_cliente['Año'].isin(selected_ao)].astype(str)
                else:
                    sorted_unique_ao = sorted(df_selected_cliente['Año'].unique())
                    selected_ao = container2.multiselect('Año(s):', sorted_unique_ao, key="año2") 
                    df_selected_ao = df_selected_cliente[df_selected_cliente['Año'].isin(selected_ao)].astype(str)
        
            with c3:
                container3 = st.container()
                allC3 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC3:
                    sorted_unique_mes = sorted(df_selected_ao['Mes'].unique())
                    selected_mes = container3.multiselect('Mes(es):', sorted_unique_mes, sorted_unique_mes, key="mes1") 
                    df_selected_mes = df_selected_ao[df_selected_ao['Mes'].isin(selected_mes)].astype(str)
                else:
                    sorted_unique_mes = sorted(df_selected_ao['Mes'].unique())
                    selected_mes = container3.multiselect('Mes(es):', sorted_unique_mes, key="mes2") 
                    df_selected_mes = df_selected_ao[df_selected_ao['Mes'].isin(selected_mes)].astype(str)
        
            # Dataframe
            st.markdown("<h5 style='text-align: left;'>Datos históricos de los eventos</h5>", unsafe_allow_html=True)
            df_selected_mes = df_selected_mes[['Fecha', 'Nombre Monitorista', 'Bitácora', 'Cliente', 'Motivo de Entrada', 'Marca', 'Modelo', 'Placas', 'Economico', 'Latitud', 'Longitud', 'Estado', 'Municipio', 'Tramo', 'Estatus', 'Observaciones']]
            st.dataframe(df_selected_mes)
            x1, x2, x3, x4, x5 = st.columns([1,1,1,1,1])
            with x3:
                export1 = st.button("Descargar")
                if export1:
                    df_selected_mes.to_excel("Historico.xlsx")
                    st.success("¡Archivo Descargado!")

            # Métricas
            st.markdown("<h5 style='text-align: left;'>Métricas</h5>", unsafe_allow_html=True)

            total_eventos = len(df_selected_mes['Bitácora'])
            total_recuperados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'RECUPERADO']
            total_recuperados1 = len(total_recuperados)
            total_consumados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'CONSUMADO']
            total_consumados1 = len(total_consumados)
            total_frustrados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'FRUSTRADO']
            total_frustrados1 = len(total_frustrados)
            total_pendientes = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'PENDIENTE']
            total_pendientes1 = len(total_pendientes)
            total_noaplica = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'NO APLICA']
            total_noaplica1 = len(total_noaplica)
    
            c4, c5, c6, c7, c8, c9 = st.columns(6)
            with c4:
                st.metric("Eventos", f"{total_eventos}")
            with c5:
                st.metric("Recuperados", f"{total_recuperados1}")
            with c6:
                st.metric("Consumados", f"{total_consumados1}")
            with c7:
                st.metric("Frustrados", f"{total_frustrados1}")
            with c8:
                st.metric("Pendientes", f"{total_pendientes1}")
            with c9:
                st.metric("No Aplica", f"{total_noaplica1}")

            # Diagrama Sankey
            #st.markdown("<h3 style='text-align: left;'>Flujo de Eventos</h3>", unsafe_allow_html=True)

            dSankey = df_selected_mes.groupby(['Motivo de Entrada','Estado']).aggregate({'Estatus':'count'}).reset_index()

            fig = genSankey(dSankey,cat_cols=['Motivo de Entrada','Estado','Estatus'],value_cols='Estatus',title='Flujo de Eventos AInsurance')
            st.plotly_chart(fig, use_container_width=True)

            # Indicadores

            st.markdown("<h3 style='text-align: left;'>Indicadores</h3>", unsafe_allow_html=True)
    
            st.markdown("<h5 style='text-align: left;'>Gráfico Mensual de Intentos de Robos</h5>", unsafe_allow_html=True)
            d1 = df_grafico(df_selected_mes)

            g1 = g_recuperacion(d1)
    
            st.markdown("<h5 style='text-align: left;'>Segmentación de Intentos de Robos</h5>", unsafe_allow_html=True)
            df_pie = df_selected_mes.groupby(['Estatus']).size()
            df_pie1 = pd.DataFrame(df_pie)
            df_pie1.reset_index(drop = False, inplace = True)
            df_pie1 = df_pie1.rename(columns={'Estatus':'Tipo de Evento', 0:'Total'})
            plt.figure(figsize = (10,10))
            fig = px.pie(df_pie1, values='Total', names='Tipo de Evento')
            st.plotly_chart(fig, use_container_width=True)

    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.") 
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk6")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            #Mapa Coropleta
            mapa = map_coropleta_fol(df_selected_mes2)
            c13, c14, c15, c16, c17 = st.columns([1,1,1,1,1])
            with c15:
                export_mapa = st.button("Descargar Mapa")
                if export_mapa:
                    mapa.save("mapa.html")
                    st.success("¡Mapa Descargado!")

    elif username == 'cgalan':
        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Data Visualización","Mapa de Calor"))
        # Realizar auditorías seleccionadas
        
        if options=="Data Visualización":
            
            df = pd.DataFrame(obtener_df())
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y', errors='coerce')
            df['Año'] = df['Fecha'].apply(lambda x: x.year)
            df['MesN'] = df['Fecha'].apply(lambda x: x.month)
            df['Mes'] = df['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
    
            st.markdown("<h2 style='text-align: left;'>Visualización de Datos del Histórico de Eventos</h2>", unsafe_allow_html=True)
            st.write(f"Marco de datos del histórico de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df.Mes.min()} {df.Año.min().astype(int)}*** a ***{df.Mes.max()} {df.Año.max().astype(int)}***.")
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                container1 = st.container()
                allC1 = st.checkbox("Seleccionar Todos", key="chk1")
                if allC1:
                    sorted_unique_cliente = sorted(df['Cliente'].unique())
                    selected_cliente = container1.multiselect('Cliente(es):', sorted_unique_cliente, sorted_unique_cliente, key="cliente1")
                    df_selected_cliente = df[df['Cliente'].isin(selected_cliente)].astype(str)
                else:
                    sorted_unique_cliente = sorted(df['Cliente'].unique())
                    selected_cliente = container1.multiselect('Cliente(es)', sorted_unique_cliente, key="cliente2")
                    df_selected_cliente = df[df['Cliente'].isin(selected_cliente)].astype(str)
        
            with c2:
                container2 = st.container()
                allC2 = st.checkbox("Seleccionar Todos", key="chk2")
                if allC2:
                    sorted_unique_ao = sorted(df_selected_cliente['Año'].unique())
                    selected_ao = container2.multiselect('Año(s):', sorted_unique_ao, sorted_unique_ao, key="año1") 
                    df_selected_ao = df_selected_cliente[df_selected_cliente['Año'].isin(selected_ao)].astype(str)
                else:
                    sorted_unique_ao = sorted(df_selected_cliente['Año'].unique())
                    selected_ao = container2.multiselect('Año(s):', sorted_unique_ao, key="año2") 
                    df_selected_ao = df_selected_cliente[df_selected_cliente['Año'].isin(selected_ao)].astype(str)
    
            with c3:
                container3 = st.container()
                allC3 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC3:
                    sorted_unique_mes = sorted(df_selected_ao['Mes'].unique())
                    selected_mes = container3.multiselect('Mes(es):', sorted_unique_mes, sorted_unique_mes, key="mes1") 
                    df_selected_mes = df_selected_ao[df_selected_ao['Mes'].isin(selected_mes)].astype(str)
                else:
                    sorted_unique_mes = sorted(df_selected_ao['Mes'].unique())
                    selected_mes = container3.multiselect('Mes(es):', sorted_unique_mes, key="mes2") 
                    df_selected_mes = df_selected_ao[df_selected_ao['Mes'].isin(selected_mes)].astype(str)
    
            # Dataframe
            st.markdown("<h5 style='text-align: left;'>Datos históricos de los eventos</h5>", unsafe_allow_html=True)
            df_selected_mes = df_selected_mes[['Fecha', 'Nombre Monitorista', 'Bitácora', 'Cliente', 'Motivo de Entrada', 'Marca', 'Modelo', 'Placas', 'Economico', 'Latitud', 'Longitud', 'Estado', 'Municipio', 'Tramo', 'Estatus', 'Observaciones']]
            st.dataframe(df_selected_mes)
            x1, x2, x3, x4, x5 = st.columns([1,1,1,1,1])
            with x3:
                export1 = st.button("Descargar")
                if export1:
                    df_selected_mes.to_excel("Historico.xlsx")
                    st.success("¡Archivo Descargado!")

            # Métricas
            st.markdown("<h5 style='text-align: left;'>Métricas</h5>", unsafe_allow_html=True)

            total_eventos = len(df_selected_mes['Bitácora'])
            total_recuperados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'RECUPERADO']
            total_recuperados1 = len(total_recuperados)
            total_consumados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'CONSUMADO']
            total_consumados1 = len(total_consumados)
            total_frustrados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'FRUSTRADO']
            total_frustrados1 = len(total_frustrados)
            total_pendientes = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'PENDIENTE']
            total_pendientes1 = len(total_pendientes)
            total_noaplica = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'NO APLICA']
            total_noaplica1 = len(total_noaplica)
    
            c4, c5, c6, c7, c8, c9 = st.columns(6)
            with c4:
                st.metric("Eventos", f"{total_eventos}")
            with c5:
                st.metric("Recuperados", f"{total_recuperados1}")
            with c6:
                st.metric("Consumados", f"{total_consumados1}")
            with c7:
                st.metric("Frustrados", f"{total_frustrados1}")
            with c8:
                st.metric("Pendientes", f"{total_pendientes1}")
            with c9:
                st.metric("No Aplica", f"{total_noaplica1}")
            
            # Diagrama Sankey
            #st.markdown("<h3 style='text-align: left;'>Flujo de Eventos</h3>", unsafe_allow_html=True)

            dSankey = df_selected_mes.groupby(['Motivo de Entrada','Estado']).aggregate({'Estatus':'count'}).reset_index()

            fig = genSankey(dSankey,cat_cols=['Motivo de Entrada','Estado','Estatus'],value_cols='Estatus',title='Flujo de Eventos AInsurance')
            st.plotly_chart(fig, use_container_width=True)

            # Indicadores

            st.markdown("<h3 style='text-align: left;'>Indicadores</h3>", unsafe_allow_html=True)
    
            st.markdown("<h5 style='text-align: left;'>Gráfico Mensual de Intentos de Robos</h5>", unsafe_allow_html=True)
            d1 = df_grafico(df_selected_mes)

            g1 = g_recuperacion(d1)
    
            st.markdown("<h5 style='text-align: left;'>Segmentación de Intentos de Robos</h5>", unsafe_allow_html=True)
            df_pie = df_selected_mes.groupby(['Estatus']).size()
            df_pie1 = pd.DataFrame(df_pie)
            df_pie1.reset_index(drop = False, inplace = True)
            df_pie1 = df_pie1.rename(columns={'Estatus':'Tipo de Evento', 0:'Total'})
            plt.figure(figsize = (10,10))
            fig = px.pie(df_pie1, values='Total', names='Tipo de Evento')
            st.plotly_chart(fig, use_container_width=True)

    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")

            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)

            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk6")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            #Mapa Coropleta
            mapa = map_coropleta_fol(df_selected_mes2)
            c13, c14, c15, c16, c17 = st.columns([1,1,1,1,1])
            with c15:
                export = st.button("Descargar")
                if export:
                    mapa.save("mapa.html")
                    st.success("¡Mapa Descargado!")

    elif username == 'fmartinez':
        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Data Visualización","Mapa de Calor"))
        # Realizar auditorías seleccionadas
        
        if options=="Data Visualización":
            
            df = pd.DataFrame(obtener_df())
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y', errors='coerce')
            df['Año'] = df['Fecha'].apply(lambda x: x.year)
            df['MesN'] = df['Fecha'].apply(lambda x: x.month)
            df['Mes'] = df['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
    
            st.markdown("<h2 style='text-align: left;'>Visualización de Datos del Histórico de Eventos</h2>", unsafe_allow_html=True)
            st.write(f"Marco de datos del histórico de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df.Mes.min()} {df.Año.min().astype(int)}*** a ***{df.Mes.max()} {df.Año.max().astype(int)}***.")
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                container1 = st.container()
                allC1 = st.checkbox("Seleccionar Todos", key="chk1")
                if allC1:
                    sorted_unique_cliente = sorted(df['Cliente'].unique())
                    selected_cliente = container1.multiselect('Cliente(es):', sorted_unique_cliente, sorted_unique_cliente, key="cliente1")
                    df_selected_cliente = df[df['Cliente'].isin(selected_cliente)].astype(str)
                else:
                    sorted_unique_cliente = sorted(df['Cliente'].unique())
                    selected_cliente = container1.multiselect('Cliente(es)', sorted_unique_cliente, key="cliente2")
                    df_selected_cliente = df[df['Cliente'].isin(selected_cliente)].astype(str)
        
            with c2:
                container2 = st.container()
                allC2 = st.checkbox("Seleccionar Todos", key="chk2")
                if allC2:
                    sorted_unique_ao = sorted(df_selected_cliente['Año'].unique())
                    selected_ao = container2.multiselect('Año(s):', sorted_unique_ao, sorted_unique_ao, key="año1") 
                    df_selected_ao = df_selected_cliente[df_selected_cliente['Año'].isin(selected_ao)].astype(str)
                else:
                    sorted_unique_ao = sorted(df_selected_cliente['Año'].unique())
                    selected_ao = container2.multiselect('Año(s):', sorted_unique_ao, key="año2") 
                    df_selected_ao = df_selected_cliente[df_selected_cliente['Año'].isin(selected_ao)].astype(str)
    
            with c3:
                container3 = st.container()
                allC3 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC3:
                    sorted_unique_mes = sorted(df_selected_ao['Mes'].unique())
                    selected_mes = container3.multiselect('Mes(es):', sorted_unique_mes, sorted_unique_mes, key="mes1") 
                    df_selected_mes = df_selected_ao[df_selected_ao['Mes'].isin(selected_mes)].astype(str)
                else:
                    sorted_unique_mes = sorted(df_selected_ao['Mes'].unique())
                    selected_mes = container3.multiselect('Mes(es):', sorted_unique_mes, key="mes2") 
                    df_selected_mes = df_selected_ao[df_selected_ao['Mes'].isin(selected_mes)].astype(str)
    
            # Dataframe
            st.markdown("<h5 style='text-align: left;'>Datos históricos de los eventos</h5>", unsafe_allow_html=True)
            df_selected_mes = df_selected_mes[['Fecha', 'Nombre Monitorista', 'Bitácora', 'Cliente', 'Motivo de Entrada', 'Marca', 'Modelo', 'Placas', 'Economico', 'Latitud', 'Longitud', 'Estado', 'Municipio', 'Tramo', 'Estatus', 'Observaciones']]
            st.dataframe(df_selected_mes)
            x1, x2, x3, x4, x5 = st.columns([1,1,1,1,1])
            with x3:
                export1 = st.button("Descargar")
                if export1:
                    df_selected_mes.to_excel("Historico.xlsx")
                    st.success("¡Archivo Descargado!")

            # Métricas
            st.markdown("<h5 style='text-align: left;'>Métricas</h5>", unsafe_allow_html=True)

            total_eventos = len(df_selected_mes['Bitácora'])
            total_recuperados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'RECUPERADO']
            total_recuperados1 = len(total_recuperados)
            total_consumados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'CONSUMADO']
            total_consumados1 = len(total_consumados)
            total_frustrados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'FRUSTRADO']
            total_frustrados1 = len(total_frustrados)
            total_pendientes = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'PENDIENTE']
            total_pendientes1 = len(total_pendientes)
            total_noaplica = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'NO APLICA']
            total_noaplica1 = len(total_noaplica)
    
            c4, c5, c6, c7, c8, c9 = st.columns(6)
            with c4:
                st.metric("Eventos", f"{total_eventos}")
            with c5:
                st.metric("Recuperados", f"{total_recuperados1}")
            with c6:
                st.metric("Consumados", f"{total_consumados1}")
            with c7:
                st.metric("Frustrados", f"{total_frustrados1}")
            with c8:
                st.metric("Pendientes", f"{total_pendientes1}")
            with c9:
                st.metric("No Aplica", f"{total_noaplica1}")
            
            # Diagrama Sankey
            #st.markdown("<h3 style='text-align: left;'>Flujo de Eventos</h3>", unsafe_allow_html=True)

            dSankey = df_selected_mes.groupby(['Motivo de Entrada','Estado']).aggregate({'Estatus':'count'}).reset_index()

            fig = genSankey(dSankey,cat_cols=['Motivo de Entrada','Estado','Estatus'],value_cols='Estatus',title='Flujo de Eventos AInsurance')
            st.plotly_chart(fig, use_container_width=True)

            # Indicadores

            st.markdown("<h3 style='text-align: left;'>Indicadores</h3>", unsafe_allow_html=True)
    
            st.markdown("<h5 style='text-align: left;'>Gráfico Mensual de Intentos de Robos</h5>", unsafe_allow_html=True)
            d1 = df_grafico(df_selected_mes)

            g1 = g_recuperacion(d1)
    
            st.markdown("<h5 style='text-align: left;'>Segmentación de Intentos de Robos</h5>", unsafe_allow_html=True)
            df_pie = df_selected_mes.groupby(['Estatus']).size()
            df_pie1 = pd.DataFrame(df_pie)
            df_pie1.reset_index(drop = False, inplace = True)
            df_pie1 = df_pie1.rename(columns={'Estatus':'Tipo de Evento', 0:'Total'})
            plt.figure(figsize = (10,10))
            fig = px.pie(df_pie1, values='Total', names='Tipo de Evento')
            st.plotly_chart(fig, use_container_width=True)

    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")

            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)

            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk6")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            #Mapa Coropleta
            mapa = map_coropleta_fol(df_selected_mes2)
            c13, c14, c15, c16, c17 = st.columns([1,1,1,1,1])
            with c15:
                export = st.button("Descargar")
                if export:
                    mapa.save("mapa.html")
                    st.success("¡Mapa Descargado!")
    
    elif username == 'mvillareal':
        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Data Visualización","Mapa de Calor"))
        # Realizar auditorías seleccionadas
        
        if options=="Data Visualización":
            
            df = pd.DataFrame(obtener_df())
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d-%m-%Y', errors='coerce')
            df['Año'] = df['Fecha'].apply(lambda x: x.year)
            df['MesN'] = df['Fecha'].apply(lambda x: x.month)
            df['Mes'] = df['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
    
            st.markdown("<h2 style='text-align: left;'>Visualización de Datos del Histórico de Eventos</h2>", unsafe_allow_html=True)
            st.write(f"Marco de datos del histórico de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df.Mes.min()} {df.Año.min().astype(int)}*** a ***{df.Mes.max()} {df.Año.max().astype(int)}***.")
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                container1 = st.container()
                allC1 = st.checkbox("Seleccionar Todos", key="chk1")
                if allC1:
                    sorted_unique_cliente = sorted(df['Cliente'].unique())
                    selected_cliente = container1.multiselect('Cliente(es):', sorted_unique_cliente, sorted_unique_cliente, key="cliente1")
                    df_selected_cliente = df[df['Cliente'].isin(selected_cliente)].astype(str)
                else:
                    sorted_unique_cliente = sorted(df['Cliente'].unique())
                    selected_cliente = container1.multiselect('Cliente(es)', sorted_unique_cliente, key="cliente2")
                    df_selected_cliente = df[df['Cliente'].isin(selected_cliente)].astype(str)
        
            with c2:
                container2 = st.container()
                allC2 = st.checkbox("Seleccionar Todos", key="chk2")
                if allC2:
                    sorted_unique_ao = sorted(df_selected_cliente['Año'].unique())
                    selected_ao = container2.multiselect('Año(s):', sorted_unique_ao, sorted_unique_ao, key="año1") 
                    df_selected_ao = df_selected_cliente[df_selected_cliente['Año'].isin(selected_ao)].astype(str)
                else:
                    sorted_unique_ao = sorted(df_selected_cliente['Año'].unique())
                    selected_ao = container2.multiselect('Año(s):', sorted_unique_ao, key="año2") 
                    df_selected_ao = df_selected_cliente[df_selected_cliente['Año'].isin(selected_ao)].astype(str)
    
            with c3:
                container3 = st.container()
                allC3 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC3:
                    sorted_unique_mes = sorted(df_selected_ao['Mes'].unique())
                    selected_mes = container3.multiselect('Mes(es):', sorted_unique_mes, sorted_unique_mes, key="mes1") 
                    df_selected_mes = df_selected_ao[df_selected_ao['Mes'].isin(selected_mes)].astype(str)
                else:
                    sorted_unique_mes = sorted(df_selected_ao['Mes'].unique())
                    selected_mes = container3.multiselect('Mes(es):', sorted_unique_mes, key="mes2") 
                    df_selected_mes = df_selected_ao[df_selected_ao['Mes'].isin(selected_mes)].astype(str)
    
            # Dataframe
            st.markdown("<h5 style='text-align: left;'>Datos históricos de los eventos</h5>", unsafe_allow_html=True)
            df_selected_mes = df_selected_mes[['Fecha', 'Nombre Monitorista', 'Bitácora', 'Cliente', 'Motivo de Entrada', 'Marca', 'Modelo', 'Placas', 'Economico', 'Latitud', 'Longitud', 'Estado', 'Municipio', 'Tramo', 'Estatus', 'Observaciones']]
            st.dataframe(df_selected_mes)
            x1, x2, x3, x4, x5 = st.columns([1,1,1,1,1])
            with x3:
                export1 = st.button("Descargar")
                if export1:
                    df_selected_mes.to_excel("Historico.xlsx")
                    st.success("¡Archivo Descargado!")

            # Métricas
            st.markdown("<h5 style='text-align: left;'>Métricas</h5>", unsafe_allow_html=True)

            total_eventos = len(df_selected_mes['Bitácora'])
            total_recuperados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'RECUPERADO']
            total_recuperados1 = len(total_recuperados)
            total_consumados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'CONSUMADO']
            total_consumados1 = len(total_consumados)
            total_frustrados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'FRUSTRADO']
            total_frustrados1 = len(total_frustrados)
            total_pendientes = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'PENDIENTE']
            total_pendientes1 = len(total_pendientes)
            total_noaplica = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'NO APLICA']
            total_noaplica1 = len(total_noaplica)
    
            c4, c5, c6, c7, c8, c9 = st.columns(6)
            with c4:
                st.metric("Eventos", f"{total_eventos}")
            with c5:
                st.metric("Recuperados", f"{total_recuperados1}")
            with c6:
                st.metric("Consumados", f"{total_consumados1}")
            with c7:
                st.metric("Frustrados", f"{total_frustrados1}")
            with c8:
                st.metric("Pendientes", f"{total_pendientes1}")
            with c9:
                st.metric("No Aplica", f"{total_noaplica1}")
            
            # Diagrama Sankey
            #st.markdown("<h3 style='text-align: left;'>Flujo de Eventos</h3>", unsafe_allow_html=True)

            dSankey = df_selected_mes.groupby(['Motivo de Entrada','Estado']).aggregate({'Estatus':'count'}).reset_index()

            fig = genSankey(dSankey,cat_cols=['Motivo de Entrada','Estado','Estatus'],value_cols='Estatus',title='Flujo de Eventos AInsurance')
            st.plotly_chart(fig, use_container_width=True)

            # Indicadores

            st.markdown("<h3 style='text-align: left;'>Indicadores</h3>", unsafe_allow_html=True)
    
            st.markdown("<h5 style='text-align: left;'>Gráfico Mensual de Intentos de Robos</h5>", unsafe_allow_html=True)
            d1 = df_grafico(df_selected_mes)

            g1 = g_recuperacion(d1)
    
            st.markdown("<h5 style='text-align: left;'>Segmentación de Intentos de Robos</h5>", unsafe_allow_html=True)
            df_pie = df_selected_mes.groupby(['Estatus']).size()
            df_pie1 = pd.DataFrame(df_pie)
            df_pie1.reset_index(drop = False, inplace = True)
            df_pie1 = df_pie1.rename(columns={'Estatus':'Tipo de Evento', 0:'Total'})
            plt.figure(figsize = (10,10))
            fig = px.pie(df_pie1, values='Total', names='Tipo de Evento')
            st.plotly_chart(fig, use_container_width=True)

    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")

            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)

            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk6")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            #Mapa Coropleta
            mapa = map_coropleta_fol(df_selected_mes2)
            c13, c14, c15, c16, c17 = st.columns([1,1,1,1,1])
            with c15:
                export = st.button("Descargar")
                if export:
                    mapa.save("mapa.html")
                    st.success("¡Mapa Descargado!")
    
    elif username == 'dramos':
        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Registro y Edición de Eventos","Mapa de Calor"))
        # Realizar auditorías seleccionadas

        if options=="Registro y Edición de Eventos":
            
            st.markdown("<h2 style='text-align: left;'>Registro de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Registrar eventos de los servicios (Bitácoras) que fueron detonados como emergencia por los clientes AInsurance de AI27.")

            # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
            date = datetime.today()
            #usr = name
            cliente = ["SITRACK", "AUTOFLETES CHIHUAHUA", "TGT", "MAEDA", "MAVERICK", "TRANSPORTES MENDEZ","SETRAMEX"]
            notificacion = ["Llamada del Cliente", "Whatsapp del Cliente", "Alerta por Telegram", "Bitácora Centro Monitoreo", "Correo del Cliente"]
            marcatracto = ["KENWORTH", "INTERNACIONAL", "FREIGHTLINER", "VOLVO", "MERCEDES"]
            estado = ["Ciudad de México", "México", "Querétaro", "Puebla", "Guanajuato", "Veracruz", "Chiapas", "Jalisco", "Durango", "Hidalgo", "San Luis Potosí", "Nuevo León", "Chihuahua","Campeche", "Sonora","Zacatecas", "Sinaloa", "Tamaulipas", "Oaxaca", "Tabasco", "Michoacán", "Colima", "Guerrero", "Tlaxcala", "Morelos", "Baja California", "Quintana Roo", "Yucatán", "Aguascalientes", "Coahuila", "Nayarit"]
            estatus = ["RECUPERADO", "CONSUMADO", "FRUSTADO", "PENDIENTE","NO APLICA"]

            with st.form("entry_form", clear_on_submit= True):
                col7, col8, col9, col10, col11 = st.columns([1,1,1,1,1])
                with col7:
                    fecha = st.text_input("Fecha:", placeholder="Fecha del Evento", key="fecha1")
                with col8:
                    ndocumentador = st.text_input("Nombre Monitorista:", name, disabled=True, key="name1")
                with col9:
                    nBitacora = st.text_input("Bitácora:", placeholder="Nro Bitácora", key="bitacora1")
                with col10:
                    sCliente = st.selectbox("Cliente:", cliente, placeholder="Nombre Cliente", key="cliente1")
                with col11: 
                    mEntrada = st.selectbox("Motivo de Entrada:", notificacion, placeholder="Tipo de Notificación", key="notificacion1")
                col12, col13, col14, col15, col16 = st.columns([1,1,1,1,1])   
                with col12: 
                    marca = st.selectbox("Marca:", marcatracto, placeholder="Marca del Tracto", key="marca1")
                with col13: 
                    modelo = st.text_input("Modelo:", placeholder="Año del Tracto", key="ao1")
                with col14: 
                    placas = st.text_input("Placas:", placeholder="Placas del Tracto", key="placas1")
                with col15:
                    economico = st.text_input("Económico:", placeholder="Número Económico", key="economico1")
                with col16:    
                    latitud = st.text_input("Latitud:", placeholder="Latitud", key="latitud1")
                col17, col18, col19, col20, col21, = st.columns([1,1,1,1,1])
                with col17:    
                    longitud = st.text_input("Longitud:", placeholder="Longitud", key="longitud1")
                with col18:
                    estado = st.selectbox("Estado:", estado, key="estado1")
                with col19:    
                    municipio = st.text_input("Municipio:", placeholder="Municipio", key="municipio")
                with col20:    
                    tramo = st.text_input("Tramo:", placeholder="Tramo Carretero", key="tramo1")
                with col21:    
                    estatus = st.selectbox("Estatus:", estatus, key="estatus1")

                coment = st.text_area("Observaciones:", placeholder="Escriba Observaciones ...", key= "coments1")
                "---"
                col19, col20, col21, col22, col23 = st.columns([1,1,1,1,1])
                with col21:
                    submitted = st.form_submit_button("Guardar")
                    if submitted:
                        ainsurance_db.insert_register_ainsurance(fecha, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)
                        st.success("¡Guardado!")

            st.markdown("<h2 style='text-align: left;'>Edición de Marco de Datos de los Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Marco de datos para editar eventos de los servicios (Bitácoras) AInsurance de AI27 registrados con errores o cambios de estatus posteriores.")
            
            elementos = ainsurance_db.fetch_all_ainsurance()
            if len(elementos) < 1:
                df1 = pd.DataFrame(columns=DF_HEADER)
            else:
                df1 = pd.DataFrame(elementos)

            # Hide the key in display. In Deta db, the key is the username.
            edited_df = st.data_editor(
                df1,
                num_rows="dynamic",
                key='account',
                column_config={"key": None}
            )
            col24, col25, col26, col27, col28, col29 = st.columns([1,1,1,1,1,1])
            with col26:
                if st.button("Actualizar"):
                    ainsurance_db.put_new_register(edited_df)
            with col27:
                export1 = st.button("Descargar")
                if export1:
                    edited_df.to_excel("Historico.xlsx")
                    st.success("¡Archivo Descargado!")
    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")

            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            #Mapa Coropleta
            mapa = map_coropleta_fol(df_selected_mes2)
            c13, c14, c15, c16, c17 = st.columns([1,1,1,1,1])
            with c15:
                export = st.button("Descargar")
                if export:
                    mapa.save('mapa.html')
                    st.success("¡Mapa Descargado!")

    elif username == 'sdominguez':
        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Registro y Edición de Eventos","Mapa de Calor"))
        # Realizar auditorías seleccionadas

        if options=="Registro y Edición de Eventos":
            
            st.markdown("<h2 style='text-align: left;'>Registro de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Registrar eventos de los servicios (Bitácoras) que fueron detonados como emergencia por los clientes AInsurance de AI27.")

            # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
            date = datetime.today()
            #usr = name
            cliente = ["SITRACK", "AUTOFLETES CHIHUAHUA", "TGT", "MAEDA", "MAVERICK", "TRANSPORTES MENDEZ","SETRAMEX"]
            notificacion = ["Llamada del Cliente", "Whatsapp del Cliente", "Alerta por Telegram", "Bitácora Centro Monitoreo", "Correo del Cliente"]
            marcatracto = ["KENWORTH", "INTERNACIONAL", "FREIGHTLINER", "VOLVO", "MERCEDES"]
            estado = ["Ciudad de México", "México", "Querétaro", "Puebla", "Guanajuato", "Veracruz", "Chiapas", "Jalisco", "Durango", "Hidalgo", "San Luis Potosí", "Nuevo León", "Chihuahua","Campeche", "Sonora","Zacatecas", "Sinaloa", "Tamaulipas", "Oaxaca", "Tabasco", "Michoacán", "Colima", "Guerrero", "Tlaxcala", "Morelos", "Baja California", "Quintana Roo", "Yucatán", "Aguascalientes", "Coahuila", "Nayarit"]
            estatus = ["RECUPERADO", "CONSUMADO", "FRUSTADO", "PENDIENTE","NO APLICA"]

            with st.form("entry_form", clear_on_submit= True):
                col7, col8, col9, col10, col11 = st.columns([1,1,1,1,1])
                with col7:
                    fecha = st.text_input("Fecha:", placeholder="Fecha del Evento", key="fecha1")
                with col8:
                    ndocumentador = st.text_input("Nombre Monitorista:", name, disabled=True, key="name1")
                with col9:
                    nBitacora = st.text_input("Bitácora:", placeholder="Nro Bitácora", key="bitacora1")
                with col10:
                    sCliente = st.selectbox("Cliente:", cliente, placeholder="Nombre Cliente", key="cliente1")
                with col11: 
                    mEntrada = st.selectbox("Motivo de Entrada:", notificacion, placeholder="Tipo de Notificación", key="notificacion1")
                col12, col13, col14, col15, col16 = st.columns([1,1,1,1,1])   
                with col12: 
                    marca = st.selectbox("Marca:", marcatracto, placeholder="Marca del Tracto", key="marca1")
                with col13: 
                    modelo = st.text_input("Modelo:", placeholder="Año del Tracto", key="ao1")
                with col14: 
                    placas = st.text_input("Placas:", placeholder="Placas del Tracto", key="placas1")
                with col15:
                    economico = st.text_input("Económico:", placeholder="Número Económico", key="economico1")
                with col16:    
                    latitud = st.text_input("Latitud:", placeholder="Latitud", key="latitud1")
                col17, col18, col19, col20, col21, = st.columns([1,1,1,1,1])
                with col17:    
                    longitud = st.text_input("Longitud:", placeholder="Longitud", key="longitud1")
                with col18:
                    estado = st.selectbox("Estado:", estado, key="estado1")
                with col19:    
                    municipio = st.text_input("Municipio:", placeholder="Municipio", key="municipio")
                with col20:    
                    tramo = st.text_input("Tramo:", placeholder="Tramo Carretero", key="tramo1")
                with col21:    
                    estatus = st.selectbox("Estatus:", estatus, key="estatus1")

                coment = st.text_area("Observaciones:", placeholder="Escriba Observaciones ...", key= "coments1")
                "---"
                col19, col20, col21, col22, col23 = st.columns([1,1,1,1,1])
                with col21:
                    submitted = st.form_submit_button("Guardar")
                    if submitted:
                        ainsurance_db.insert_register_ainsurance(fecha, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)
                        st.success("¡Guardado!")


            st.markdown("<h2 style='text-align: left;'>Edición de Marco de Datos de los Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Marco de datos para editar eventos de los servicios (Bitácoras) AInsurance de AI27 registrados con errores o cambios de estatus posteriores.")
            
            elementos = ainsurance_db.fetch_all_ainsurance()
            if len(elementos) < 1:
                df1 = pd.DataFrame(columns=DF_HEADER)
            else:
                df1 = pd.DataFrame(elementos)

            # Hide the key in display. In Deta db, the key is the username.
            edited_df = st.data_editor(
                df1,
                num_rows="dynamic",
                key='account',
                column_config={"key": None}
            )
            col24, col25, col26, col27, col28, col29 = st.columns([1,1,1,1,1,1])
            with col26:
                if st.button("Actualizar"):
                    ainsurance_db.put_new_register(edited_df)
            with col27:
                export1 = st.button("Descargar")
                if export1:
                    edited_df.to_excel("Historico.xlsx")
                    st.success("¡Archivo Descargado!")
    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            #Mapa Coropleta
            mapa = map_coropleta_fol(df_selected_mes2)
            c13, c14, c15, c16, c17 = st.columns([1,1,1,1,1])
            with c15:
                export = st.button("Descargar")
                if export:
                    mapa.save("mapa.html")
                    st.success("¡Mapa Descargado!")
    
    elif username == 'djarquin':

        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Registro y Edición de Eventos","Mapa de Calor"))
        # Realizar auditorías seleccionadas

        if options=="Registro y Edición de Eventos":
            
            st.markdown("<h2 style='text-align: left;'>Registro de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Registrar eventos de los servicios (Bitácoras) que fueron detonados como emergencia por los clientes AInsurance de AI27.")

            # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
            date = datetime.today()
            #usr = name
            cliente = ["SITRACK", "AUTOFLETES CHIHUAHUA", "TGT", "MAEDA", "MAVERICK", "TRANSPORTES MENDEZ","SETRAMEX"]
            notificacion = ["Llamada del Cliente", "Whatsapp del Cliente", "Alerta por Telegram", "Bitácora Centro Monitoreo", "Correo del Cliente"]
            marcatracto = ["KENWORTH", "INTERNACIONAL", "FREIGHTLINER", "VOLVO", "MERCEDES"]
            estado = ["Ciudad de México", "México", "Querétaro", "Puebla", "Guanajuato", "Veracruz", "Chiapas", "Jalisco", "Durango", "Hidalgo", "San Luis Potosí", "Nuevo León", "Chihuahua","Campeche", "Sonora","Zacatecas", "Sinaloa", "Tamaulipas", "Oaxaca", "Tabasco", "Michoacán", "Colima", "Guerrero", "Tlaxcala", "Morelos", "Baja California", "Quintana Roo", "Yucatán", "Aguascalientes", "Coahuila", "Nayarit"]
            estatus = ["RECUPERADO", "CONSUMADO", "FRUSTADO", "PENDIENTE","NO APLICA"]

            with st.form("entry_form", clear_on_submit= True):
                col7, col8, col9, col10, col11 = st.columns([1,1,1,1,1])
                with col7:
                    fecha = st.text_input("Fecha:", placeholder="Fecha del Evento", key="fecha1")
                with col8:
                    ndocumentador = st.text_input("Nombre Monitorista:", name, disabled=True, key="name1")
                with col9:
                    nBitacora = st.text_input("Bitácora:", placeholder="Nro Bitácora", key="bitacora1")
                with col10:
                    sCliente = st.selectbox("Cliente:", cliente, placeholder="Nombre Cliente", key="cliente1")
                with col11: 
                    mEntrada = st.selectbox("Motivo de Entrada:", notificacion, placeholder="Tipo de Notificación", key="notificacion1")
                col12, col13, col14, col15, col16 = st.columns([1,1,1,1,1])   
                with col12: 
                    marca = st.selectbox("Marca:", marcatracto, placeholder="Marca del Tracto", key="marca1")
                with col13: 
                    modelo = st.text_input("Modelo:", placeholder="Año del Tracto", key="ao1")
                with col14: 
                    placas = st.text_input("Placas:", placeholder="Placas del Tracto", key="placas1")
                with col15:
                    economico = st.text_input("Económico:", placeholder="Número Económico", key="economico1")
                with col16:    
                    latitud = st.text_input("Latitud:", placeholder="Latitud", key="latitud1")
                col17, col18, col19, col20, col21, = st.columns([1,1,1,1,1])
                with col17:    
                    longitud = st.text_input("Longitud:", placeholder="Longitud", key="longitud1")
                with col18:
                    estado = st.selectbox("Estado:", estado, key="estado1")
                with col19:    
                    municipio = st.text_input("Municipio:", placeholder="Municipio", key="municipio")
                with col20:    
                    tramo = st.text_input("Tramo:", placeholder="Tramo Carretero", key="tramo1")
                with col21:    
                    estatus = st.selectbox("Estatus:", estatus, key="estatus1")

                coment = st.text_area("Observaciones:", placeholder="Escriba Observaciones ...", key= "coments1")
                "---"
                col19, col20, col21, col22, col23 = st.columns([1,1,1,1,1])
                with col21:
                    submitted = st.form_submit_button("Guardar")
                    if submitted:
                        ainsurance_db.insert_register_ainsurance(fecha, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)
                        st.success("¡Guardado!")


            st.markdown("<h2 style='text-align: left;'>Edición de Marco de Datos de los Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Marco de datos para editar eventos de los servicios (Bitácoras) AInsurance de AI27 registrados con errores o cambios de estatus posteriores.")
            
            elementos = ainsurance_db.fetch_all_ainsurance()
            if len(elementos) < 1:
                df1 = pd.DataFrame(columns=DF_HEADER)
            else:
                df1 = pd.DataFrame(elementos)

            # Hide the key in display. In Deta db, the key is the username.
            edited_df = st.data_editor(
                df1,
                num_rows="dynamic",
                key='account',
                column_config={"key": None}
            )
            col24, col25, col26, col27, col28, col29 = st.columns([1,1,1,1,1,1])
            with col26:
                if st.button("Actualizar"):
                    ainsurance_db.put_new_register(edited_df)
            with col27:
                export1 = st.button("Descargar")
                if export1:
                    edited_df.to_excel("Historico.xlsx")
                    st.success("¡Archivo Descargado!")
    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            #Mapa Coropleta
            mapa = map_coropleta_fol(df_selected_mes2)
            c13, c14, c15, c16, c17 = st.columns([1,1,1,1,1])
            with c15:
                export = st.button("Descargar")
                if export:
                    mapa.save("mapa.html")
                    st.success("¡Mapa Descargado!")
    
    elif username == 'fnicolas':
        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Registro y Edición de Eventos","Mapa de Calor"))
        # Realizar auditorías seleccionadas

        if options=="Registro y Edición de Eventos":
            
            st.markdown("<h2 style='text-align: left;'>Registro de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Registrar eventos de los servicios (Bitácoras) que fueron detonados como emergencia por los clientes AInsurance de AI27.")

            # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
            date = datetime.today()
            #usr = name
            cliente = ["SITRACK", "AUTOFLETES CHIHUAHUA", "TGT", "MAEDA", "MAVERICK", "TRANSPORTES MENDEZ","SETRAMEX"]
            notificacion = ["Llamada del Cliente", "Whatsapp del Cliente", "Alerta por Telegram", "Bitácora Centro Monitoreo", "Correo del Cliente"]
            marcatracto = ["KENWORTH", "INTERNACIONAL", "FREIGHTLINER", "VOLVO", "MERCEDES"]
            estado = ["Ciudad de México", "México", "Querétaro", "Puebla", "Guanajuato", "Veracruz", "Chiapas", "Jalisco", "Durango", "Hidalgo", "San Luis Potosí", "Nuevo León", "Chihuahua","Campeche", "Sonora","Zacatecas", "Sinaloa", "Tamaulipas", "Oaxaca", "Tabasco", "Michoacán", "Colima", "Guerrero", "Tlaxcala", "Morelos", "Baja California", "Quintana Roo", "Yucatán", "Aguascalientes", "Coahuila", "Nayarit"]
            estatus = ["RECUPERADO", "CONSUMADO", "FRUSTADO", "PENDIENTE","NO APLICA"]

            with st.form("entry_form", clear_on_submit= True):
                col7, col8, col9, col10, col11 = st.columns([1,1,1,1,1])
                with col7:
                    fecha = st.text_input("Fecha:", placeholder="Fecha del Evento", key="fecha1")
                with col8:
                    ndocumentador = st.text_input("Nombre Monitorista:", name, disabled=True, key="name1")
                with col9:
                    nBitacora = st.text_input("Bitácora:", placeholder="Nro Bitácora", key="bitacora1")
                with col10:
                    sCliente = st.selectbox("Cliente:", cliente, placeholder="Nombre Cliente", key="cliente1")
                with col11: 
                    mEntrada = st.selectbox("Motivo de Entrada:", notificacion, placeholder="Tipo de Notificación", key="notificacion1")
                col12, col13, col14, col15, col16 = st.columns([1,1,1,1,1])   
                with col12: 
                    marca = st.selectbox("Marca:", marcatracto, placeholder="Marca del Tracto", key="marca1")
                with col13: 
                    modelo = st.text_input("Modelo:", placeholder="Año del Tracto", key="ao1")
                with col14: 
                    placas = st.text_input("Placas:", placeholder="Placas del Tracto", key="placas1")
                with col15:
                    economico = st.text_input("Económico:", placeholder="Número Económico", key="economico1")
                with col16:    
                    latitud = st.text_input("Latitud:", placeholder="Latitud", key="latitud1")
                col17, col18, col19, col20, col21, = st.columns([1,1,1,1,1])
                with col17:    
                    longitud = st.text_input("Longitud:", placeholder="Longitud", key="longitud1")
                with col18:
                    estado = st.selectbox("Estado:", estado, key="estado1")
                with col19:    
                    municipio = st.text_input("Municipio:", placeholder="Municipio", key="municipio")
                with col20:    
                    tramo = st.text_input("Tramo:", placeholder="Tramo Carretero", key="tramo1")
                with col21:    
                    estatus = st.selectbox("Estatus:", estatus, key="estatus1")

                coment = st.text_area("Observaciones:", placeholder="Escriba Observaciones ...", key= "coments1")
                "---"
                col19, col20, col21, col22, col23 = st.columns([1,1,1,1,1])
                with col21:
                    submitted = st.form_submit_button("Guardar")
                    if submitted:
                        ainsurance_db.insert_register_ainsurance(fecha, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)
                        st.success("¡Guardado!")


            st.markdown("<h2 style='text-align: left;'>Edición de Marco de Datos de los Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Marco de datos para editar eventos de los servicios (Bitácoras) AInsurance de AI27 registrados con errores o cambios de estatus posteriores.")
            
            elementos = ainsurance_db.fetch_all_ainsurance()
            if len(elementos) < 1:
                df1 = pd.DataFrame(columns=DF_HEADER)
            else:
                df1 = pd.DataFrame(elementos)

            # Hide the key in display. In Deta db, the key is the username.
            edited_df = st.data_editor(
                df1,
                num_rows="dynamic",
                key='account',
                column_config={"key": None}
            )
            col24, col25, col26, col27, col28, col29 = st.columns([1,1,1,1,1,1])
            with col26:
                if st.button("Actualizar"):
                    ainsurance_db.put_new_register(edited_df)
            with col27:
                export1 = st.button("Descargar")
                if export1:
                    edited_df.to_excel("Historico.xlsx")
                    st.success("¡Archivo Descargado!")
    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            #Mapa Coropleta
            mapa = map_coropleta_fol(df_selected_mes2)
            c13, c14, c15, c16, c17 = st.columns([1,1,1,1,1])
            with c15:
                export = st.button("Descargar")
                if export:
                    mapa.save("mapa.html")
                    st.success("¡Mapa Descargado!")

    elif username == 'eromero':
        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Registro de Eventos","Mapa de Calor"))
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
            estatus = ["RECUPERADO", "CONSUMADO", "FRUSTADO", "PENDIENTE","NO APLICA"]

            with st.form("entry_form", clear_on_submit= True):
                col7, col8, col9, col10, col11 = st.columns([1,1,1,1,1])
                with col7:
                    fecha = st.text_input("Fecha:", placeholder="Fecha del Evento", key="fecha1")
                with col8:
                    ndocumentador = st.text_input("Nombre Monitorista:", name, disabled=True, key="name1")
                with col9:
                    nBitacora = st.text_input("Bitácora:", placeholder="Nro Bitácora", key="bitacora1")
                with col10:
                    sCliente = st.selectbox("Cliente:", cliente, placeholder="Nombre Cliente", key="cliente1")
                with col11: 
                    mEntrada = st.selectbox("Motivo de Entrada:", notificacion, placeholder="Tipo de Notificación", key="notificacion1")
                col12, col13, col14, col15, col16 = st.columns([1,1,1,1,1])   
                with col12: 
                    marca = st.selectbox("Marca:", marcatracto, placeholder="Marca del Tracto", key="marca1")
                with col13: 
                    modelo = st.text_input("Modelo:", placeholder="Año del Tracto", key="ao1")
                with col14: 
                    placas = st.text_input("Placas:", placeholder="Placas del Tracto", key="placas1")
                with col15:
                    economico = st.text_input("Económico:", placeholder="Número Económico", key="economico1")
                with col16:    
                    latitud = st.text_input("Latitud:", placeholder="Latitud", key="latitud1")
                col17, col18, col19, col20, col21, = st.columns([1,1,1,1,1])
                with col17:    
                    longitud = st.text_input("Longitud:", placeholder="Longitud", key="longitud1")
                with col18:
                    estado = st.selectbox("Estado:", estado, key="estado1")
                with col19:    
                    municipio = st.text_input("Municipio:", placeholder="Municipio", key="municipio")
                with col20:    
                    tramo = st.text_input("Tramo:", placeholder="Tramo Carretero", key="tramo1")
                with col21:    
                    estatus = st.selectbox("Estatus:", estatus, key="estatus1")

                coment = st.text_area("Observaciones:", placeholder="Escriba Observaciones ...", key= "coments1")
                "---"
                col19, col20, col21, col22, col23 = st.columns([1,1,1,1,1])
                with col21:
                    submitted = st.form_submit_button("Guardar")
                    if submitted:
                        ainsurance_db.insert_register_ainsurance(fecha, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)
                        st.success("¡Guardado!")
    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            mapa = map_coropleta_fol(df_selected_mes2)
    
    elif username == 'cruiz':
        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Registro de Eventos","Mapa de Calor"))
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
            estatus = ["RECUPERADO", "CONSUMADO", "FRUSTADO", "PENDIENTE","NO APLICA"]

            with st.form("entry_form", clear_on_submit= True):
                col7, col8, col9, col10, col11 = st.columns([1,1,1,1,1])
                with col7:
                    fecha = st.text_input("Fecha:", placeholder="Fecha del Evento", key="fecha1")
                with col8:
                    ndocumentador = st.text_input("Nombre Monitorista:", name, disabled=True, key="name1")
                with col9:
                    nBitacora = st.text_input("Bitácora:", placeholder="Nro Bitácora", key="bitacora1")
                with col10:
                    sCliente = st.selectbox("Cliente:", cliente, placeholder="Nombre Cliente", key="cliente1")
                with col11: 
                    mEntrada = st.selectbox("Motivo de Entrada:", notificacion, placeholder="Tipo de Notificación", key="notificacion1")
                col12, col13, col14, col15, col16 = st.columns([1,1,1,1,1])   
                with col12: 
                    marca = st.selectbox("Marca:", marcatracto, placeholder="Marca del Tracto", key="marca1")
                with col13: 
                    modelo = st.text_input("Modelo:", placeholder="Año del Tracto", key="ao1")
                with col14: 
                    placas = st.text_input("Placas:", placeholder="Placas del Tracto", key="placas1")
                with col15:
                    economico = st.text_input("Económico:", placeholder="Número Económico", key="economico1")
                with col16:    
                    latitud = st.text_input("Latitud:", placeholder="Latitud", key="latitud1")
                col17, col18, col19, col20, col21, = st.columns([1,1,1,1,1])
                with col17:    
                    longitud = st.text_input("Longitud:", placeholder="Longitud", key="longitud1")
                with col18:
                    estado = st.selectbox("Estado:", estado, key="estado1")
                with col19:    
                    municipio = st.text_input("Municipio:", placeholder="Municipio", key="municipio")
                with col20:    
                    tramo = st.text_input("Tramo:", placeholder="Tramo Carretero", key="tramo1")
                with col21:    
                    estatus = st.selectbox("Estatus:", estatus, key="estatus1")

                coment = st.text_area("Observaciones:", placeholder="Escriba Observaciones ...", key= "coments1")
                "---"
                col19, col20, col21, col22, col23 = st.columns([1,1,1,1,1])
                with col21:
                    submitted = st.form_submit_button("Guardar")
                    if submitted:
                        ainsurance_db.insert_register_ainsurance(fecha, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)
                        st.success("¡Guardado!")
    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            mapa = map_coropleta_fol(df_selected_mes2)
    
    elif username == 'mponce':
        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Registro de Eventos","Mapa de Calor"))
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
            estatus = ["RECUPERADO", "CONSUMADO", "FRUSTADO", "PENDIENTE","NO APLICA"]

            with st.form("entry_form", clear_on_submit= True):
                col7, col8, col9, col10, col11 = st.columns([1,1,1,1,1])
                with col7:
                    fecha = st.text_input("Fecha:", placeholder="Fecha del Evento", key="fecha1")
                with col8:
                    ndocumentador = st.text_input("Nombre Monitorista:", name, disabled=True, key="name1")
                with col9:
                    nBitacora = st.text_input("Bitácora:", placeholder="Nro Bitácora", key="bitacora1")
                with col10:
                    sCliente = st.selectbox("Cliente:", cliente, placeholder="Nombre Cliente", key="cliente1")
                with col11: 
                    mEntrada = st.selectbox("Motivo de Entrada:", notificacion, placeholder="Tipo de Notificación", key="notificacion1")
                col12, col13, col14, col15, col16 = st.columns([1,1,1,1,1])   
                with col12: 
                    marca = st.selectbox("Marca:", marcatracto, placeholder="Marca del Tracto", key="marca1")
                with col13: 
                    modelo = st.text_input("Modelo:", placeholder="Año del Tracto", key="ao1")
                with col14: 
                    placas = st.text_input("Placas:", placeholder="Placas del Tracto", key="placas1")
                with col15:
                    economico = st.text_input("Económico:", placeholder="Número Económico", key="economico1")
                with col16:    
                    latitud = st.text_input("Latitud:", placeholder="Latitud", key="latitud1")
                col17, col18, col19, col20, col21, = st.columns([1,1,1,1,1])
                with col17:    
                    longitud = st.text_input("Longitud:", placeholder="Longitud", key="longitud1")
                with col18:
                    estado = st.selectbox("Estado:", estado, key="estado1")
                with col19:    
                    municipio = st.text_input("Municipio:", placeholder="Municipio", key="municipio")
                with col20:    
                    tramo = st.text_input("Tramo:", placeholder="Tramo Carretero", key="tramo1")
                with col21:    
                    estatus = st.selectbox("Estatus:", estatus, key="estatus1")

                coment = st.text_area("Observaciones:", placeholder="Escriba Observaciones ...", key= "coments1")
                "---"
                col19, col20, col21, col22, col23 = st.columns([1,1,1,1,1])
                with col21:
                    submitted = st.form_submit_button("Guardar")
                    if submitted:
                        ainsurance_db.insert_register_ainsurance(fecha, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)
                        st.success("¡Guardado!")
    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            mapa = map_coropleta_fol(df_selected_mes2)
    
    elif username == 'fcabrera':

        # Mostrar tipo de auditoria a registrar
        options = st.sidebar.selectbox("Seleccionar Opciones:",("Registro de Eventos","Mapa de Calor"))
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
            estatus = ["RECUPERADO", "CONSUMADO", "FRUSTADO", "PENDIENTE","NO APLICA"]

            with st.form("entry_form", clear_on_submit= True):
                col7, col8, col9, col10, col11 = st.columns([1,1,1,1,1])
                with col7:
                    fecha = st.text_input("Fecha:", placeholder="Fecha del Evento", key="fecha1")
                with col8:
                    ndocumentador = st.text_input("Nombre Monitorista:", name, disabled=True, key="name1")
                with col9:
                    nBitacora = st.text_input("Bitácora:", placeholder="Nro Bitácora", key="bitacora1")
                with col10:
                    sCliente = st.selectbox("Cliente:", cliente, placeholder="Nombre Cliente", key="cliente1")
                with col11: 
                    mEntrada = st.selectbox("Motivo de Entrada:", notificacion, placeholder="Tipo de Notificación", key="notificacion1")
                col12, col13, col14, col15, col16 = st.columns([1,1,1,1,1])   
                with col12: 
                    marca = st.selectbox("Marca:", marcatracto, placeholder="Marca del Tracto", key="marca1")
                with col13: 
                    modelo = st.text_input("Modelo:", placeholder="Año del Tracto", key="ao1")
                with col14: 
                    placas = st.text_input("Placas:", placeholder="Placas del Tracto", key="placas1")
                with col15:
                    economico = st.text_input("Económico:", placeholder="Número Económico", key="economico1")
                with col16:    
                    latitud = st.text_input("Latitud:", placeholder="Latitud", key="latitud1")
                col17, col18, col19, col20, col21, = st.columns([1,1,1,1,1])
                with col17:    
                    longitud = st.text_input("Longitud:", placeholder="Longitud", key="longitud1")
                with col18:
                    estado = st.selectbox("Estado:", estado, key="estado1")
                with col19:    
                    municipio = st.text_input("Municipio:", placeholder="Municipio", key="municipio")
                with col20:    
                    tramo = st.text_input("Tramo:", placeholder="Tramo Carretero", key="tramo1")
                with col21:    
                    estatus = st.selectbox("Estatus:", estatus, key="estatus1")

                coment = st.text_area("Observaciones:", placeholder="Escriba Observaciones ...", key= "coments1")
                "---"
                col19, col20, col21, col22, col23 = st.columns([1,1,1,1,1])
                with col21:
                    submitted = st.form_submit_button("Guardar")
                    if submitted:
                        ainsurance_db.insert_register_ainsurance(fecha, nBitacora, sCliente, mEntrada, marca, modelo, placas, economico, latitud, longitud, estado, municipio, tramo, estatus, coment)
                        st.success("¡Guardado!")
    
        elif options=="Mapa de Calor":
            
            df1 = pd.DataFrame(obtener_df())
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%d/%m/%Y')
            df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
            df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
            df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
            df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            
            st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
            st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde ***{df1.Mes.min()} {df1.Año.min().astype(int)}*** a ***{df1.Mes.max()} {df1.Año.max().astype(int)}***.")
    
            st.markdown("<h5 style='text-align: left;'>Seleccionar datos</h5>", unsafe_allow_html=True)
            c10, c11, c12 = st.columns(3)

            with c10:
                container4 = st.container()
                allC4 = st.checkbox("Seleccionar Todos", key="chk3")
                if allC4:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es):', sorted_unique_cliente1, sorted_unique_cliente1, key="cliente3")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
                else:
                    sorted_unique_cliente1 = sorted(df1['Cliente'].unique())
                    selected_cliente2 = container4.multiselect('Cliente(es)', sorted_unique_cliente1, key="cliente4")
                    df_selected_cliente2 = df1[df1['Cliente'].isin(selected_cliente2)].astype(str)
        
            with c11:
                container5 = st.container()
                allC5 = st.checkbox("Seleccionar Todos", key="chk4")
                if allC5:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, sorted_unique_ao2, key="año3") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
                else:
                    sorted_unique_ao2 = sorted(df_selected_cliente2['Año'].unique())
                    selected_ao2 = container5.multiselect('Año(s):', sorted_unique_ao2, key="año4") 
                    df_selected_ao2 = df_selected_cliente2[df_selected_cliente2['Año'].isin(selected_ao2)].astype(str)
    
            with c12:
                container6 = st.container()
                allC6 = st.checkbox("Seleccionar Todos", key="chk5")
                if allC6:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, sorted_unique_mes2, key="mes2") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)
                else:
                    sorted_unique_mes2 = sorted(df_selected_ao2['Mes'].unique())
                    selected_mes2 = container6.multiselect('Mes(es):', sorted_unique_mes2, key="mes3") 
                    df_selected_mes2 = df_selected_ao2[df_selected_ao2['Mes'].isin(selected_mes2)].astype(str)

            mapa = map_coropleta_fol(df_selected_mes2)