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

def obtener_df():
    data = ainsurance_db.fetch_all_ainsurance()
    return data
    
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

    elif options=="Data Visualización":
        
        df = pd.DataFrame(obtener_df())
        df = df[['Fecha', 'Nombre Monitorista', 'Bitácora', 'Cliente', 'Motivo de Entrada', 'Marca', 'Modelo', 'Placas', 'Economico', 'Latitud', 'Longitud', 'Estado', 'Municipio', 'Tramo', 'Estatus', 'Observaciones']]
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d', errors='coerce')
        df['Año'] = df['Fecha'].apply(lambda x: x.year)
        df['MesN'] = df['Fecha'].apply(lambda x: x.month)
        df['Mes'] = df['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})

        st.markdown("<h2 style='text-align: left;'>Visualización de Datos del Histórico de Eventos</h2>", unsafe_allow_html=True)
        st.write(f"Marco de datos del histórico de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde {df.Mes.values[0]} {df.Año.values[0].astype(int)} a {df.Mes.values[-1]} {df.Año.values[-1].astype(int)} .")
        st.dataframe(df)

        """
        c1, c2, c3 = st.columns(3)

        with c1:
            container1 = st.container()
            allC1 = st.checkbox("Seleccionar Todos", key="chk1")
            if allC1:
                sorted_unique_cliente = sorted(df['Cliente'].unique())
                selected_cliente = container1.multiselect('Cliente(es):', sorted_unique_cliente, sorted_unique_cliente, key="cliente1")
                df_selected_cliente = df[df['Cliente'].isin(sorted_unique_cliente)].astype(str)
            else:
                sorted_unique_cliente = sorted(df['Cliente'].unique())
                selected_cliente = container1.multiselect('Cliente(es)', sorted_unique_cliente, key="cliente2")
                df_selected_cliente = df[df['Cliente'].isin(sorted_unique_cliente)].astype(str)
            
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

        st.dataframe(df_selected_mes)

        # Métricas

        total_eventos = df_selected_mes['Bitácora'].count(axis=1)
        total_recuperados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'RECUPERADO'].count()
        total_consumados = df_selected_mes.loc[df_selected_mes.loc[:, 'Estatus'] == 'CONSUMADO'].count()
        c4, c5, c6 = st.columns(3)
        col1.metric("Total Eventos", f"{total_eventos}")
        col2.metric("Total Recuperados", f"{total_recuperados}")
        col3.metric("Total Consumados", f"{total_consumados}")

        # Sankey

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

        # Diagrama Sankey
        st.markdown("<h3 style='text-align: left;'>Flujo de Eventos</h3>", unsafe_allow_html=True)

        dSankey = df_selected_mes.groupby(['Estado','Tramo','Estatus']).aggregate({'Estatus':'count'}).reset_index()

        fig = genSankey(dSankey,cat_cols=['Estado','Tramo','Estatus'],value_cols='Estatus',title='Flujo de Eventos AInsurance')
        st.plotly_chart(fig)

        st.markdown("<h3 style='text-align: left;'>Indicadores</h3>", unsafe_allow_html=True)

        def df_grafico(df):
    
            df['Fecha y Hora'] = pd.to_datetime(df['Fecha y Hora'], format='%Y-%m-%d', errors='coerce')

            # Para Cumplimiento
            df1 = df.copy()
            df1 = df1.loc[df1.loc[:, 'Estatus'] == 'RECUPERADO']
            df1.drop(['Dia','Motivo Entrada', 'Eco', 'Marca', 'Modelo', 'Latitud', 'Longitud','Estado', 'Municipio', 'Tramo'], axis = 'columns', inplace=True)    
            df1 = df1.set_index('Fecha y Hora')
            df2 = pd.DataFrame(df1['Placas'].resample('M').count())
            df2 = df2.rename(columns={'Placas':'RECUPERADO'})

            # Para No Cumplimiento
            df3 = df.copy()
            df3 = df3.loc[df3.loc[:, 'Estatus'] == 'CONSUMADO']
            df3.drop(['Dia','Motivo Entrada', 'Eco', 'Marca', 'Modelo', 'Latitud', 'Longitud','Estado', 'Municipio', 'Tramo'], axis = 'columns', inplace=True)    
            df3 = df3.set_index('Fecha y Hora')
            df4 = pd.DataFrame(df3['Placas'].resample('M').count())
            df4 = df4.rename(columns={'Placas':'CONSUMADO'})

            # Unir dataframe
            df5 = pd.concat([df2, df4], axis=1)
    
            # Reset Indíces
            df5 = df5.reset_index()

            # Preparar Dataframe Final
            df5['MesN'] = df5['Fecha y Hora'].apply(lambda x: x.month)
            df5['Mes'] = df5['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})
            df5['Año'] = df5['Fecha y Hora'].dt.year
            df5 = df5.fillna(0)
            df5['Total'] = (df5['RECUPERADO'] + df5['CONSUMADO'])
            df5['% Recuperado'] = round((df5['RECUPERADO'] / df5['Total']),2) * 100
            df5['% Consumado'] = round((df5['CONSUMADO'] / df5['Total']),2) * 100
            df5['Recuperados (%)'] = round((df5['RECUPERADO'] / df5['Total']),2) * 100
            df5['Mes Año'] = df5['Mes'] + ' ' + df5['Año'].astype(str)
        
            df5 = df5.dropna()

            return df5

        def g_recuperacion(df):

            sr_data1 = go.Bar(x = df['Fecha y Hora'],
                        y=df['RECUPERADO'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Recuperados',
                        text= [f'Recuperado(s): {x:.0f}' for x in df['RECUPERADO']]
                        )
    
            sr_data2 = go.Bar(x = df['Fecha y Hora'],
                        y=df['CONSUMADO'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Consumados',
                        text= [f'Consumado(s): {x:.0f}' for x in df['CONSUMADO']]
                        )
    
            sr_data3 = go.Bar(x = df['Fecha y Hora'],
                        y=df['Total'],
                        opacity=0.8,
                        yaxis = 'y1',
                        name='Intentos',
                        text= [f'Intentos: {x:.0f}' for x in df['Total']]
                        )
    
            sr_data4 = go.Scatter(x = df['Fecha y Hora'],
                        y=df['Recuperados (%)'],
                        line=go.scatter.Line(color='green', width = 0.6),
                        opacity=0.8,
                        yaxis = 'y2',
                        hoverinfo = 'text',
                        name='% Recuperados',
                        text= [f'Recuperados(s): {x:.0f}%' for x in df['Recuperados (%)']])
    
            # Create a layout with interactive elements and two yaxes
            layout = go.Layout(height=500, width=700, font=dict(size=7), hovermode="x unified",
                   #title='Robos',
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
            st.plotly_chart(fig)

        c1, c2 = st.columns((1,1))
        with c1:
            st.markdown("<h3 style='text-align: left;'>Gráfico Mensual de Robos</h3>", unsafe_allow_html=True)
            d1 = df_grafico(df_selected_mes)
            #st.write(d1)
            g1 = g_recuperacion(d1)
        with c2:
            st.markdown('### Segmentación de Intentos de Robos')
            df_pie = df_selected_mes.groupby(['Estatus']).size()
            df_pie1 = pd.DataFrame(df_pie)
            df_pie1.reset_index(drop = False, inplace = True)
            df_pie1 = df_pie1.rename(columns={'Estatus':'Tipo de Evento', 0:'Total'})
            plt.figure(figsize = (2,2))
            st.write(px.pie(df_pie1, values='Total', names='Tipo de Evento'))
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
        """
    elif options=="Mapa de Calor":
        
        df1 = pd.DataFrame(get_all_periods())
        df1['Fecha'] = pd.to_datetime(df1['Fecha'], format='%Y-%m-%d', errors='coerce')
        df1['Año'] = df1['Fecha'].apply(lambda x: x.year)
        df1['MesN'] = df1['Fecha'].apply(lambda x: x.month)
        df1['Mes'] = df1['MesN'].map({1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"})

        st.markdown("<h2 style='text-align: left;'>Mapa de Eventos AInsurance</h2>", unsafe_allow_html=True)
        st.write(f"Mapa de eventos que fueron detonados como emergencia por los clientes AInsurance de AI27 desde {df1.Mes.values[0]} {df1.Año.values[0].astype(int)} a {df1.Mes.values[-1]} {df1.Año.values[-1].astype(int)} .")


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
        
        mapa = map_coropleta_fol(df1)
