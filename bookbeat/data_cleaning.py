import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
import re

download('punkt')
download('stopwords')

from bookbeat.api_google_book import obtener_descripcion_isbn

"""Se crea función para limpieza de texto.
Una función específica para descripción/blurbs de libros.
Otra específica para letras de canciones."""

def cleaning_books(sentence):
    """Función que realiza limpieza de texto. Incluye limpieza básica: eliminar espacios, pasar a minúscula,
    eliminar números y puntuación. Limpieza avanzada: tokenizar, eliminar stopwords (sólo inglés), y eliminar
    usando la librería re algunas palabras especiales como links"""
    sentence = sentence.strip()
    sentence = sentence.lower()
    sentence = ''.join(char for char in sentence if not char.isdigit())

    # Advanced cleaning
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '')
    tokenized_sentence = word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    tokenized_sentence_cleaned = [w for w in tokenized_sentence if not w in stop_words]

    sentence = ' '.join(word for word in tokenized_sentence_cleaned)

    # Eliminar palabras que comienzan o terminan con "http" y tienen "http" en el medio
    sentence = re.sub(r'\bhttp\w*|\w*http\b|(?<=http)\w*\b', '', sentence)

    # Eliminar símbolos específicos que no están dentro de string.punctuation
    sentence = re.sub(r'[”“—’…‘]', '', sentence)

    # Eliminar palabras particulares
    words_to_remove = ['book', 'story', 'one', 'new', 'isbn', 'oct', 'nov', 'feb', 'sep', 'jul', 'apr', 'dec', 'jan', 'mar', 'may', 'jun', 'aug']
    pattern = r'\b(?:' + '|'.join(re.escape(word) for word in words_to_remove) + r')\b'
    sentence = re.sub(pattern, '', sentence, flags=re.IGNORECASE)

    # Eliminar espacios duplicados resultantes de las sustituciones
    clean_sentence = re.sub(r'\s+', ' ', sentence).strip()

    return clean_sentence


def cleaning_songs(sentence, language):
    """Función que realiza limpieza de texto, específica para letras de canciones.
    Realiza limpieza básica (quitar espacios al inicio/final, puntuación, símbolos, números, pasar a minúsculas)
    Limpieza avanzada: Tokenizar y eliminar stopwords (en 2 idiomas: en, es).
    Quita símbolos y palabras específicas usando Re"""

    sentence = sentence.strip()
    sentence = sentence.lower()
    sentence = ''.join(char for char in sentence if not char.isdigit())

    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '')

    # Eliminar palabras específicas
    words_to_remove = ['uoh', 'yeah', 'ta', 'pumpumpum', 'tumtumtum', 'brumbrumbrum', 'pal', 'pa', 'ay', 'ey', 'wouwouwou',
                       'ihhhyo', 'ihhhye', 'shalala', 'lalala', 'nanana', 'na', 'uh', 'ah', 'ohh', 'oh', 'ooh', 'ho',
                       'mmm', 'hey', 'im', 'oh', 'ohhh', 'ohohoh', 'em', 'ne', 'yo', 'en', 'aint', 'lay', 'youre', 'gon',
                       'til', 'nana', 'wan']
    for word in words_to_remove:
        sentence = re.sub(r'\b' + re.escape(word) + r'\b', '', sentence)

    # Eliminar símbolos específicos que no están dentro de string.punctuation
    sentence = re.sub(r'[”“—’…‘¡¿]', '', sentence)

    # Tokenizar
    tokenized_sentence = word_tokenize(sentence)

    # Define las stopwords según el idioma
    if language == 'en':
        stop_words = set(stopwords.words('english'))
    elif language == 'es':
        stop_words = set(stopwords.words('spanish'))
    else:
        stop_words = set()  # Si el idioma no está en la lista, no eliminar stopwords

    tokenized_sentence_cleaned = [w for w in tokenized_sentence if not w in stop_words]

    cleaned_sentence = ' '.join(word for word in tokenized_sentence_cleaned)

    return cleaned_sentence
