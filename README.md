# Streamlit app for the movie recommender

This is the repository for our movie recommender app.

# Setup
Create your environment from the requirements.txt
````
cd ds-bootcamp-team-yellow
pip install -r requirements.txt
````

# How to run
Activate the env
````
source env/bin/activate
````
Run the app
````
streamlit run src/app.py
````
If you are running locally, you may need to set your ENV to LOCAL in order to retrieve the config
You also need to add a config.local.json with your API_KEY from IBM Cloud when testing locally.

# Guidelines for contributing
Make sure to create a new branch and send a pull request for your changes.
Try to adhere to the conventional commits (e.g. using feat, refactor, fix, etc.)

# Architecture overview
tbc