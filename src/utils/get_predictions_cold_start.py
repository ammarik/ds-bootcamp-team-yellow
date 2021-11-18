import pickle
from sklearn.neighbors import NearestNeighbors
import numpy as np




occupations = ['K 12 Student', 'Academic Educator', 'Artist',
       'Clerical Admin', 'College Graduate Student', 'Customer Service',
       'Doctor Health Care', 'Executive Mangerial', 'Farmer', 'Homemaker',
       'Lawyer', 'Other', 'Programmer', 'Retired',
       'Sales/Marketing', 'Scientist', 'Self Employed', 'Technician/Engineer',
       'Tradesman/Craftsman', 'Unemployed', 'Writer']


def load_pickle(file_name):

    knn_model_bytes = open(file_name, "rb")
    knn_model = pickle.load(knn_model_bytes)
    knn_model_bytes.close()

    return knn_model

def get_prediction(processed_input, knn_model):

    #user_id = int(knn_model.kneighbors(processed_input, return_distance=False)[0]) + 1

    #int(x_1[0])+1

    user_id = int(knn_model.kneighbors(processed_input, return_distance=False)[0]) + 1



    return user_id


#returns the index which should be set to 1 in the input array. +2 since first two columns are occupied (age, gender)

def index_occupation(occ):

    return occupations.index(occ) + 2

def get_gender(gender):

    encoding = 0 if gender=='Male' else 1
    return encoding

def normalize_age(age):

    return (age - 1) / (56 - 1)    

def preprocess_input(gender, age, occupation):
    
    model_input = np.zeros((1,23))
    model_input[0][0] = get_gender(gender)
    model_input[0][1] = normalize_age(age)
    model_input[0][index_occupation(occupation)] = 1

    return model_input
if __name__ =='__main__':
    
    knn_model = load_pickle("../../data/knn_model.pickle")
    processed = np.array([[0.        , 0.30909091, 0.        , 0.        , 0.        ,
       0.        , 1.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        , 0.        , 0.        ,
       0.        , 0.        , 0.        ]])
    #index_occupation('K 12Student')
    
    #print(np.zeros((1,23)))
    #processed = preprocess_input(gender= "Male", age = 31, occupation = 'K 12 Student')
    
    #print(get_prediction(processed))

    x = read_users_wl_filter(1000)

    print(type(x))

    print(x)