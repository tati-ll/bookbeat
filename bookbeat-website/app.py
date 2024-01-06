import streamlit as st
import os

import numpy as np
import pandas as pd

'''
# BOOKBEAT'''

st.markdown("""
## Select a book
""")

# Ruta al archivo CSV
ruta_archivo = "/home/cecigatta/code/ceci-jitsi/bookbeat/raw_data/books_sentiment.csv"

# Cargar datos desde el archivo CSV
data = pd.read_csv(ruta_archivo)

# Crear un menú desplegable con la lista de libros
libro_seleccionado = st.selectbox("Selecciona un libro:", data['Book'].tolist(), index=0, key='libro')
libros_seleccionados = st.multiselect("Selecciona un libro:", data['Book'].tolist(), key="libro")
