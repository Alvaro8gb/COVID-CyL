import streamlit as st
import pandas as pd
from os.path import join
import pydeck as pdk
from PIL import Image


COLUMNAS = [
    'Nuevos Hospitalizados en Planta',
    'Hospitalizados en Planta',
    'Nuevos Hospitalizados en UCI',
    'Hospitalizados en UCI',
    'Nuevas Altas', 'Altas',
    'Nuevos fallecimientos', 'Fallecimientos'
]


def fmt_norm(x): return x.strip().replace(" ", "_") + "_norm"


@st.cache_data
def load_image(image_path):
    img = Image.open(image_path)
    return img


def preprocesing(df):

    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')
    df[['Latitud', 'Longitud']] = df['posicion'].str.split(
        ',', expand=True).astype(float)

    df.rename(columns={
        'hospital': 'Hospital',
        'nuevos_hospitalizados_planta': 'Nuevos Hospitalizados en Planta',
        'hospitalizados_planta': 'Hospitalizados en Planta',
        'hospitalizados_planta_incluidos_sospecha': 'Hospitalizados en Planta (Incluidos Sospechosos)',
        'nuevos_hospitalizados_uci': 'Nuevos Hospitalizados en UCI',
        'hospitalizados_uci': 'Hospitalizados en UCI',
        'hospitalizados_uci_incluidos_sospecha': 'Hospitalizados en UCI (Incluidos Sospechosos)',
        'nuevas_altas': 'Nuevas Altas',
        'porcentaje_ocupacion_uci': 'Porcentaje de ocupación en UCI',
        'altas': 'Altas',
        'nuevos_fallecimientos': 'Nuevos fallecimientos',
        'fallecimientos': 'Fallecimientos'
    }, inplace=True)

    for col in COLUMNAS:
        df[col] = df[col].fillna(0)
        maxi = df[col].max()
        mini = df[col].min()
        df[fmt_norm(col)] = (
            ((df[col] - mini) / (maxi - mini)) * 999 + 1).astype(int)

    return df


def toggle_date_selector():
    st.session_state.show_slider = not st.session_state.show_slider


def main():

    logo_image = load_image("img/logo.png")

    st.sidebar.write(
        "<h1> VIII Concurso de Datos Abiertos </h1> ", unsafe_allow_html=True)
    st.sidebar.image(
        logo_image, caption='https://datosabiertos.jcyl.es/', use_column_width=True)

    df = pd.read_csv(
        join("data", "situacion-de-hospitalizados-por-coronavirus-en-castilla-y-leon.csv"), delimiter=";")

    df = preprocesing(df)

    st.title(
        "PandemIA CyL: Monitorización de Hospitales por COVID-19 en Castilla y León")

    if 'show_slider' not in st.session_state:
        st.session_state.show_slider = True

    if st.button("Cambiar método de selección de fecha", on_click=toggle_date_selector):
        pass

    # Muestra el slider o el date input según el estado
    if st.session_state.show_slider:
        st.write("Slider")
        selected_date = st.slider(
            "Selecciona una fecha:",
            min_value=df['fecha'].min().date(),
            max_value=df['fecha'].max().date(),
            value=df['fecha'].min().date(),  # Valor inicial
            format="YYYY-MM-DD"  # Formato de fecha
        )
    else:
        st.write("Calendario")
        selected_date = st.date_input(
            "Seleccione una fecha",
            value=df['fecha'].min(),
            min_value=df['fecha'].min(),
            max_value=df['fecha'].max()
        )

    filtered_df = df[df["fecha"] == pd.to_datetime(selected_date)]

    dato_repr = st.selectbox("Seleccione qué dato representar:", COLUMNAS)

    filtered_df = filtered_df.sort_values(by=dato_repr, ascending=False)

    if not filtered_df.empty:
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=filtered_df,
            get_position='[Longitud, Latitud]',
            get_color='[255, 0, 0, 160]',
            get_radius=f'{fmt_norm(dato_repr)} * 10',
            radius_scale=2,
            opacity=0.9,
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=filtered_df['Latitud'].mean(),
            longitude=filtered_df['Longitud'].mean(),
            zoom=6.5,
            pitch=0,
        )

        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": f"{{Hospital}}: {{{dato_repr}}}"},
        )

        st.pydeck_chart(r)
        st.write(f"Número de hospitales: {len(filtered_df)}")
        st.write("Resumen:")
        st.dataframe(filtered_df[[
            'Hospital', dato_repr]].set_index('Hospital'))

    else:
        st.write("No hay datos disponibles para la fecha seleccionada.")

    st.write("<h2> IA Predictiva de futuros brotes </h2> ",
             unsafe_allow_html=True)
    st.info("🔧 Esta sección estará disponible en el futuro. ¡Mantente atento a las actualizaciones!")


if __name__ == "__main__":
    main()
