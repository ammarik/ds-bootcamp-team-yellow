"""
Script to get recommendations for an existing user
The script filters out the predictions if the user has already seen a movie
"""

import logging
import pickle
import typing as th

import numpy as np
import pandas as pd

from .get_logger import get_logger

logger: logging.Logger = get_logger()


def read_predictions_pkl(user_id: int) -> np.ndarray:
    """
    Read the predictions pickle file
    Currently: shape (6040, 3706), these are users with ID 1 until 6040
    Movies are until 3706
    """
    with open('model/predictions.pkl', 'rb') as handle:
        predictions = pickle.load(handle)
    return predictions[user_id]


def read_users_wl_filter(user_id: int) -> th.List:
    """
    Read what the users already watched from a file
    Currently: shape (162541, 2), only need users with ID 1 until 6040
    """
    users_wl = pd.read_csv('data/users-watchlist.csv')
    # drop the users with ID not present in small dataset
    users_wl_selected = users_wl.loc[users_wl['userid'] < 6040]
    # split the watchlist into a list of integer values
    users_wl_cs = users_wl_selected[users_wl_selected['userid']
                                    == user_id]['watchlist'].values[0].split(",")
    users_wl_int = list(map(int, users_wl_cs))
    # drop the movies from the list that are not included in the small dataset
    users_wl_movies_selected = [i for i in users_wl_int if i < 3706]
    return users_wl_movies_selected


def get_predictions(user_id: int, nr_of_recommendations: int) -> th.List:
    """
    Get predictions from predictions matrix
    Currently only for users 1 to 6040
    Filtered by movies from watchlist if user has already seen the movie
    Best recommendations are those with highest score in matrix

    :param user_id:
    :param nr_of_recommendations:
    :return:
    """
    # read the prediction matrix
    preds_for_user_all = pd.DataFrame(read_predictions_pkl(user_id))
    # reset the index as it starts at 0, we want 1
    preds_for_user_all.index = np.arange(1, len(preds_for_user_all) + 1)
    # filter the movies the user has already watched
    watched_for_user = read_users_wl_filter(user_id)
    preds_for_user_not_watched = preds_for_user_all.drop(
        preds_for_user_all.index[watched_for_user])
    # only show the number of recommendations the users wishes to see
    top_n_preds = preds_for_user_not_watched[0].nlargest(nr_of_recommendations)
    logger.debug(top_n_preds)
    return top_n_preds.index.tolist()


if __name__ == "__main__":
    top_n_preds = get_predictions(6039, 10)
    # read_users_wl_filter()
