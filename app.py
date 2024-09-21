import streamlit as st
import pandas as pd
from os.path import join
import pydeck as pdk

def preprocesing(df):

    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')
    df[['latitude', 'longitude']] = df['posicion'].str.split(',', expand=True).astype(float)
    
    return df 


def main():

    st.sidebar.write("<h1> COVID-19 CyL </h1> ", unsafe_allow_html=True)

    df = pd.read_csv(
        join("data", "situacion-de-hospitalizados-por-coronavirus-en-castilla-y-leon.csv"), delimiter=";")

    df=preprocesing(df)

    st.title("Datos de COVID-19 en Castilla y León")

    st.title("Filtrar por fecha")
    selected_date = st.date_input(
        "Seleccione una fecha",
        value=df["fecha"].min(),
        min_value=df["fecha"].min(),
        max_value=df["fecha"].max()
    )

    filtered_df = df[df["fecha"] == pd.to_datetime(selected_date)]
    st.title(f"Datos de COVID-19 en Castilla y León el {selected_date.strftime('%Y-%m-%d')}")

    columnas = {
        'nuevos_hospitalizados_planta': 'Nuevos Hospitalizados en Planta',
        'hospitalizados_planta': 'Hospitalizados en Planta',
        'hospitalizados_planta_incluidos_sospecha': 'Hospitalizados en Planta (Incluidos Sospechosos)',
        'nuevos_hospitalizados_uci': 'Nuevos Hospitalizados en UCI',
        'hospitalizados_uci': 'Hospitalizados en UCI',
        'hospitalizados_uci_incluidos_sospecha': 'Hospitalizados en UCI (Incluidos Sospechosos)',
        'porcentaje_ocupacion_uci': 'Porcentaje de Ocupación UCI',
        'nuevas_altas': 'Nuevas Altas',
        'altas': 'Altas',
        'nuevos_fallecimientos': 'Nuevos Fallecimientos',
        'fallecimientos': 'Fallecimientos'
    }

    dato_repr = st.selectbox("Seleccione qué dato representar:", list(columnas.values()))
    seleccion_key = [k for k, v in columnas.items() if v == dato_repr][0]

    if not filtered_df.empty:
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=filtered_df,
            get_position='[longitude, latitude]',
            get_color='[255, 0, 0, 160]',  
            get_radius=f'{seleccion_key} * 500',  
            radius_scale=1,
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=filtered_df['latitude'].mean(),
            longitude=filtered_df['longitude'].mean(),
            zoom=7,
            pitch=50,
        )

        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": f"{{hospital}}: {{{seleccion_key}}}"},
        )

        st.pydeck_chart(r)
        st.write(f"Número de hospitales: {len(filtered_df)}")
        st.write("Resumen:")
        st.dataframe(filtered_df[[
                   'hospital', 'nuevos_hospitalizados_planta', 'latitude', 'longitude']].reset_index(drop=True))
        
    else:
        st.write("No hay datos disponibles para la fecha seleccionada.")


if __name__ == "__main__":
    main()
