"""
Streamlit hello world page
"""

import streamlit as st
import pandas as pd


def recommend(uid=None):
    """ToDo"""
    if uid is None:
        # ToDo: Get recomendations for newcomer
        recomendations = pd.DataFrame(['A', 'B', 'C'])
    else:
        # ToDo: Get recomendations for the user with the given UID
        recomendations = pd.DataFrame(['A', 'B', 'C'])
    st.table(recomendations)



st.title("Movie recommender")

name = st.text_input("Enter Your UID")

if st.button('Login') :
    uid = name.title()
    st.success(uid)
    recommend(uid)

if st.button('Proceed without logging in'):
    recommend()
