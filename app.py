import streamlit as st
import pandas as pd


def preprocesing(df):


    return df 


def main():

    st.sidebar.write("<h1> COVID-19 CyL </h1> ", unsafe_allow_html=True)

    df = pd.read_csv(
        "data/situacion-de-hospitalizados-por-coronavirus-en-castilla-y-leon.csv", delimiter=";")

    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')

    st.sidebar.title("Filter by Date")
    selected_date = st.sidebar.date_input(
        "Select a date",
        value=df["fecha"].min(),
        min_value=df["fecha"].min(),
        max_value=df["fecha"].max()
    )

    filtered_df = df[df["fecha"] == pd.to_datetime(selected_date)]

    st.title(f"Hospitalizations on {selected_date.strftime('%Y-%m-%d')}")

    if not filtered_df.empty:

        filtered_df[['latitude', 'longitude']] = df['posicion'].str.split(
            ',', expand=True).astype(float)

        st.map(filtered_df[['latitude', 'longitude']])

        st.write(f"Number of hospitals: {len(filtered_df)}")
        st.write("Hospital df:")
        st.dataframe(filtered_df[[
                   'hospital', 'nuevos_hospitalizados_planta', 'latitude', 'longitude']])
    else:
        st.write("No df available for the selected date.")


if __name__ == "__main__":
    main()
