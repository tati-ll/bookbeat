import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
import re

download('punkt')
download('stopwords')

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
    sentence = re.sub(r'\s+', ' ', sentence).strip()

    return sentence
