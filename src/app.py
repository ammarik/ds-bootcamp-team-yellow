"""
Streamlit hello world page
"""

import streamlit as st
import pandas as pd

from conn.wml_client import WMLClient
from movie_source import MovieInfoSource


def recommend(uid=None):
    """
    This function retrieves and displays in a table
    the recommended movies, both for the new/undetermined 
    user and for the user specified by his/her UID.
    """
    # logged in user --> get personalized recs using WML api
    if uid:
        try:
            model_conn = WMLClient()
            # get the predictions for the given uid
            # TODO define inputs needed for final model
            # TODO show outputs from WML not dummy outputs
            model_conn.get_predictions()
            st.success(f'Recommended movies for user with  uid: {uid}')

            recommendations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

            for recommendation in recommendations:
                st.header(movie_source.get_movie_name(recommendation))
                description, image = movie_source.get_movie_info(recommendation)
                st.write(description)
                st.image(image)

        except:  # for testing purposes
            # if not able to connect, show some default recommendations
            recommendations = pd.DataFrame(
                ['The Shawshank Redemption', 'The Godfather',
                    'Pulp Fiction', 'Forrest Gump'],
                columns=['Movie name'])
    # cold start user --> show the most beloved movies
    else:
        # show hard-coded recommendations from a file for cold-start user using a file
        # TODO change to csv
        recommendations = pd.DataFrame(
            ['The Shawshank Redemption', 'The Godfather',
                'Pulp Fiction', 'Forrest Gump'],
            columns=['Movie name'])
    st.table(recommendations)

movie_source = MovieInfoSource()

st.title("Movie recommender")

uid = st.text_input("Enter Your UID")

if st.button('Login'):
    recommend(uid)

if st.button('Proceed without logging in'):
    recommend()
