import pandas as pd
import numpy as np

def book_isbn(titulo_libro: str, autor: str, dataframe):
    '''Funcion para obtener el numero de ISBN a partir de un título'''
    # Convertir el título del libro a minúsculas para realizar una búsqueda sin distinción entre mayúsculas y minúsculas
    titulo_libro = titulo_libro.lower()
    autor_libro = autor.lower()

    # Filtrar el DataFrame para encontrar el ISBN correspondiente al título
    resultado = dataframe[(dataframe['Title'].str.lower() == titulo_libro) &
                          (dataframe['Author'].str.lower() == autor_libro)]

    if not resultado.empty:
        # Si se encuentra una coincidencia, devolver el ISBN
        isbn_encontrado = resultado.iloc[0]['ISBN']
        return isbn_encontrado
    else:
        # Si no se encuentra ninguna coincidencia, devolver un mensaje indicando que no se encontró el ISBN
        return f"No se encontró el ISBN para el libro con título '{titulo_libro}'."
