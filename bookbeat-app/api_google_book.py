'''Defimos función para buscar un libro en la api de Google Books
La función devuelve la descripción de un libro'''

import requests
import json

def obtener_descripcion_isbn(isbn):
    '''Retorna la descripción de un libro a partir de su número de ISBN'''
    base_url = "https://www.googleapis.com/books/v1/volumes"
    parametros = {"q": f'isbn:{isbn}'}

    # Hacer la solicitud a la API de Google Books
    respuesta = requests.get(base_url, params=parametros)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if respuesta.status_code == 200:
        # Obtener datos del libro
        libro = respuesta.json()

        # Verifica si hay libro
        if libro['totalItems'] != 0:
            book_description = libro["items"][0]["volumeInfo"]

            # Verificar si hay un resumen disponible
            resumen = book_description.get("description", "No hay resumen disponible.")
            return resumen

        else:
            return "No se encontro libro"

    else:
        # Manejar el caso de error
        return "Error al obtener información del libro."
