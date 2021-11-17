"""
Streamlit hello world page
"""

import streamlit as st
import pandas as pd


def recommend(uid=None):
    """
    This function retrieves and displays in a table
    the recommended movies, both for the new/undetermined 
    user and for the user specified by his/her UID.
    """

    if uid is None:
        # ToDo: Obtain recomendations for newcomer using API.
        recomendations = pd.DataFrame(
            ['The Shawshank Redemption', 'The Godfather', 'Pulp Fiction', 'Forrest Gump'],
             columns =['Movie name'])
    else:
        # ToDo: Get recomendations for the user with the given UID using API.
        st.success(f'Recommended movies for user with  uid: {uid}')
        recomendations = pd.DataFrame(
            ['Shrek', 'Toy Story', 'Frozen', 'Finding Nemo'],
             columns =['Movie name'])
    st.table(recomendations)



st.title("Movie recommender")

uid = st.text_input("Enter Your UID")

if st.button('Login') :
    recommend(uid)

if st.button('Proceed without logging in'):
    recommend()