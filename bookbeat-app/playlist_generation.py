"""Dos funciones esenciales para el programa:
- Función que obtiene el 'sentiment compound' uttilizando Vader (SentimentIntensityAnalyzer)
- Función que obtiene la playlist basado en comparación de sentimiento y popularidad de las canciones"""

import pandas as pd
import nltk
from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer

download('punkt')
download('vader_lexicon')

def obtain_compound(text):
    """Función que obtiene el sentimiento de un texto usando SentimentIntensityAnalyzer de Vader, y de éste entrega
    el 'sentiment compound' como output (número entre -1 y 1)"""
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    # Devuelve el sentimiento del libro
    return scores['compound']


def playlist_popularity(book_sentiment, songs_df, n_tracks):
    """Función que busca el 'sentiment compound' del título dado y lo compara con el 'sentiment compound' de las
    canciones en el dataset, y genera una playlist de 20 canciones más similares en sentimiento, además tomando en
    cuenta la popularidad de las canciones"""

    # Calcular la diferencia absoluta en el sentimiento
    songs_df['abs_dif'] = abs(songs_df['sentiment'] - book_sentiment)

    # Seleccionar las 20 canciones más similares en sentimiento
    similar_songs = songs_df.nsmallest(70, 'abs_dif')

    # Ordenar las canciones en base a 'track_popularity'
    sorted_playlist = similar_songs.sort_values(by=['track_popularity', 'abs_dif'], ascending=[False, True]).head(int(n_tracks))

    return sorted_playlist
