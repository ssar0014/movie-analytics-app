# Imports
import os
import requests
from dotenv import load_dotenv
# from minio import Minio
# from minio.error import ResponseError

# Define an ApiPoller class that has 2 methods defined: 
# 1. get_all_movies: this method calls one of the 2 databases, and grabs all movies
# 2. get_movie_data: this method calls one of the 2 databases, and takes an ID to return a specific movie info
class ApiPoller:
    def __init__(self, base_url="", auth_token="", timeout=10, max_retries=5):
        self.base_url = base_url
        self.auth_token = auth_token
        self.timeout = timeout
        self.max_retries = max_retries
    
    def get_all_movies(self, database):
        retries = 0
        while retries < self.max_retries:
            try:
                # Get all the movies data from the cinemaworld database
                full_url = self.base_url + "/" + database + "/movies"
                headers = {"x-access-token": self.auth_token}
                response = requests.get(full_url, headers=headers, timeout=self.timeout)

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 500:
                    print("Received Internal Server Error (500). Retrying...")
                    retries += 1
                else:
                    print(f"Error: {response.status_code}")
                    return None

            except requests.exceptions.Timeout:
                print("The request timed out. Please try again later.")
                return None

            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                return None
        
if __name__ == "__main__":
    # load in the environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))
    api_token = os.environ.get("API_TOKEN")
    api_url = os.environ.get("API_URL")
    
    # these are the 2 databases
    db_names = ["cinemaworld", "filmworld"]

    # these are the different paths to obtain data from
    api_path_all_movies = "movies" # this path returns all movies in the database in a single response object
    api_path_single_movie = "movie" # we need to provide this path with an ID, to get a single movie's response
    api_path_single_movie_id = "" # initiating the movie id with an empty string

    # Define the headers with the authentication token
    apiPollerObj = ApiPoller(base_url=api_url, auth_token=api_token)

    response = apiPollerObj.get_all_movies(database=db_names[0])
    print(response)
