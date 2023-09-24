# imports
import os
import requests
from api_poller import ApiPoller
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)

# load in the environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
api_token = os.environ.get("API_TOKEN")
api_url = os.environ.get("API_URL")

# declare the api poller object
apiPollerObj = ApiPoller(base_url=api_url, auth_token=api_token)


@app.route("/get_all_movies", methods=["GET"])
def get_all_movies():
    # these are the 2 databases
    db_names = ["cinemaworld", "filmworld"]
    response_dict = {}
    for db in db_names:
        if db not in response_dict.keys():
            response_dict[db] = apiPollerObj.get_all_movies(database=db)
    return response_dict


@app.route("/get_all_movies/<string:db_name>", methods=["GET"])
def get_all_movies_db(db_name):
    return apiPollerObj.get_all_movies(database=db_name)


@app.route("/get_movie_info/<string:db_name>/<string:movie_id>", methods=["GET"])
def get_movie_info(db_name, movie_id):
    # get a specific movie
    response = apiPollerObj.get_movie_data(database=db_name, movie_id=movie_id)
    return response


if __name__ == "__main__":
    app.run(debug=True)
