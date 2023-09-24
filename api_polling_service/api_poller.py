# Imports
import os
import requests
from dotenv import load_dotenv


# Define an ApiPoller class that has 3 methods defined:
# 1. __make_api_call: this is a private helper method that contains the logic for making api calls
# 2. get_all_movies: this method calls one of the 2 databases, and grabs all movies
# 3. get_movie_data: this method calls one of the 2 databases, and takes an ID to return a specific movie info
class ApiPoller:
    def __init__(self, base_url="", auth_token="", timeout=10, max_retries=5):
        self.base_url = base_url
        self.auth_token = auth_token
        self.timeout = timeout
        self.max_retries = max_retries

    # internal method to make api calls
    def __make_api_call(self, full_url, headers):
        retries = 0
        while retries < self.max_retries:
            response = requests.get(full_url, headers=headers, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 500:
                print("Received Internal Server Error (500). Retrying...")
                retries += 1
            else:
                print(f"Error: {response.status_code}")
                return None

    # public method to get all movies info from the api
    def get_all_movies(self, database):
        try:
            full_url = self.base_url + "/" + database + "/movies"
            headers = {"x-access-token": self.auth_token}
            return self.__make_api_call(full_url, headers)

        except requests.exceptions.Timeout:
            print("The request timed out. Please try again later.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    # public method to get specific movie data given an id
    def get_movie_data(self, database, movie_id):
        # since we will be cleaning the IDs, we need to attach the prefix back to make requests
        if database == "cinemaworld":
            db_prefix = "cw"
        elif database == "filmworld":
            db_prefix = "fw"
        api_path_single_movie_id = db_prefix + movie_id

        try:
            full_url = (
                self.base_url
                + "/"
                + database
                + "/movie"
                + "/"
                + api_path_single_movie_id
            )
            headers = {"x-access-token": self.auth_token}
            return self.__make_api_call(full_url, headers)

        except requests.exceptions.Timeout:
            print("The request timed out. Please try again later.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None


# manual testing
if __name__ == "__main__":
    # load in the environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
    api_token = os.environ.get("API_TOKEN")
    api_url = os.environ.get("API_URL")

    # these are the 2 databases
    db_names = ["cinemaworld", "filmworld"]

    # Define the headers with the authentication token
    apiPollerObj = ApiPoller(base_url=api_url, auth_token=api_token)

    # get all movies
    response = apiPollerObj.get_all_movies(database=db_names[0])
    print(response)

    # get a specific movie
    response = apiPollerObj.get_movie_data(database=db_names[0], movie_id="0121766")
    print(response)
