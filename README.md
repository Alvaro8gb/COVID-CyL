



# PandemIA CyL: Monitorización de Hospitales por COVID-19 en Castilla y León

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pandem-ia-cyl.streamlit.app/)

Esta aplicación web proporciona una herramienta de visualización para monitorear los datos hospitalarios relacionados con el COVID-19 en Castilla y León, España. Los usuarios pueden seleccionar diferentes variables como hospitalizaciones, ingresos en UCI, altas y fallecimientos en los hospitales, y visualizar los datos de manera interactiva en un mapa.


## Características

- **Selección de Fecha**: Los usuarios pueden elegir una fecha utilizando un deslizador o un calendario para filtrar los datos.
- **Representación de Datos**: Se pueden seleccionar múltiples métricas relacionadas con los hospitales, como nuevas hospitalizaciones, ingresos en UCI, altas y fallecimientos.
- **Visualización en Mapa**: Los datos filtrados de los hospitales se muestran en un mapa interactivo, mostrando la distribución geográfica y la intensidad de los datos hospitalarios.
- **Normalización de Datos**: Los datos se normalizan y se representan visualmente mediante el escalado de color y tamaño de los puntos.
- **Sección Predictiva**: Sección de marcador de posición para futuras características predictivas basadas en IA sobre posibles brotes de COVID-19.

## Instalación

1. Clona el repositorio o descarga el código fuente.
2. Instala las dependencias de Python necesarias:

```bash
pip install -r requirements.txt
```

## Ejecutar la Aplicación

Para ejecutar la aplicación de Streamlit, navega al directorio del proyecto y ejecuta el siguiente comando:

```bash
streamlit run app.py
```

Esto iniciará el servidor de Streamlit y abrirá la aplicación en tu navegador predeterminado.

## Estructura de la Aplicación

### Funciones

- **`load_image(image_path)`**: Carga y almacena en caché la imagen del logo que se muestra en la barra lateral.
- **`preprocesing(df)`**: Limpia, formatea y normaliza los datos hospitalarios para su visualización. La función también divide la columna `posicion` en coordenadas de latitud y longitud para el mapeo con PyDeck.
- **`toggle_date_selector()`**: Alterna entre los métodos de selección de fecha con deslizador o calendario.

### Columnas Mostradas

Las siguientes columnas se utilizan en la aplicación:

- `Nuevos Hospitalizados en Planta`
- `Hospitalizados en Planta`
- `Nuevos Hospitalizados en UCI`
- `Hospitalizados en UCI`
- `Nuevas Altas`
- `Altas`
- `Nuevos fallecimientos`
- `Fallecimientos`

### Visualización de Datos

- **Mapa PyDeck**: Las ubicaciones de los hospitales se representan como puntos en el mapa, con el tamaño de cada punto escalado de acuerdo con los datos seleccionados.
- **Filtro de Fechas**: Los usuarios pueden filtrar los datos por fecha utilizando un deslizador o un calendario.

## Datos

Los datos para esta aplicación deben estar en formato CSV e incluir las siguientes columnas:
- `hospital`: Nombre del hospital.
- `fecha`: Fecha del registro.
- `nuevos_hospitalizados_planta`: Nuevos ingresos en camas normales.
- `hospitalizados_planta`: Total de hospitalizados en camas normales.
- `nuevos_hospitalizados_uci`: Nuevos ingresos en UCI.
- `hospitalizados_uci`: Total de hospitalizados en UCI.
- `nuevas_altas`: Nuevas altas.
- `altas`: Total de altas.
- `nuevos_fallecimientos`: Nuevos fallecimientos.
- `fallecimientos`: Total de fallecimientos.
- `posicion`: Coordenadas GPS del hospital (en formato `latitud,longitud`).

## Capturas de Pantalla

- **Panel**: Panel principal con barra lateral, mapa y tabla de datos.
- **Selector de Fecha**: Alternar entre deslizador y selector de fecha.

## Características Futuras

- **Módulo Predictivo IA**: En futuras versiones, se añadirá análisis predictivo para pronosticar posibles brotes de COVID-19 basados en los datos proporcionados.

## Licencia

Este proyecto está bajo la licencia [GNU](LICENSE).

## Reporte 

Para más información sobre el proyecto leer [reporte](report.pdf).
## Créditos

- **Fuente de Datos**: [Datos Abiertos Castilla y León](https://datosabiertos.jcyl.es/)
- **Librerías Usadas**: [Streamlit](https://streamlit.io/), [Pandas](https://pandas.pydata.org/), PyDeck, PIL (Pillow)

