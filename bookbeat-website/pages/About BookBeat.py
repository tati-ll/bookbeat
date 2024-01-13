import streamlit as st
import os

import numpy as np
import pandas as pd

import sys
sys.path.append("..")

from bookbeat.playlist_generation import playlist_popularity

# -- Set page config
app_page_title = 'About BookBeat'

st.set_page_config(page_title=app_page_title, page_icon=":book:")

st.image("../raw_data/BookBeat_3.png")
