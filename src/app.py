"""
Streamlit hello world page
"""

import logging
import random

import streamlit as st
import pandas as pd

import conn.wml_client as wmlc
from movie_source import FailedToRetrieveMovieInformation, MovieInfoSource
from typing import List
from utils.get_logger import get_logger

logger: logging.Logger = get_logger()


def present_recommendations(movie_source: MovieInfoSource, recommendations: List[int]) -> None:
    """
    It will obtain more information about each movie
    and it will present it the browser.
    """
    for recommendation in recommendations:
        try:
            st.header(movie_source.get_movie_name(recommendation))
            description, url, image = movie_source.get_movie_info(recommendation)
            col1, col2 = st.columns(2)

            col1.write(url)
            col1.write(description)
            col2.image(image)
        except FailedToRetrieveMovieInformation as e:
            logger.warning(e)


def recommend(add_select_box: str, movie_source: MovieInfoSource) -> None:
    """
    This function retrieves and displays in a table
    the recommended movies for three user types:
    - for the new user
    - for the user specified by his/her UID
    - and for the user who does not want to log in
    """
    # logged in user --> get personalized recs using WML api
    if add_selectbox == 'Yes':
        uid = st.text_input("Enter Your UID")
        if uid:
            try:
                model_conn = wmlc.WMLClient()
                # get the predictions for the given uid
                # TODO define inputs needed for final model
                # TODO show outputs from WML not dummy outputs
                model_conn.get_predictions()
                st.success(
                    f'Welcome back! We think you might enjoy these movies, {uid}')
                
                # TODO replace with real recommendations
                recommendations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                present_recommendations(movie_source, recommendations)
                
            except KeyError as e:  # for testing purposes
                # if not able to connect, show some default recommendations
                logger.warning("WML conn failed")
                logger.warning(e)
                
                recommendations = [1, 2, 3]
                present_recommendations(movie_source, recommendations)
            except:
                logger.warning("Failed due to another reason")

    # cold start user --> enter details and show the most beloved movies to start with
    elif add_selectbox == 'No - sign up':
        name = st.text_input("Enter Your name")
        age = st.text_input("Enter Your age")
        if name and age:
            st.success(
                f'Welcome! here are some movies to get started with, {name}')
            st.success(f'Your user id is 885564')  # dummy user id TODO
            if st.button('Show me recommendations'):
                df_recommendations = pd.read_csv('data/movie-ratings-top10.csv', index_col=[0])
                present_recommendations(movie_source, df_recommendations['movieid'].tolist())

    # anonymous user - show general recommendations / trending movies
    elif add_selectbox == 'No - continue browsing in anonymous mode':
        st.success(
            f'Not sure if you want to sign up? no problem! here are some movies people generally love')
        if st.button('Show me recommendations anyway'):
            recommendations = pd.DataFrame(
                ['The Shawshank Redemption', 'The Godfather',
                    'Pulp Fiction', 'Forrest Gump'],
                columns=['Movie name'])
            st.table(recommendations)

    # if an error occurs
    else:
        st.error(
            'Sorry, there seems to be an issuing retrieving movie recommendations')


def setup_page() -> str:
    """
    Set up the page with the general components
    - The title
    - The sidebar with the three user options
    Return the add_selectbox 
    """

    st.title("Movie recommender")

    # Add a selectbox to the sidebar:
    add_selectbox = st.sidebar.selectbox(
        'Are you an existing user?',
        ('Yes', 
        'No - sign up', 
        'No - continue browsing in anonymous mode')
    )
    return add_selectbox


if __name__ == '__main__':
    add_selectbox = setup_page()
    movie_source = MovieInfoSource()
    recommend(add_selectbox, movie_source)
