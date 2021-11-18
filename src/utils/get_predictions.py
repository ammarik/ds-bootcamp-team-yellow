"""
Script to get recommendations for an existing user
The script filters out the predictions if the user has already seen a movie
"""

import logging
import pickle
import typing as th

import numpy as np
import pandas as pd

# from .get_logger import get_logger

# logger: logging.Logger = get_logger()


def read_predictions_pkl(user_id: int) -> np.ndarray:
    """
    Read the predictions pickle file
    Currently: shape (6040, 3706), these are users with ID 1 until 6040
    Movies are until 3706
    """
    with open('model/predictions-v2.pkl', 'rb') as handle:
        predictions = pickle.load(handle)
    return predictions[user_id - 1]


def read_user_movie_matrix() -> pd.DataFrame:
    """
    """
    user_movie_matrix = pd.read_csv('data/user-movie-matrix.csv',
                                    index_col=0)
    return user_movie_matrix





def read_users_wl_filter(user_id: int) -> th.List:
    """
    Read what the users already watched from a file
    Currently: shape (162541, 2), only need users with ID 1 until 6040
    Note: changed to smaller selection of users due to Git constraints
    """
    users_wl = pd.read_csv('data/users-watchlist-selected.csv')
    # drop the users with ID not present in small dataset
    users_wl_selected = users_wl.loc[users_wl['userid'] < 6040]
    # split the watchlist into a list of integer values
    users_wl_cs = users_wl_selected[users_wl_selected['userid']
                                    == user_id]['watchlist'].values[0].split(",")
    users_wl_int = list(map(int, users_wl_cs))
    # drop the movies from the list that are not included in the small dataset
    users_wl_movies_selected = [i for i in users_wl_int if i < 3706]
    return users_wl_movies_selected

def read_ranked_watchlist(user_id: int) -> th.List:
    """
    Read what the users already watched from a file
    Currently: shape (162541, 2), only need users with ID 1 until 6040
    Note: changed to smaller selection of users due to Git constraints
    """
    # print(user_id)

    users_all_watchlist = pd.read_csv('data/USERS_WATCHLIST_RANKED_TOP5.csv')
    # drop the users with ID not present in small dataset
    #users_wl_selected = users_wl.loc[users_wl['userid'] < 6040]
    # split the watchlist into a list of integer values
    """
    users_wl_cs = users_wl[users_wl['userid']
                                    == user_id]['watchlist'].values[0].split(",")
    users_wl_int = list(map(int, users_wl_cs))
    """
    # drop the movies from the list that are not included in the small dataset

    #users_wl_cs = users_all_watchlist[users_all_watchlist['userid']== user_id][:5]
    users_wl_cs = users_all_watchlist[users_all_watchlist['userid']
                                == user_id]['top5movies'].values[0].split(",")

    # print("this is the users wl cs : " + str(users_wl_cs))
    users_wl_int = list(map(int, users_wl_cs))
    return users_wl_int


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
    # logger.debug(top_n_preds)
    return top_n_preds.index.tolist()


def recommend_for_existing_user(user_id, number_of_recommendations) -> th.Union[th.List, th.List]:
    """
    """
  # ***  PARAMS: user_id of exisiting user; number_of_recommendations for movies
    predicted_ratings = read_predictions_pkl(user_id)
    # get prediction for specific user
    # predicted_ratings = predictions[user_id - 1]

    # actual rating of specific user
    Ratings = read_user_movie_matrix()
    rated_movies = Ratings.iloc[user_id - 1]

    # if not rated initially, filter is set to True
    filter_for_unreviewed_movies = [rated_movies == 0][0]

    # exhaustive filter to keep index and filter prediction for already reviewed movies
    counter = 0
    pred_ratings_unwatched_movies = []

    for state in filter_for_unreviewed_movies:
        if state:
            # if not rated, prediction is accepted
            pred_ratings_unwatched_movies.append(predicted_ratings[counter])
        else:
            # if rated, 'prediction' is set to -1 to avoid retrieving information
            pred_ratings_unwatched_movies.append(-1)

        counter = counter + 1
    # sort indicies (movies) based on the value of the numpy array
    # take the desired number of recommended movies
    # flip short list around to have the indicies with the highest value on top

    # see which one works better
    #recommeded_movie_ids = np.flip(np.argsort(pred_ratings_unwatched_movies))[:number_of_recommendations]

    recommeded_movie_ids = np.flip(
        (np.argsort(pred_ratings_unwatched_movies))[-number_of_recommendations:])
    # list(reversed((np.argsort(pred_ratings_unwatched_movies))[-number_of_recommendations:]))

    # we have to get the right id and add one for the actual movie-id
    # recommendations = [x+1 for x in recommeded_movie_ids]

    watched_movies = [rated_movies > 0][0]

    # exhaustive filter to keep index and filter prediction for already reviewed movies
    counter = 0
    watched_movies_only = []
    for state in watched_movies:
        if state:
            # if not rated, prediction is accepted
            watched_movies_only.append(rated_movies.iloc[counter])
        else:
            # if rated, 'prediction' is set to -1 to avoid retrieving information
            watched_movies_only.append(-1)
        counter = counter + 1

    watch_list_top10_biased = np.flip((np.argsort(watched_movies_only)[-10:]))

    # watch_list_top10 = [x+1 for x in watch_list_top10_biased]

    # to get the actual movies
    correct_movie_ids = Ratings.columns

    recommendations = []
    for item in recommeded_movie_ids:
        recommendations.append(correct_movie_ids[item])

    watch_list_top10 = []
    for item in watch_list_top10_biased:
        watch_list_top10.append(correct_movie_ids[item])

    return list(map(int, watch_list_top10)), list(map(int, recommendations))


if __name__ == "__main__":
    # top_n_preds = get_predictions(522, 10)
    # read_users_wl_filter()
    recommend_for_existing_user(2, 3)
